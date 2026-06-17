"""
高级 AI Agent 示例 - 使用 LangChain 和工具

这个示例展示：
- LangChain Agent 架构
- 自定义工具
- 结构化输出
- 错误处理和重试
"""

import os
from typing import List, Optional
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, SystemMessage

# 加载环境变量
load_dotenv()


# ============================================
# 自定义工具
# ============================================

def calculator(expression: str) -> str:
    """
    计算数学表达式

    Args:
        expression: 数学表达式，如 "2 + 2" 或 "10 * 5"

    Returns:
        计算结果
    """
    try:
        result = eval(expression)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"


def get_weather(city: str) -> str:
    """
    获取城市天气（模拟）

    Args:
        city: 城市名称

    Returns:
        天气信息
    """
    # 这是一个模拟函数，实际应该调用天气 API
    weather_data = {
        "北京": "晴天，温度 15°C",
        "上海": "多云，温度 18°C",
        "深圳": "小雨，温度 22°C",
        "广州": "晴天，温度 25°C"
    }

    return weather_data.get(city, f"暂无 {city} 的天气信息")


def search_knowledge(query: str) -> str:
    """
    搜索知识库（模拟）

    Args:
        query: 搜索查询

    Returns:
        搜索结果
    """
    # 这是一个模拟函数，实际应该调用向量数据库
    knowledge = {
        "python": "Python 是一种高级编程语言，广泛用于 Web 开发、数据科学、AI 等领域。",
        "ai": "人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。",
        "langchain": "LangChain 是一个用于开发由语言模型驱动的应用程序的框架。"
    }

    for key, value in knowledge.items():
        if key in query.lower():
            return value

    return f"未找到关于 '{query}' 的信息"


# ============================================
# 高级 Agent 类
# ============================================

class AdvancedAgent:
    """使用 LangChain 的高级 AI Agent"""

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        verbose: bool = True
    ):
        """
        初始化 Agent

        Args:
            model: OpenAI 模型名称
            temperature: 温度参数（0-1，越高越随机）
            verbose: 是否显示详细信息
        """
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # 定义工具
        self.tools = [
            Tool(
                name="Calculator",
                func=calculator,
                description="用于计算数学表达式。输入应该是有效的 Python 数学表达式，如 '2 + 2' 或 '10 * 5'。"
            ),
            Tool(
                name="Weather",
                func=get_weather,
                description="用于获取城市天气信息。输入应该是城市名称，如 '北京' 或 '上海'。"
            ),
            Tool(
                name="KnowledgeSearch",
                func=search_knowledge,
                description="用于搜索知识库。输入应该是搜索查询，如 'Python' 或 'AI'。"
            )
        ]

        # 创建提示模板
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个强大的 AI 助手，可以使用多种工具来帮助用户。

你可以使用以下工具：
- Calculator: 计算数学表达式
- Weather: 查询城市天气
- KnowledgeSearch: 搜索知识库

请根据用户的问题选择合适的工具，并给出清晰、有帮助的回答。
如果不需要使用工具，可以直接回答。"""),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        # 创建 agent
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        # 创建 agent executor
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=verbose,
            handle_parsing_errors=True,
            max_iterations=3
        )

    def run(self, query: str, chat_history: Optional[List] = None) -> str:
        """
        运行 agent

        Args:
            query: 用户查询
            chat_history: 对话历史

        Returns:
            agent 的回复
        """
        try:
            result = self.agent_executor.invoke({
                "input": query,
                "chat_history": chat_history or []
            })
            return result["output"]
        except Exception as e:
            return f"Error: {str(e)}"


# ============================================
# 主函数
# ============================================

def main():
    """演示高级 Agent 的使用"""

    print("=" * 60)
    print("Advanced AI Agent Demo (with LangChain & Tools)")
    print("=" * 60)
    print()

    # 检查 API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found.")
        print("Please set it in your .env file.")
        return

    # 创建 agent
    print("🚀 Initializing Advanced Agent...")
    agent = AdvancedAgent(verbose=True)
    print("✅ Agent ready!")
    print()

    # 测试不同类型的查询
    test_queries = [
        "计算 25 * 4 + 10",
        "北京的天气怎么样？",
        "什么是 Python？",
        "告诉我一个编程笑话"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'=' * 60}")
        print(f"Query {i}: {query}")
        print("-" * 60)

        response = agent.run(query)

        print(f"\n📝 Response:")
        print(response)
        print("=" * 60)

    print("\n✨ Demo completed!")


if __name__ == "__main__":
    main()
