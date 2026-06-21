# 文件名: aliChat.py
# 用途: 基于阿里云千问的普通输出问答机器人
# 使用方法: python aliChat.py

import os
import asyncio
from openai import AsyncOpenAI


class AliChat:
    """阿里云千问普通问答机器人 - 简单版，updating skeletons """

    def __init__(self):
        """初始化"""
        print('初始化')
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")

        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

    async def ask(self, question: str):
        """
        问答方法 - 普通输出（一次性显示完整答案）

        参数:
            question: 你的问题
        """
        print(f"\n你的问题: {question}\n")
        print("AI正在思考...\n")

        try:
            # 调用AI
            response = await self.client.chat.completions.create(
                model="qwen3.5-plus",
                messages=[{"role": "user", "content": question}],
            )

            # 获取完整回答
            answer = response.choices[0].message.content

            # 一次性输出
            print(f"AI回答:\n{answer}\n")
            print("=" * 60 + "\n")

        except Exception as e:
            print(f"\n错误: {str(e)}\n")

    def run(self):
        """运行交互式问答"""
        print("=" * 60)
        print("阿里云千问 - 问答机器人")
        print("=" * 60)
        print("直接输入你的问题，AI会回答你")
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
    bot = AliChat()
    bot.run()
