from ..LLM_API.BaseAPI import BaseAPI

class BaseAgent:
    """智能体基类"""
    def Agent(session_data):
        """智能体主处理函数
        
        参数:
            session_data (dict): 补全后的会话数据
            
        返回:
            dict: 格式化后的响应数据，包含:
                - id: 会话ID
                - title: 会话标题
                - start_time: 开始时间
                - finish_reason: 结束原因
                - messages: 消息列表
                - usage: API使用情况
        """
        try:
            # 调用大模型API
            response_data = BaseAPI.request(session_data)
            
            return response_data
            
        except Exception as e:
            # 错误处理
            session_data['messages'].append({
                "role": "system",
                "content": f'处理请求时出错: {str(e)}'
            })
            return session_data
