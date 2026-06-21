# 文件名: aliChatStream.py
# 用途: 基于阿里云千问的流式输出问答机器人
# 使用方法: python aliChatStream.py

import os
import asyncio
from openai import AsyncOpenAI


class AliChatStream:
    """阿里云千问流式问答机器人 - 简单版"""

    def __init__(self):
        """初始化"""
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")

        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

    async def ask(self, question: str):
        """
        问答方法 - 流式输出

        参数:
            question: 你的问题
        """
        print(f"\n你的问题: {question}\n")
        print("AI回答: ", end="", flush=True)

        try:
            # 调用AI，流式输出
            stream = await self.client.chat.completions.create(
                model="qwen3.5-plus",
                messages=[{"role": "user", "content": question}],
                stream=True,
            )

            # 逐字输出
            async for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    if chunk.choices[0].delta.content:
                        print(chunk.choices[0].delta.content, end="", flush=True)

            print("\n" + "=" * 60 + "\n")

        except Exception as e:
            print(f"\n错误: {str(e)}\n")

    def run(self):
        """运行交互式问答"""
        print("=" * 60)
        print("阿里云千问 - 流式问答机器人")
        print("=" * 60)
        print("直接输入你的问题，AI会流式回答你")
        print("输入 'exit' 退出")
        print("=" * 60 + "\n")

        while True:
            try:
                question = input("请输入问题: ").strip()

                if not question:
                    continue

                if question.lower() in ["exit", "quit", "退出"]:
                    print("\n再见！\n")
                    break

                # 调用AI回答
                asyncio.run(self.ask(question))

            except KeyboardInterrupt:
                print("\n\n再见！\n")
                break
            except Exception as e:
                print(f"\n错误: {str(e)}\n")


if __name__ == "__main__":
    bot = AliChatStream()
    bot.run()
