from yaa.Tools.BaseTool import Tool as OldTool
from yaa.Stream.StreamTools import StreamTools as st

class Tool(OldTool):
    '''完成会话
    大模型使用时：
        大模型的回答包含：<完成会话>\n<理由>（对任务完成的总结）</理由>\n</完成会话>
    '''
    ToolInfo = {
        "id": "finish",
        "name": "完成会话",
        "description": "如果所有的任务和子任务都已经完成，使用这个工具结束会话。",
        "parameters": {
            "properties": [
                {
                    "name": "理由",
                    "type": "string",
                    "description": "对任务完成的总结"
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
            status = '已完成'
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