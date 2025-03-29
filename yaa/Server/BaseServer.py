"""基础服务器模块

职责：
1. 实现简单的 TCP 服务器监听
2. 处理会话数据结构
3. 返回响应消息
"""

import socket
import json
from ..Config.Config import Config
from ..Agent.BaseAgent import BaseAgent

class BaseServer:
    def __init__(self, config=None):
        """初始化服务器
        
        参数:
            config (dict): 服务器配置，包含:
                - yaa_server: 服务器配置(ip, port等)
                - security: 安全配置
        """
        if config is None:
            config = {}
            
        server_config = config.get('yaa_server', {})
        self.host = server_config.get('ip', 'localhost')
        self.port = server_config.get('port', 12345)
        self.max_connections = server_config.get('max_connections', 1)
        
        self.security_config = config.get('security', {})
        self.api_keys = [key['key'] for key in self.security_config.get('api_key', [])]
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def listen(self):
        """监听并处理请求"""
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.max_connections)
        print(f"Server listening on {self.host}:{self.port}")
        
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
                
                # 补全会话配置
                merged_data = Config.merge_config(session_data)
                
                # 交给智能体处理
                response_data = BaseAgent.Agent(merged_data)
                
                # 返回响应
                conn.sendall(b'HTTP/1.1 200 OK\n')
                conn.sendall(b'Content-Type: application/json\n\n')
                conn.sendall(json.dumps(response_data).encode('utf-8'))
                
            except Exception as e:
                conn.sendall(b'HTTP/1.1 500 Internal Server Error\n\n')
                print(f"Error processing request: {e}")
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
        # TODO
        pass