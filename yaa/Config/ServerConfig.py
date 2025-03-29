"""服务端默认配置模块

职责：
1. 提供服务端相关的默认配置项
"""

class ServerConfig:
    """服务端默认配置类"""
    
    # 基础配置
    YAA_SERVER_CONFIG = {
        'ip': '0.0.0.0',
        'port': 12345,
        'max_connections': 100,
        "max_receive": 1024,
        'timeout': 60
    }

    # 安全验证配置
    SECURITY_CONFIG = {
        'auth_required': True,
        'api_key_header': 'X-API-KEY',
        'rate_limit': '100/1m',
        'max_request_size': '10MB'
    }

    @classmethod
    def merge_config(cls, args_config=None):
        """合并用户配置和默认配置
        
        参数:
            args_config (dict): 服务器运行时参数传入编译的配置字典
            
        返回:
            dict: 合并后的配置字典，参数配置优先于默认配置
        """
        if args_config is None:
            args_config = {}
            
        merged_config = {
            'yaa_server': {**cls.YAA_SERVER_CONFIG, **args_config.get('yaa_server', {})},
            'security': {**cls.SECURITY_CONFIG, **args_config.get('security', {})}
        }
        
        return merged_config