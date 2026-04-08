# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI

client = OpenAI(
    # os 这里获取的是环境变量的 api_key
    api_key=os.environ.get('AI_DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         # {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": "你好，你是谁"},
#     ],
#     stream=False
# )
# print(response.choices[0].message.content)


# 流式输出
stream_response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "你好，你是谁"}
    ],
    stream=True   # 开启流式输出
)

# 处理流式响应
for chunk in stream_response:
    # 每个 chunk 中可能有多个 choices，通常只有一个
    if chunk.choices and len(chunk.choices) > 0:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)  # 实时打印不换行
print()