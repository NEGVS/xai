import os

from openai import OpenAI

print(os.getenv("DEEPSEEK_API_KEY"))
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a senior assistant, possessing high emotional intelligence and high intelligence"},
        {"role": "user", "content": "My girlfriend said she has her period. What should I do?"},
    ],
    # stream=False
    stream=True
)
# print(response.choices[0].message.content)
# print(response)
# if stream is true
for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end='')
