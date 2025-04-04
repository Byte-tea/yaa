"""流式服务器实现"""

import json

from yaa.Server.BaseServer import Server as OutdatedServer
from yaa.Config.Config import Config
from yaa.Agent.ToolCall import Agent
from yaa.Debug.DebugTools import DebugTools

class Server(OutdatedServer):
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        self.dt = DebugTools(self.debug_mode)

    def listen(self):
        """监听并处理请求，支持流式传输"""
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.max_connections)
        print(f"服务器正在监听：{self.host}:{self.port}")
        
        while True:
            self.dt.dprint("进入主监听循环")
            conn, addr = self.socket.accept()
            try:
                # 接收请求数据
                data = conn.recv(4096).decode('utf-8')
                self.dt.dprint(f"接收到原始数据: {data[:100]}...")
                if not data:
                    continue
                    
                # 解析请求头和JSON数据
                headers, body = self._parse_request(data)
                
                # 解析会话数据
                session_data = json.loads(body)
                self.dt.dprint("解析后的会话数据:", session_data)
                use_stream = session_data['config']['llm_api'].get('stream', Config.YAA_CONFIG['stream'])

                # 验证授权
                if not self._validate_auth(headers.get('Authorization')):
                    conn.sendall(b'HTTP/1.1 401 Unauthorized\n\n')
                    continue

                # 检查请求格式是否完整
                if not self._check_request_format(session_data):
                    conn.sendall(b'HTTP/1.1 400 Bad Request\n\n')
                    continue

                # 设置流式响应头
                self.dt.dprint("使用流式模式:", use_stream)
                if use_stream:
                    conn.sendall(b'HTTP/1.1 200 OK\n')
                    conn.sendall(b'Content-Type: text/event-stream\n')
                    conn.sendall(b'Cache-Control: no-cache\n')
                    conn.sendall(b'Connection: keep-alive\n\n')
                else:
                    conn.sendall(b'HTTP/1.1 200 OK\n')
                    conn.sendall(b'Content-Type: application/json\n\n')
                
                agent = Agent()

                # 交给智能体处理
                if use_stream:
                    # 流式处理模式
                    def send_response(response_data):
                        nonlocal conn
                        conn.sendall(f"data: {json.dumps(*response_data)}\n\n".encode('utf-8'))

                    agent.run(session_data=session_data, stream_func=send_response)
                    self.dt.dprint("流式响应结束")
                    conn.sendall(b"data: [DONE]\n\n")
                else:
                    # 非流式处理模式
                    response_data = agent.run(session_data)
                    conn.sendall(json.dumps(response_data).encode('utf-8'))

            except KeyboardInterrupt:
                print("\n服务已停止")
                break
            except Exception as e:
                conn.sendall(b'HTTP/1.1 500 Internal Server Error\n\n')
                print(f"处理请求时出错：{e}")
            finally:
                conn.close()