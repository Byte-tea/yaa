from yaa.Stream.StreamTools import StreamTools as st

class Tool:
    '''再度思考
    大模型使用时：
        大模型的回答包含：<再度思考>\n<理由>（调用这个工具的理由）</理由>\n</再度思考>
        需要用户输入包含：<再度思考>\n<授权>（true 或 false）</授权>\n<反馈>（可选，用户对自己决策的说明）</反馈>\n</再度思考>
    '''
    ToolInfo = {
        "id": "base_tool",
        "name": "再度思考",
        "description": "将当前的对话历史再次输入到模型中，让模型继续思考更多的可能性。适合在模型单次达到输出量限制时使用。",
        "parameters": {
            "properties": [
                {
                    "name": "理由",
                    "type": "string",
                    "description": "调用这个工具的理由"
                }
            ],
            "required": ["理由"]
        },
        "feedback": {
            "properties": [
                {
                    "name": "授权",
                    "type": "bool",
                    "description": "用户是否批准本次工具调用"
                },
                {
                    "name": "反馈",
                    "type": "string",
                    "description": "用户对自己决策的说明"
                }
            ],
            "required": ["授权"]
        }
    }

    @classmethod
    def use(cls, session_data, stream_func=None):
        stream_tools = st(session_data)
        name = cls.ToolInfo['name']
        role = 'tool'

        # 验证权限
        if session_data['config']['tool'][cls.ToolInfo['id']]['auto_approve'] == True:
            tool_content = f'[{name}]执行成功。'
            status = '进行中'
        else:
            tool_content = None
            status = '已中断'

        # 推送流式数据
        stream_tools.update_stream(
            tool_content,
            session_data,
            role=role,
            status=status,
            stream_func=stream_func
        )

        if tool_content is not None:
            session_data['messages'].append({
                "role": role,
                "content": tool_content
            })
        session_data['status'] = status
        return session_data
