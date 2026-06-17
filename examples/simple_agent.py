"""
简单的 AI Agent 示例

这个示例展示了如何创建一个基础的 AI agent，包括：
- 使用 OpenAI API
- 对话历史管理
- 工具调用
- 错误处理
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()


class SimpleAgent:
    """简单的 AI Agent 类"""

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        system_prompt: Optional[str] = None
    ):
        """
        初始化 Agent

        Args:
            model: OpenAI 模型名称
            system_prompt: 系统提示词
        """
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.conversation_history: List[Dict[str, str]] = []

        # 设置系统提示词
        if system_prompt is None:
            system_prompt = "You are a helpful AI assistant."

        self.conversation_history.append({
            "role": "system",
            "content": system_prompt
        })

    def chat(self, user_message: str) -> str:
        """
        与 agent 对话

        Args:
            user_message: 用户消息

        Returns:
            agent 的回复
        """
        # 添加用户消息到历史
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        try:
            # 调用 OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=500
            )

            # 获取助手回复
            assistant_message = response.choices[0].message.content

            # 添加到历史
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except Exception as e:
            error_msg = f"Error calling OpenAI API: {str(e)}"
            print(error_msg)
            return error_msg

    def reset_conversation(self):
        """重置对话历史（保留系统提示词）"""
        system_message = self.conversation_history[0]
        self.conversation_history = [system_message]

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.conversation_history


def main():
    """主函数 - 演示如何使用 SimpleAgent"""

    print("=" * 50)
    print("Simple AI Agent Demo")
    print("=" * 50)
    print()

    # 检查 API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please set it in your .env file.")
        return

    # 创建一个专业的 Python 编程助手
    agent = SimpleAgent(
        model="gpt-3.5-turbo",
        system_prompt=(
            "You are an expert Python programming assistant. "
            "You help developers write clean, efficient, and well-documented code. "
            "Always provide practical examples and explanations."
        )
    )

    print("✅ Agent initialized successfully!")
    print(f"📝 Model: {agent.model}")
    print()

    # 示例对话
    test_messages = [
        "Hello! Can you help me with Python?",
        "How do I read a CSV file in Python?",
        "What's the difference between a list and a tuple?"
    ]

    for i, message in enumerate(test_messages, 1):
        print(f"User: {message}")
        response = agent.chat(message)
        print(f"Agent: {response}")
        print("-" * 50)
        print()

    # 显示对话历史
    print("📚 Conversation History:")
    for msg in agent.get_conversation_history()[1:]:  # 跳过系统消息
        role = msg["role"].capitalize()
        content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
        print(f"{role}: {content}")

    print()
    print("✨ Demo completed!")


if __name__ == "__main__":
    main()
