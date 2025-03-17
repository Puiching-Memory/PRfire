import requests

port = 1234

url = f"http://localhost:{port}/v1/chat/completions"

data = {
    "model": "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
    "messages": [{"role": "user", "content": "从生理学与人工智能研究的视角，思考人类思维的本质与未来"}],
}

response = requests.post(url, json=data)
print(response.json())