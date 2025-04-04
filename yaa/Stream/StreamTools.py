class StreamTools:
    '''流式工具类，用于处理智能体内部流式数据
    使用之前须实例化，如：
        stream_tools = StreamTools(session_data)
    '''

    def __init__(self, session_data):
        self.session_data = session_data

    def update_stream(self, content, session_data=None, role=None, status=None, stream_func=None):
        '''格式化智能体回复数据
        输入：
            content: 智能体回复内容
            session_data: 会话数据
            role: 角色
            stream_func: 流式推送函数
        '''
        if stream_func is not None:
            if not session_data:
                session_data = self.session_data
            response_data = {
                "id": session_data['id'],
                "object": "chat.completion.chunk",
                "status": status if status else session_data['status'],
                "message": {
                    'role': role if role else session_data['messages'][-1]['role'],
                    'content': content
                }
            }
            stream_func(response_data=response_data)
            return response_data

    # def update_stream(self, content, session_data):
    #     '''格式化智能体回复数据'''
    #     response_data = {
    #         "id": session_data['id'],
    #         "object": "chat.completion.chunk",
    #         "status": session_data['status'],
    #         "message": {
    #             "role": session_data['messages'][-1]['role'],
    #             "content": content
    #         }
    #     }
    #     return f"data: {json.dumps(response_data)}\n\n".encode('utf-8')

    def end_stream(self):
        '''返回流式传输中断'''
        return b"data: [DONE]\n\n"
