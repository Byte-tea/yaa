class DebugTools:
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
    
    def dprint(self, message, end="\n", flush=False):
        if self.debug_mode:
            print('日志' + message, end=end, flush=flush)