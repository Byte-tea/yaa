"""智能体默认配置模块

职责：
1. 提供系统默认配置项
2. 管理配置加载优先级（默认配置 < 用户配置 < 运行时配置）
"""

class Config:
    """系统默认配置类"""
    
    # 基础配置
    YAA_CONFIG = {
        'stream': True
    }

    # LLM API 配置
    LLM_API_CONFIG = {
        'provider': {
            'api_url': 'https://api.openai.com/v1/chat/completions',
            'api_key': '',
            'model_name': 'gpt-4',
            'model_type': {
                'is_function_call': False,
                'is_reasoning': False
            },
            'cost_per_ktoken': 0.03,
            'cost_unit': 'USD',
            'max_tokens': 2000,
            'model_settings': {
                'use_custom_temp': False,
                'temperature': 0.7
            }
        },
        'stream': True,
        "request_timeout": 360,
        "interval": 0,
        'retry': {
            'times': 3,
            'delay': 5
        }
    }
    
    # TODO 提示词配置
    PROMPT_CONFIG = {
        'function': 'TODO',
        'system': 'TODO',
        'error': 'TODO：{error}'
    }
    
    # TODO 工具调用配置
    TOOL_CONFIG = {
        'auto_approve': False,
        'timeout': 30,
        'max_memory': '512MB',
        'cpu_threshold': 0.8,
        'interrupt_monitor': True
    }

    @classmethod
    def merge_config(cls, user_config=None):
        """合并用户配置和默认配置
        
        参数:
            user_config (dict): 用户提供的配置字典
            
        返回:
            dict: 合并后的配置字典，保留所有原始字段并合并特定配置项
        """
        if user_config is None:
            user_config = {}
            
        # 保留所有原始字段
        merged_config = user_config.copy()
        
        # 合并特定配置项
        if 'yaa' in user_config:
            merged_config['yaa'] = {**cls.YAA_CONFIG, **user_config['yaa']}
        if 'llm_api' in user_config:
            merged_config['llm_api'] = {**cls.LLM_API_CONFIG, **user_config['llm_api']}
        if 'prompt' in user_config:
            merged_config['prompt'] = {**cls.PROMPT_CONFIG, **user_config['prompt']}
        if 'tool' in user_config:
            merged_config['tool'] = {**cls.TOOL_CONFIG, **user_config['tool']}
            
        return merged_config