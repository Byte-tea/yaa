class API:
    def request(session_data):
        # 添加系统回复消息
        session_data['messages'].append({
            "role": "system",
            "content": "您好，此为 yaa 的系统回复。"
        })

        return session_data