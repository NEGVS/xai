from google import genai
from google.genai import types

# success use
client = genai.Client(api_key="AIzaSyCY0pgtmhJbisYENnNgWzd0m_u5vKdiB8U")
# client = genai.Client()

# 1-只能问答，思考，不思考
response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how computer works  ", config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0)  # Disables thinking
    ),
)


print(response.text)
