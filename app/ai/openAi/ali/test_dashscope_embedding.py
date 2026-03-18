# 文件名: test_dashscope_embedding.py
# 用途: 独立测试阿里千问 DashScope 的 embedding 接口
# 使用方法: python test_dashscope_embedding.py

import os
import asyncio
from typing import List, Optional
from openai import AsyncOpenAI


class DashScopeEmbeddingTester:
    """
    阿里 DashScope embedding 接口测试类
    支持同步/异步调用，打印向量维度、长度、预览值
    """

    def __init__(
            self,
            api_key: Optional[str] = None,
            base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1",
            default_model: str = "multimodal-embedding-v1",
    ):
        """
        初始化测试类

        参数:
            api_key: DashScope API Key（默认从环境变量 DASHSCOPE_API_KEY 读取）
            base_url: DashScope OpenAI 兼容地址
            default_model: 默认 embedding 模型（text-embedding-v3 最常用）
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.base_url = base_url
        self.default_model = default_model

        if not self.api_key:
            raise ValueError(
                "请设置环境变量 DASHSCOPE_API_KEY，或在初始化时传入 api_key 参数\n"
                "示例: export DASHSCOPE_API_KEY='sk-xxxx你的key'"
            )

        print(f"[1 初始化] API Key: {self.api_key[:6]}...{self.api_key[-4:]}")
        print(f"[2 初始化] Base URL: {self.base_url}")
        print(f"[3 初始化] 模型: {self.default_model}\n")

        # 创建兼容 OpenAI 的异步客户端
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    async def embed(self, texts: List[str], model: Optional[str] = None) -> List[List[float]]:
        """
        异步调用 embedding 接口

        参数:
            texts: 要向量化的一组文本（可以是 1 条或多条）
            model: 指定模型（默认使用初始化时的模型）

        返回:
            List[List[float]]: 每个文本对应的 embedding 向量
        """
        model = model or self.default_model

        try:
            print(f"[请求] 调用 embedding 模型: {model}")
            print(f"[输入文本数量] {len(texts)}")
            print(f"[第一条文本预览] {texts[0][:50]}{'...' if len(texts[0]) > 50 else ''}\n")

            response = await self.client.embeddings.create(
                model=model,
                input=texts,
            )

            embeddings = [item.embedding for item in response.data]

            print(f"[成功] 返回向量数量: {len(embeddings)}")
            print(f"[向量维度] {len(embeddings[0])}")
            print(f"[第一个向量前5个数值] {embeddings[0][:5]} ...\n")

            return embeddings

        except Exception as e:
            print(f"[失败] embedding 调用报错: {str(e)}")
            raise

    def test(self, texts: Optional[List[str]] = None):
        """
        同步测试方法，方便直接运行

        参数:
            texts: 测试用的文本列表（默认提供几个示例）
        """
        if not texts:
            texts = [
                "这是一个测试句子，用于验证阿里千问 embedding 接口是否正常。",
                "Python 是一种非常流行的编程语言，广泛应用于人工智能和数据科学领域。"
            ]

        print("=" * 60)
        print("开始测试 DashScope embedding 接口...")
        print("=" * 60 + "\n")

        loop = asyncio.get_event_loop()

        try:
            embeddings = loop.run_until_complete(self.embed(texts))
            print("测试成功！所有文本均成功向量化。")
        except Exception as e:
            print("测试失败，请检查 API Key、余额或网络。")
            print(f"错误详情: {str(e)}")


# 直接运行测试
if __name__ == "__main__":
    tester = DashScopeEmbeddingTester()
    tester.test()