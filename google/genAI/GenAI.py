from google import genai

# 官方文档
# https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn

# 旧版 SDK 会隐式处理 API 客户端对象。在新 SDK 中，您可以创建 API 客户端并使用它调用 API。请注意，无论是哪种情况，如果您未将 API 密钥传递给客户端，SDK 都会从 GOOGLE_API_KEY 环境变量中提取 API 密钥。
# client = genai.Client()
# Set the API key using the GOOGLE_API_KEY env var.
# export GOOGLE_API_KEY="YOUR_API_KEY"
# export GOOGLE_API_KEY="AIzaSyCY0pgtmhJbisYENnNgWzd0m_u5vKdiB8U"
# Alternatively, you could set the API key explicitly:
client = genai.Client(api_key="AIzaSyCY0pgtmhJbisYENnNgWzd0m_u5vKdiB8U")

# 生成内容
# 新版 SDK 通过 Client 对象提供对所有 API 方法的访问权限。除了一些有状态的特殊情况（chat 和实时 API session）外，这些都是无状态函数。为了实用性和统一性，返回的对象是 pydantic 类。
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='Tell me a story in 300 words.'
)
print(response)
print(response.model_dump_json(
    exclude_none=True, indent=4
))
