# 第一步：导入和设置
from openai import AsyncOpenAI
from nano_graphrag import GraphRAG, QueryParam
import os

# 设置你的OpenAI
# API Key，这是必须的，因为默认用GPT来提取实体和关系--# 把"sk-xxxxxxx"这个值存入名为OPENAI_API_KEY的环境变量中，已经存了的不需要
# os.environ["OPENAI_API_KEY"] = "你的-api-key-here"

# 创建兼容 OpenAI 的客户端
dashscope_client = AsyncOpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'

)


# 自定义 LLM 函数（已过滤非法参数）
async def qwen_llm_func(prompt: str, **kwargs):
    allowed_params = [
        "model", "messages", "temperature", "max_tokens", "top_p",
        "frequency_penalty", "presence_penalty", "stop", "stream",
        "n", "best_of", "logit_bias"
    ]
    clean_kwargs = {k: v for k, v in kwargs.items() if k in allowed_params}

    messages = [{"role": "user", "content": prompt}]

    client = AsyncOpenAI(
        api_key=os.environ["DASHSCOPE_API_KEY"],
        base_url=os.environ["OPENAI_BASE_URL"]
    )

    try:
        resp = await client.chat.completions.create(
            model="qwen-max",
            messages=messages,
            temperature=0.3,
            max_tokens=2048,
            **clean_kwargs
        )
        return resp.choices[0].message.content
    except Exception as e:
        print(f"qwen-max 失败: {e}，回退到 qwen3.5-plus")
        resp = await client.chat.completions.create(
            model="qwen3.5-plus",
            messages=messages,
            temperature=0.3,
            max_tokens=2048,
            **clean_kwargs
        )
        return resp.choices[0].message.content



# 自定义 LLM 调用函数（支持 fallback：先 qwen-max，失败再 qwen3.5-plus）
async def qwen_llm_func_B(prompt: str, **kwargs):
    try:
        # 优先 qwen-max
        resp = await dashscope_client.chat.completions.create(
            model="qwen3.5-plus",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2048,
            **kwargs
        )
        print('qwen3.5-plus 使用成功')
        return resp.choices[0].message.content
    except Exception as e:
        print(f"qwen-max 失败: {e}，回退到 qwen3.5-plus")
        # fallback 到 qwen3.5-plus
        resp = await dashscope_client.chat.completions.create(
            model="qwen3.5-plus",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2048,
            **kwargs
        )
        print("回退到 qwen3.5-plus--end")
        print(resp.choices[0].message.content)
        return resp.choices[0].message.content
print("-----1")

always_create_working_dir = True
# 确保目录不存在时会自动创建
graph_rag = GraphRAG(working_dir="my_first_graphrag",
                     # llm_model_func=qwen_llm_func, # 关键：传入自定义函数
                     best_model_func=qwen_llm_func,  # 关键：传入自定义函数
                     always_create_working_dir=True)
# llm_model_list = ["qwen-max", "qwen3.5-plus"],
print("-----2")

# 第三步：喂给它一些知识
with open("product.txt", "r", encoding="utf-8") as f:
    print('----喂给它一些知识')
    product_description = f.read()
print("-----3")

# 插入文本，内部会自动完成分块、实体关系提取、图谱构建等一系列操作
graph_rag.insert(product_description)
print("知识插入完成！开始构建图谱...")

# 第四步：提问！
# 全局查询：在整个知识图谱中寻找主题和关联
global_answer = graph_rag.query("这个文档里主要有哪些人物？")
print("【全局查询结果】")
print(global_answer)

# 局部查询：在相关的子图（社区）内进行更聚焦的搜索
local_answer = graph_rag.query("谁就职在实验室？哪个实验室？", param=QueryParam(mode="local"))
print("\n【局部查询结果】")
print(local_answer)