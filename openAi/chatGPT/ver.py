from openai import OpenAI
import os

# 配置你的 API 密钥和模型
# 从系统环境变量中读取
api_key = os.getenv("OPENAI_API_KEY")  # ✅ 从环境变量读取 API Key
model = "text-embedding-3-small"  # 或 text-embedding-3-large
# # 可选：提供默认模型，也从环境变量读取
# model = os.getenv("OPENAI_MODEL", "text-embedding-3-small")


# 初始化 OpenAI Client
client = OpenAI(api_key=api_key)

# 打印验证（只用一次）
print("Loaded API Key (safe):", api_key[:1000])
print("Loaded Model:", model)
try:
    print('Embedding...')
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input="Hello, world!"
    )
    # 获取嵌入向量
    embedding = response.data[0].embedding
    print("Embedding end:/n", embedding)
except Exception as e:
    print(f"其他错误：{e}")
