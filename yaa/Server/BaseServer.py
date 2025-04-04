"""基础服务器模块

职责：
1. 实现简单的 TCP 服务器监听
2. 处理会话数据结构
3. 返回响应消息
"""

import socket
import json

from yaa.Agent.BaseAgent import Agent
from yaa.Auth.KeyAuth import Auth
from yaa.Config.ServerConfig import ServerConfig

class Server:
    def __init__(self, config=None):
        """初始化服务器
        
        参数:
            config (dict): 服务器配置，包含:
                - yaa_server: 服务器配置(ip, port等)
                - security: 安全配置
        """
        if config is None:
            config = ServerConfig.get_default_config()
        else:
            config = ServerConfig.merge_config(config)
            
        server_config = config.get('yaa_server', {})
        self.host = server_config.get('ip', 'localhost')
        self.port = server_config.get('port', 12345)
        self.max_connections = server_config.get('max_connections', 1)
        
        self.security_config = config.get('security', {})
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def listen(self):
        """监听并处理请求"""
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.max_connections)
        print(f"服务器正在监听：{self.host}:{self.port}")
        
        while True:
            conn, addr = self.socket.accept()
            try:
                # 接收请求数据
                data = conn.recv(4096).decode('utf-8')
                if not data:
                    continue
                    
                # 解析请求头和JSON数据
                headers, body = self._parse_request(data)
                
                # 解析会话数据
                session_data = json.loads(body)

                # 验证授权
                if not self._validate_auth(headers.get('Authorization')):
                    conn.sendall(b'HTTP/1.1 401 Unauthorized\n\n')
                    continue

                # 检查请求格式是否完整
                if not self._check_request_format(session_data):
                    conn.sendall(b'HTTP/1.1 400 Bad Request\n\n')
                    continue

                # 交给智能体处理
                response_data = Agent.Agent(session_data)
                
                # 返回响应
                conn.sendall(b'HTTP/1.1 200 OK\n')
                conn.sendall(b'Content-Type: application/json\n\n')
                conn.sendall(json.dumps(response_data).encode('utf-8'))
            except KeyboardInterrupt:
                print("\n服务已停止")
                break
            except Exception as e:
                conn.sendall(b'HTTP/1.1 500 Internal Server Error\n\n')
                print(f"处理请求时出错：{e}")
            finally:
                conn.close()
    
    def _parse_request(self, data):
        """解析HTTP请求"""
        parts = data.split('\r\n\r\n')
        headers_part = parts[0]
        body = parts[1] if len(parts) > 1 else ''
        
        headers = {}
        for line in headers_part.split('\r\n')[1:]:  # 跳过第一行请求行
            if ': ' in line:
                key, value = line.split(': ', 1)
                headers[key] = value
                
        return headers, body
    
    def _validate_auth(self, auth_header):
        """验证授权头"""
        return Auth.check_key(auth_header)

    def _check_request_format(session_data):
        """
        检查会话数据格式是否完整
        
        参数:
        - session_data (dict): 会话数据
        
        返回值:
        - bool: 请求格式是否完整
        """
        required_keys = ['id', 'status', 'messages']
        
        for key in required_keys:
            if key not in session_data or not session_data[key] :
                return False
        
        return True