import http.client
import json
from urllib.parse import urlparse

from yaa.LLM_API.BaseAPI import API as OutdatedAPI
from yaa.Stream.StreamTools import StreamTools as st

class API(OutdatedAPI):

    def request(self, session_data, stream_func=None):
        # 获取配置
        provider_config = session_data['config']['llm_api']['provider']
        api_url = provider_config['api_url']
        api_key = provider_config['api_key']
        model_name = provider_config['model_name']
        use_stream = session_data['config']['llm_api']['stream']

        # 实例化流式传输工具
        stream_tools = st(session_data)

        # 解析 API URL
        parsed_url = urlparse(api_url)
        host = parsed_url.netloc
        path = parsed_url.path
        
        # 构建请求
        conn = http.client.HTTPSConnection(host)
        payload = json.dumps({
            "model": model_name,
            "messages": session_data['messages'],
            "stream": use_stream
        })
        
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # 发送请求
        conn.request("POST", path, payload, headers)
        res = conn.getresponse()
        
        if use_stream:
            # 流式处理
            buffer = ""
            ai_response = {"role": "assistant", "content": ""}
            
            while True:
                try:
                    chunk = res.read(1024).decode("utf-8", errors="replace")
                    if not chunk:
                        break
                except UnicodeDecodeError:
                    chunk = res.read(1024).decode("utf-8", errors="ignore")
                    if not chunk:
                        break
                    
                buffer += chunk
                lines = buffer.split("\n")
                buffer = lines.pop() # 保存不完整的行
                
                for line in lines:
                    if line.startswith("data: "):
                        data = line[6:].strip()
                        if data == "[DONE]":
                            break

                        try:
                            chunk_data = json.loads(data)
                            if "choices" in chunk_data and chunk_data["choices"]:
                                delta = chunk_data["choices"][0].get("delta", {})
                                if "content" in delta and delta["content"] is not None:
                                    stream_tools.update_stream(
                                        content=delta["content"],
                                        session_data=session_data,
                                        role="assistant",
                                        status='进行中',
                                        stream_func=stream_func
                                    )
                                    current_content = ai_response.get("content", "") or ""
                                    ai_response["content"] = current_content + str(delta["content"])
                        except json.JSONDecodeError:
                            continue
            
            # 添加完整回复到消息列表
            if ai_response.get("content"):  # 只添加有内容的回复
                session_data['messages'].append(ai_response)
            return session_data
        else:
            # 非流式处理
            try:
                response_body = res.read().decode("utf-8")
            except UnicodeDecodeError:
                response_body = res.read().decode("utf-8", errors="replace")
            
            # 检查响应内容是否为JSON
            try:
                data = json.loads(response_body)
            except json.JSONDecodeError:
                raise Exception(f"API 返回非 JSON 响应: {response_body[:200]}...")
                
            # 检查API响应状态
            if res.status != 200:
                error_msg = data.get('error', {}).get('message', '未知错误') if isinstance(data, dict) else response_body[:200]
                raise Exception(f"API 请求失败({res.status}): {error_msg}")
                
            if 'choices' not in data or len(data['choices']) == 0:
                raise Exception("API 返回无效响应: 缺少 choices 字段")
                
            # 添加 AI 回复到消息列表
            ai_response = data['choices'][0]['message']
            session_data['messages'].append(ai_response)
            
            return session_data
