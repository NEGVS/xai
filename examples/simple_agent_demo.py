"""
Simple Agent 测试版本 - 无需 API key 演示

这个版本使用模拟响应，可以在没有 OpenAI API key 的情况下测试代码结构
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class SimpleAgentDemo:
    """简单的 AI Agent 类（演示版）"""

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        system_prompt: Optional[str] = None,
        use_mock: bool = False
    ):
        """
        初始化 Agent

        Args:
            model: OpenAI 模型名称
            system_prompt: 系统提示词
            use_mock: 是否使用模拟响应（用于测试）
        """
        self.model = model
        self.use_mock = use_mock
        self.api_key = os.getenv("OPENAI_API_KEY")
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

        # 如果使用模拟模式或没有 API key
        if self.use_mock or not self.api_key or self.api_key == "your_openai_api_key_here":
            assistant_message = self._mock_response(user_message)
        else:
            # 真实 API 调用
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.api_key)

                response = client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    temperature=0.7,
                    max_tokens=500
                )
                assistant_message = response.choices[0].message.content
            except Exception as e:
                assistant_message = f"Error calling OpenAI API: {str(e)}"

        # 添加到历史
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def _mock_response(self, user_message: str) -> str:
        """生成模拟响应"""
        # 简单的模拟逻辑
        msg_lower = user_message.lower()

        if "hello" in msg_lower or "hi" in msg_lower or "你好" in msg_lower:
            return "Hello! I'm a helpful AI assistant. How can I help you today?"

        elif "python" in msg_lower:
            return """Python is a high-level programming language known for its simplicity and readability.
Here are some key features:
- Easy to learn and use
- Extensive standard library
- Great for web development, data science, and AI
- Large community support

Would you like to know more about any specific aspect of Python?"""

        elif "csv" in msg_lower and "read" in msg_lower:
            return """To read a CSV file in Python, you can use the `pandas` library:

```python
import pandas as pd

# Read CSV file
df = pd.read_csv('file.csv')

# Display first few rows
print(df.head())
```

Or using the built-in `csv` module:

```python
import csv

with open('file.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)
```

Which approach would you like to learn more about?"""

        elif "list" in msg_lower and "tuple" in msg_lower:
            return """Great question! Here are the key differences between lists and tuples in Python:

**Lists:**
- Mutable (can be changed after creation)
- Defined with square brackets: [1, 2, 3]
- Slightly slower
- Use when you need to modify data

**Tuples:**
- Immutable (cannot be changed after creation)
- Defined with parentheses: (1, 2, 3)
- Slightly faster
- Use for fixed data that shouldn't change

Example:
```python
my_list = [1, 2, 3]
my_list[0] = 10  # OK

my_tuple = (1, 2, 3)
my_tuple[0] = 10  # Error! Tuples are immutable
```"""

        else:
            return f"I received your message: '{user_message}'. This is a mock response since no OpenAI API key is configured. To get real AI responses, please add your OPENAI_API_KEY to the .env file."

    def reset_conversation(self):
        """重置对话历史（保留系统提示词）"""
        system_message = self.conversation_history[0]
        self.conversation_history = [system_message]

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.conversation_history


def main():
    """主函数 - 演示如何使用 SimpleAgent"""

    print("=" * 60)
    print("Simple AI Agent Demo")
    print("=" * 60)
    print()

    # 检查 API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  No valid OPENAI_API_KEY found - using MOCK mode")
        print("   To use real OpenAI API, add your key to .env file")
        use_mock = True
    else:
        print("✅ OPENAI_API_KEY found - using REAL API")
        use_mock = False

    print()

    # 创建一个专业的 Python 编程助手
    agent = SimpleAgentDemo(
        model="gpt-3.5-turbo",
        system_prompt=(
            "You are an expert Python programming assistant. "
            "You help developers write clean, efficient, and well-documented code. "
            "Always provide practical examples and explanations."
        ),
        use_mock=use_mock
    )

    print("✅ Agent initialized successfully!")
    print(f"📝 Model: {agent.model}")
    print(f"🎭 Mode: {'MOCK (Demo)' if use_mock else 'REAL (OpenAI API)'}")
    print()

    # 示例对话
    test_messages = [
        "Hello! Can you help me with Python?",
        "How do I read a CSV file in Python?",
        "What's the difference between a list and a tuple?"
    ]

    for i, message in enumerate(test_messages, 1):
        print(f"{'=' * 60}")
        print(f"💬 User: {message}")
        print("-" * 60)

        response = agent.chat(message)
        print(f"🤖 Agent: {response}")
        print()

    # 显示对话历史摘要
    print("=" * 60)
    print("📚 Conversation Summary:")
    print(f"   Total messages: {len(agent.get_conversation_history())}")
    print(f"   User messages: {len([m for m in agent.get_conversation_history() if m['role'] == 'user'])}")
    print(f"   Agent responses: {len([m for m in agent.get_conversation_history() if m['role'] == 'assistant'])}")
    print()
    print("✨ Demo completed!")
    print()

    if use_mock:
        print("💡 Tip: Add your OPENAI_API_KEY to .env file to use real AI responses!")


if __name__ == "__main__":
    main()
