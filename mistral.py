import requests

# 設置 Hugging Face 的 access token
access_token = "xxx"
api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

# 設置請求頭
headers = {
    "Authorization": f"Bearer {access_token}"
}

# 定義請求函數
def query(payload):
    response = requests.post(api_url, headers=headers, json=payload, timeout=60)  # 設置較長的超時時間
    return response.json()

# 與模型進行有意義的溝通
def chat_with_model(prompt, max_length=1000, chunk_size=500):
    generated_text = ""
    previous_text = ""
    while len(generated_text) < max_length:
        response = query({
            "inputs": prompt,
            "parameters": {
                "max_length": chunk_size,
                "top_p": 0.9,
                "temperature": 0.7,
                "stop_sequence": "\n"
            }
        })
        if 'generated_text' in response[0]:
            chunk = response[0]['generated_text']
            if chunk == previous_text:
                break  # 停止重複
            generated_text += chunk
            previous_text = chunk
            if len(chunk.strip()) == 0 or len(generated_text) >= max_length:
                break
            prompt += chunk  # 更新 prompt 以包含已生成的文本
        else:
            break
    return generated_text.strip()

# 預先定義好要測試的問題
prompts = [
    "HI,你今天怎麼樣?",
    "pytorch寫一個cnn模型",
    "Can you tell me a story about a brave knight?",
    "What is the capital of France?",
    "Write a poem about the ocean.",
    "What is the meaning of life?",
    "用python寫費波納契數列",
    "再見"
]

# 依次迭代測試問題
for prompt in prompts:
    print(f"User說: {prompt}")
    response = chat_with_model(prompt)
    print(f"Model說: {response}\n")
