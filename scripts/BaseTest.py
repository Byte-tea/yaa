import json
import requests

def main():
    # 定义请求头
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": "YAA-API-KEY yaa"
    }
    
    # 定义请求体
    data = {
        "id": "3ff6bcb1-1dbe-4e04-969c-aa610da0d85f",
        "title": "用于测试的会话",
        "start_time": "2025-03-29 13:35:04",
        "type": "对话",
        "messages": [
            {
                "role": "user",
                "content": "yaa 智能体，你好吗？"
            }
        ],
        "config": {
            "yaa" : {"stream": False},
            "llm_api": {
                "provider": {
                    "api_url": "https://llm.pj568.sbs/v1/chat/completions",
                    "api_key": "PJ568",
                    "model_name": "@cf/qwen/qwen1.5-0.5b-chat",
                    "model_type": {
                        "is_function_call": False,
                        "is_reasoning": False
                    },
                    "cost_per_ktoken": 0.0,
                    "cost_unit": "CNY",
                },
                "stream": False,
            }
        }
    }
    
    # 发送POST请求
    response = requests.post("http://localhost:12345/", headers=headers, data=json.dumps(data))
    
    # 打印响应结果
    print(response.status_code)
    print(response.json())

if __name__ == "__main__":
    main()