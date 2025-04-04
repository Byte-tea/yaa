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
    def use(cls, session_data):
        if session_data['config']['tool'][cls.ToolInfo['id']]['auto_approve'] == True:
            session_data['messages'].append({
                "role": "tool",
                "content": f"[再度思考]执行成功。"
            })
            session_data['status'] = '进行中'
        else:
            session_data['status'] = '已中断'
        return session_data
