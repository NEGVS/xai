from google import genai
from google.genai import types
import os

# 从环境变量获取API key
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("请设置 GOOGLE_API_KEY 或 GEMINI_API_KEY 环境变量")

client = genai.Client(api_key=api_key)
# client = genai.Client()

# 1-只能问答，思考，不思考
response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how computer works  ", config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0)  # Disables thinking
    ),
)


print(response.text)
