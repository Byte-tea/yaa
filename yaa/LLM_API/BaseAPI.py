class BaseAPI:
    def request(session_data):
        # 添加系统回复消息
        session_data['messages'].append({
            "role": "system",
            "content": "您好，此为 yaa 的系统回复。"
        })

        # 构建响应数据
        # response_data = {
        #     'id': session_data['id'],
        #     'title': session_data.get('title', ''),
        #     'start_time': session_data.get('start_time', ''),
        #     'finish_reason': llm_response.get('finish_reason', 'completed'),
        #     'messages': [
        #         {
        #             'role': 'assistant',
        #             'content': llm_response.get('content', '')
        #         }
        #     ],
        #     'usage': llm_response.get('usage', {
        #         'prompt_tokens': 0,
        #         'completion_tokens': 0,
        #         'total_tokens': 0
        #     })
        # }

        return session_data