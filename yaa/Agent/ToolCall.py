import importlib

from yaa.LLM_API.OpenAI import API
from yaa.PromptGen.PromptGenerater import PromptGenerater
from yaa.Agent.BaseAgent import Agent as OutdatedAgent
from yaa.Stream.StreamTools import StreamTools as st
import yaa.Tools as tools

class Agent(OutdatedAgent):
    """工具调用智能体"""

    @classmethod
    def tool_call(self, session_data, stream_tools, il=importlib, stream_func=None):
        '''工具调用处理
        如果 session_data['messages'] 以角色为 assistant 的消息结尾，检测是否存在工具调用，
        如果存在，检查工具调用是否被允许，如果允许，则调用工具，并返回结果，否则返回错误信息。
        '''
        tool_called = False

        # 当角色为 assistant 时，检测是否存在工具调用
        if session_data['messages'][-1]['role'] == 'assistant':
            last_msg = session_data['messages'][-1]['content']
            for tool_name in tools.__all__:
                tool = il.import_module('yaa.Tools.' + tool_name).Tool
                tool_start = f'<{tool.ToolInfo["name"]}>'
                tool_end = f'</{tool.ToolInfo["name"]}>'
                if tool_start in last_msg and tool_end in last_msg:
                    tool_called = True
                    session_data = tool.use(session_data, stream_func)
                    break

            if not tool_called:
                role = 'error'
                content = "<警告>请至少调用一个工具！</警告>"
                stream_tools.update_stream(
                    content,
                    session_data,
                    role=role,
                    stream_func=stream_func
                )
                session_data['messages'].append({
                    "role": role,
                    "content": content
                })

        return session_data

    def run(self, session_data, stream_func=None):
        """智能体主处理函数
        
        参数:
            session_data (dict): 补全后的会话数据
            stream_func (function): 流式传输回调函数
            
        返回:
            dict: 格式化后的智能体回复数据
        """

        try:
            # 补全配置
            from yaa.Config.Config import Config
            session_data = Config.merge_config(session_data)
            
            # 初始化各类
            stream_tools = st(session_data)
            pg = PromptGenerater()
            api = API()
            il = importlib
            agent = self

            while session_data['status'] == '进行中':

                print('循环开始………………………………………………………………………………………………………………')

                # 格式化用户消息并附上提示词
                session_data = pg.PromptGenerate(session_data, stream_func)

                print('测试：' + str(session_data['messages']))

                # 调用大模型 API
                session_data = api.request(session_data, stream_func)

                # 处理工具调用
                session_data = agent.tool_call(session_data, stream_tools, il, stream_func)

            stream_tools.end_stream()
            return self.prase_response(session_data)

        except Exception as e:
            from yaa.Error.ErrorHandler import ErrorHandler as eh
            return eh.return_error_msg(session_data=session_data, error=e, task_name='智能体', stream_func=stream_func)