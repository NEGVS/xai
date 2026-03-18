# 文件名: test_qwen_api.py
# 用途: 独立测试阿里千问 (DashScope) OpenAI 兼容接口
# 使用方法: python test_qwen_api.py

import os
import asyncio
from openai import AsyncOpenAI
from typing import Optional, List, Dict


class QwenTester:
    """
    阿里千问 DashScope 接口测试类
    支持同步/异步调用，自动 fallback 模型，打印详细调试信息
    """

    def __init__(
            self,
            api_key: Optional[str] = None,
            base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1",
            default_model: str = "qwen3.5-plus",
            fallback_models: List[str] = ["qwen3.5-plus", "qwen-turbo"],
    ):
        """
        初始化测试类

        参数:
            api_key: DashScope API Key (如果不传，会从环境变量 OPENAI_API_KEY 读取)
            base_url: DashScope 兼容模式地址（默认即可）
            default_model: 首选模型
            fallback_models: 失败时依次尝试的备用模型
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.base_url = base_url
        self.default_model = default_model
        self.fallback_models = fallback_models

        if not self.api_key:
            raise ValueError("请设置 OPENAI_API_KEY 环境变量，或在初始化时传入 api_key 参数")

        print(f"[1 初始化] 使用 API Key: {self.api_key[:6]}...{self.api_key[-4:]}")
        print(f"[2 初始化] Base URL: {self.base_url}")
        print(f"[3 初始化] 首选模型: {self.default_model}")
        print(f"[4 初始化] 备用模型: {self.fallback_models}")

        # 创建兼容 OpenAI 的异步客户端
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    async def chat(
            self,
            prompt: str,
            model: Optional[str] = None,
            temperature: float = 0.7,
            max_tokens: int = 2048,
            **kwargs
    ) -> str:
        """
        异步调用聊天完成接口，支持 fallback

        返回: 模型生成的文本内容
        """
        model = model or self.default_model
        messages = [{"role": "user", "content": prompt}]

        models_to_try = [model] + self.fallback_models

        for attempt_model in models_to_try:
            try:
                print(f"\n[5 尝试] 调用模型: {attempt_model}")
                print(f"[6 Prompt 长度] {len(prompt)} 字符")

                response = await self.client.chat.completions.create(
                    model=attempt_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )

                content = response.choices[0].message.content
                print(f"[成功] {attempt_model} 返回，长度: {len(content)}")
                print(f"[返回内容预览] {content[:100]}...")
                return content

            except Exception as e:
                print(f"[失败] {attempt_model} 报错: {str(e)}")
                if attempt_model == models_to_try[-1]:
                    raise RuntimeError(f"所有模型均失败: {str(e)}")
                print("  → 自动回退到下一个模型\n")

    def test(self, prompts: List[str] = None):
        """
        同步测试方法，方便直接运行

        参数:
            prompts: 要测试的 Prompt 列表（默认提供几个示例）
        """
        if not prompts:
            prompts = [
                "你好,请问你可以进行embedding吗？"
            ]

        print("\n" + "=" * 60)
        print("----开始测试阿里千问接口...")
        print("=" * 60 + "\n")

        loop = asyncio.get_event_loop()

        for i, prompt in enumerate(prompts, 1):
            print(i)
            print(f"\n测试 Prompt {i}/{len(prompts)}:")
            print("-" * 40)
            print(f"输入: {prompt[:150]}{'...' if len(prompt) > 150 else ''}")
            print("-" * 40)

            try:
                result = loop.run_until_complete(self.chat(prompt))
                print(f"----输出:\n{result}\n")
            except Exception as e:
                print(f"----测试失败: {str(e)}\n")

        print("=" * 60)
        print("测试完成！")


# 直接运行测试
if __name__ == "__main__":
    tester = QwenTester()
    tester.test()
