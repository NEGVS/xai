#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import asyncio
import io

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.ai.openAi.ali.aliChatStream import AliChatStream


async def handle_question(bot: AliChatStream, question: str):
    """处理用户问题并输出AI回答"""
    print(f"\n你的问题: {question}\n")
    print("AI回答: ", end="", flush=True)

    try:
        # 调用AI，流式输出
        stream = await bot.client.chat.completions.create(
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


def main():
    """主函数 - 启动AI问答CLI"""
    print("=" * 60)
    print("AI Agent CLI - 基于阿里云千问")
    print("=" * 60)
    print("输入你的问题，AI会流式回答")
    print("输入 'exit' 或 'quit' 退出")
    print("=" * 60 + "\n")

    # 初始化AI机器人
    try:
        bot = AliChatStream()
    except ValueError as e:
        print(f"初始化失败: {e}")
        print("请确保已设置 DASHSCOPE_API_KEY 环境变量")
        return

    while True:
        try:
            msg = input(">>> ").strip()

            if not msg:
                continue

            if msg.lower() in ["exit", "quit", "退出"]:
                print("\nBye\n")
                break

            # 调用AI回答
            asyncio.run(handle_question(bot, msg))

        except KeyboardInterrupt:
            print("\n\nBye\n")
            break
        except EOFError:
            print("\nBye\n")
            break
        except Exception as e:
            print(f"\n错误: {str(e)}\n")


if __name__ == "__main__":
    main()