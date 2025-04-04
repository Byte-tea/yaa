"""大语言模型 API 接口模块"""
from yaa.LLM_API.BaseAPI import API as BaseAPI
from yaa.LLM_API.OpenAI import API

__all__ = [
    "BaseAPI",
    "API"
]