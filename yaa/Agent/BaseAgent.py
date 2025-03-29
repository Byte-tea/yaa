# from ..LLM_API.BaseAPI import BaseAPI
from ..LLM_API.OpenAI import OpenAI_API

class BaseAgent:
    """智能体基类"""
    def Agent(session_data):
        """智能体主处理函数
        
        参数:
            session_data (dict): 补全后的会话数据
            
        返回:
            response_data (dict): 加入智能体信息的会话数据
        """
        try:
            # 调用大模型API
            # response_data = BaseAPI.request(session_data)
            response_data = OpenAI_API.request(session_data)
            
            return response_data
            
        except Exception as e:
            # 错误处理
            session_data['messages'].append({
                "role": "system",
                "content": f'处理请求时出错: {str(e)}'
            })
            return session_data
