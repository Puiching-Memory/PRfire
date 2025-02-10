from openai import OpenAI


def chat_with_internvl(description: str, image_url: bytes):
    client = OpenAI(api_key="YOUR_API_KEY", base_url="http://127.0.0.1:23333/v1")
    model_name = client.models.list().data[0].id
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{description}",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"{image_url}",
                        },
                    },
                ],
            }
        ],
        temperature=0.8,
        top_p=0.8,
    )
    #print(response)
    return response
