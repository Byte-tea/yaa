import sys
import inspect
from yaa.Stream.StreamTools import StreamTools as st

class ErrorHandler:
    '''错误处理'''
    @staticmethod  # 新增装饰器
    def get_caller_module():
        # 获取当前帧的上一层帧
        frame = sys._getframe().f_back.f_back  # 需要跳过当前函数和直接调用者
        module = inspect.getmodule(frame)
        return module.__name__ if module else None

    def return_error_msg(session_data, error, task_name, stream_func=None):
        """返回错误信息到上层
        session_data: (dict) 当前会话数据
        error: 错误或错误信息
        task_name: (string) 当前任务名称
        """
        role = 'error'
        err_msg = f'在{ErrorHandler.get_caller_module()}的'+ task_name + f'出错：{str(error)}'
        status = '已中断'

        # 流式推送错误信息
        stream_tools = st(session_data)
        stream_tools.update_stream(
            content=err_msg,
            session_data=session_data,
            role=role,
            status=status,
            stream_func=stream_func
        )
        stream_tools.end_stream()

        session_data['messages'].append({
            "role": role,
            "content": err_msg
        })
        session_data['status'] = status
        return session_data
