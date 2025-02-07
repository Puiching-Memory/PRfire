from openai import OpenAI
client = OpenAI(
    api_key='YOUR_API_KEY',
    base_url="http://127.0.0.1:23333/v1"
)
model_name = client.models.list().data[0].id
response = client.chat.completions.create(
  model=model_name,
  messages=[
    #{"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你好"},
  ],
    temperature=0.8,
    top_p=0.8
)
print(response)