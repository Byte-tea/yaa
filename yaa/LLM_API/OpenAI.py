import http.client
import json
from urllib.parse import urlparse

class OpenAI_API:
    def request(session_data):
        # 获取配置
        provider_config = session_data['config']['llm_api']['provider']
        api_url = provider_config['api_url']
        api_key = provider_config['api_key']
        model_name = provider_config['model_name']
        
        # 解析API URL
        parsed_url = urlparse(api_url)
        host = parsed_url.netloc
        path = parsed_url.path
        
        # 构建请求
        conn = http.client.HTTPSConnection(host)
        payload = json.dumps({
            "model": model_name,
            "messages": session_data['messages'],
            "stream": False
        })
        
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # 发送请求
        conn.request("POST", path, payload, headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        # 添加AI回复到消息列表
        ai_response = data['choices'][0]['message']
        session_data['messages'].append(ai_response)
        
        return session_data