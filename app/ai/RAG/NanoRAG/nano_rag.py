# 第一步：导入和设置
import asyncio
from openai import AsyncOpenAI
from openai import OpenAI
from nano_graphrag import GraphRAG, QueryParam
import os
from typing import List
import time

# ================================
# 第一步: Embedding 客户端（必须同步）
# ================================
embedding_client = OpenAI(
    # 设置你的OpenAI--当前使用的阿里云百炼
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
# ────────────────────────────────────────────────
# 第二步：创建兼容 OpenAI 的客户端（必须 async）
# ────────────────────────────────────────────────
# 创建兼容 OpenAI 的客户端
dashscope_client = AsyncOpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
)

semaphore = asyncio.Semaphore(2)  #  限制并发数
# ────────────────────────────────────────────────
# 第三步：自定义 LLM 函数（对话/推理）（已过滤非法参数）
# ────────────────────────────────────────────────
async def qwen_llm_func(prompt: str, **kwargs):
    async with semaphore:
        allowed_params = [
            "model", "messages", "temperature", "max_tokens", "top_p",
            "frequency_penalty", "presence_penalty", "stop", "stream",
            "n", "best_of", "logit_bias"
        ]
        clean_kwargs = {k: v for k, v in kwargs.items() if k in allowed_params}

        messages = [{"role": "user", "content": prompt}]

        for i in range(3):
            try:
                await asyncio.sleep(0.4)
                # await
                resp = await dashscope_client.chat.completions.create(
                    model="qwen3.5-plus",
                    messages=messages,
                    temperature=0.3,
                    max_tokens=1024,
                    **clean_kwargs
                )
                return resp.choices[0].message.content
            except Exception as e:
                print(f"[LLM错误] 重试{i + 1}: {e}")
                await asyncio.sleep(2 ** i)
        raise Exception("LLM调用失败")



semaphore_embedding = asyncio.Semaphore(1)  #  限制并发数
# ────────────────────────────────────────────────
# todo 第四步：自定义 Embedding 函数（使用 multimodal-embedding-v1）
# ────────────────────────────────────────────────
class QwenEmbedding:
    def __init__(self):
        self.embedding_dim = 1024 # 维度，运行时自动校正
        self.batch_size = 10  # 阿里限制最大10

    """
       必须 async 支持 await
    """
    async def __call__(self, texts: List[str]) -> List[List[float]]:
        async with semaphore_embedding:
            try:
                print(f"[Embedding 调用] 文本数量: {len(texts)} | 第一条预览: {texts[0][:50]}...")
                all_embeddings = []
                # 分批处理（核心修复）--防止超过阿里限制10
                for i in range(0, len(texts), self.batch_size):
                    batch = texts[i:i + self.batch_size]
                    print(f"[Embedding] 批次 {i // self.batch_size + 1}: {len(batch)} 条")
                    await asyncio.sleep(0.2)
                    # 重试机制
                    for retry in range(3):
                        try:
                            # 同步 API → 用线程池
                            response = await asyncio.to_thread(
                                embedding_client.embeddings.create,
                                model="text-embedding-v4",
                                input=batch
                            )

                            break
                        except Exception as e:
                            print(f"[Embedding重试] 第{retry + 1}次失败: {e}")
                            time.sleep(2 ** retry)

                    # if self.embedding_dim is None:
                    #     self.embedding_dim = len(all_embeddings[0])
                    batch_embeddings = [item.embedding for item in response.data]
                    all_embeddings.extend(batch_embeddings)

                # 自动校正维度
                real_dim = len(all_embeddings[0])
                print("----real_dim---")
                print(real_dim)
                if self.embedding_dim != real_dim:
                    print(f"[修正 embedding_dim] {self.embedding_dim} → {real_dim}")
                    self.embedding_dim = real_dim
                print(f"[Embedding完成] 共 {len(all_embeddings)} 条")
                return all_embeddings

            except Exception as e:
                print(f"[Embedding 失败] {str(e)}")
                raise



# ────────────────────────────────────────────────
# 第五步：初始化 GraphRAG
# ────────────────────────────────────────────────
print("-----1--初始化 GraphRAG")

always_create_working_dir = True
graph_rag = GraphRAG(working_dir="my_first_graphrag",
                     best_model_func=qwen_llm_func,  # 关键：传入自定义函数
                     embedding_func=QwenEmbedding(),
                     always_create_working_dir=True,  #确保目录不存在时会自动创建
                     chunk_token_size=300, #（防 token 爆）
                     )
# llm_model_list = ["qwen3.5-plus", "qwen3.5-plus"],
print("-----2--初始化完成")

# ================================
#  6. 加载数据
# ================================
with open("product.txt", "r", encoding="utf-8") as f:
    print('----喂数据---')
    product_description = f.read()

# 插入文本，内部会自动完成分块、实体关系提取、图谱构建等一系列操作
graph_rag.insert(product_description)
print("知识插入完成！开始构建图谱...")

# 第四步：提问！
# 全局查询：在整个知识图谱中寻找主题和关联
global_answer = graph_rag.query("这个文档里主要有哪些人物？")
print("【全局查询结果】")
print(global_answer)

# 局部查询：在相关的子图（社区）内进行更聚焦的搜索
local_answer = graph_rag.query(
    "谁就职在实验室？哪个实验室？",
    param=QueryParam(mode="local")
)
print("\n【局部查询结果】")
print(local_answer)