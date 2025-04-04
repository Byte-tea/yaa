from datetime import datetime
import uuid

from yaa.Agent.ToolCall import Agent
from yaa.Client.BaseClient import BaseClient

class Client(BaseClient):
    def __init__(self, debug_mode):
        self.debug_mode = debug_mode
    
    def commander(self, input_message, session_data):
        help_command = ['', '/?', '/help', '/h']
        if input_message in help_command:
            print('可用命令：')
            print(' /exit：退出程序')
            print(' /help：显示帮助信息')
            print(' /clear：清空历史消息')
            print(' /stream：切换流式模式')
            return 'continue'
        elif input_message == '/exit':
            return 'break'
        elif input_message == '/clear':
            session_data['messages'] = []
            print("已清空历史消息")
            return 'continue'
        elif input_message == '/stream':
            session_data['config']['llm_api']['stream'] = not session_data['config']['llm_api']['stream']
            # TODO 非流式处理模式相关。 session_data['config']['yaa']['stream'] = session_data['config']['llm_api']['stream']
            state = "开启" if session_data['config']['llm_api']['stream'] else "关闭"
            print(f"流式模式已{state}")
            return 'continue'

    @classmethod
    def run(self, input_message=None):
        # 创建会话数据
        session_data = {
            'id': str(uuid.uuid4()),
            "object": 'session.data',
            'title': '会话',
            'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "character": "您是 yaa，一个智能体。",
            "status": "进行中",
            'messages': [],
            'config': {
                'yaa': {
                    'stream': True
                },
                'llm_api': {
                    'stream': True
                }
            }
        }

        agent = Agent()

        try:
            while True:
                # 获取用户输入
                if not input_message or input_message == '':
                    input_message = input('> ')

                # 如果输入为命令，执行命令
                action = self.commander(self, input_message=input_message, session_data=session_data)
                if action == 'break':
                    input_message = None
                    break
                elif action == 'continue':
                    input_message = None
                    continue
                
                # 添加用户输入到会话数据
                session_data['messages'].append({
                    'role': 'user',
                    'content': input_message
                })

                input_message = None

                # 交给智能体处理
                if session_data['config']['llm_api']['stream']:
                    # 流式处理模式
                    last_role = session_data['messages'][-1]['role']
                    def print_msg(response_data):
                        nonlocal last_role
                        current_role = response_data['message']['role'] if response_data['message']['role'] else last_role
                        if "content" in response_data['message'] and response_data['message']["content"]:
                            if current_role != last_role:
                                print() # 换行
                                if current_role == 'assistant':
                                    print('模型', end='', flush=True)
                                elif current_role == 'system':
                                    print('系统', end='', flush=True)
                                elif current_role == 'tool':
                                    print('工具', end='', flush=True)
                                elif current_role == 'error':
                                    print('错误', end='', flush=True)
                                else:
                                    print('未知', end='', flush=True)
                                last_role = current_role
                            print(response_data['message']['content'], end='', flush=True)

                    response_data = agent.run(session_data, stream_func=print_msg)
                    print() # 换行
                    for message in response_data['messages']:
                        session_data['messages'].append(message)
                else:
                    # 非流式处理模式
                    agent_response = agent.run(session_data)
                    if not agent_response:
                        raise Exception("无法取得智能体返回值")
                    for response in agent_response['messages']:
                        if response['role'] == 'assistant':
                            print('模型', end='')
                        elif response['role'] == 'system':
                            print('系统', end='')
                        elif response['role'] == 'tool':
                            print('工具', end='')
                        elif response['role'] == 'error':
                            print('错误', end='')
                        else:
                            print('未知', end='')
                        print(response['content'])
                        session_data['messages'].append(response)
        except KeyboardInterrupt:
            print("\n系统退出客户端")
        except Exception as e:
            print(f"错误客户端出错: {str(e)}")