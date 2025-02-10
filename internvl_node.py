from openai import OpenAI
from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage, HumanMessage


def chat_with_internvl(message: list):
    message = conver_langchain(message)
    print(message)
    client = OpenAI(api_key="YOUR_API_KEY", base_url="http://127.0.0.1:23333/v1")
    model_name = client.models.list().data[0].id
    response = client.chat.completions.create(
        model=model_name,
        messages=message,
        temperature=0.8,
        top_p=0.8,
    )

    return response


def conver_langchain(message: list) -> list:
    converted_message = []
    for i in message:
        if type(i) == HumanMessage:
            role = "user"
            i = i.content
            # 判断是否有图片
            print(i[1]["image_url"])
            if (
                i[1]["image_url"]
                == "data:image/jpeg;base64,None"
            ):
                content = [
                    {"type": "text", "text": i[0]["content"]},
                ]
            else:
                content = [
                    {"type": "text", "text": i[0]["content"]},
                    {"type": "image_url", "image_url": i[1]["image_url"]},
                ]
        elif type(i) == AIMessage:
            i = i.content
            role = "assistant"
            content = [
                {"type": "text", "text": i[0]["content"]},
            ]

        converted_message.append(
            {
                "role": role,
                "content": content,
            }
        )

    return converted_message
