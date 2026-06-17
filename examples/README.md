# AI Agent 示例集合

这个目录包含了三个专业的 AI Agent 示例，从简单到复杂，帮助你快速上手 AI Agent 开发。

## 📚 示例列表

### 1. Simple Agent (`simple_agent.py`)
**难度**: ⭐️ 入门级

基础的对话型 AI Agent，展示：
- OpenAI API 的基本使用
- 对话历史管理
- 错误处理

**适合**: 刚接触 AI Agent 开发的初学者

### 2. Advanced Agent (`advanced_agent.py`)
**难度**: ⭐️⭐️⭐️ 中级

使用 LangChain 构建的高级 Agent，展示：
- LangChain Agent 架构
- 自定义工具（计算器、天气查询、知识搜索）
- 工具选择和调用
- 结构化提示工程

**适合**: 想要构建能使用工具的 Agent

### 3. RAG Agent (`rag_agent.py`)
**难度**: ⭐️⭐️⭐️⭐️ 高级

检索增强生成 Agent，展示：
- 文档加载和分割
- 向量存储（ChromaDB）
- 相似度检索
- 基于文档的问答

**适合**: 需要 Agent 能回答特定领域知识的场景

## 🚀 快速开始

### 前置条件

1. **配置环境变量**
   ```bash
   cp ../.env.example ../.env
   # 编辑 .env 文件，填入你的 OPENAI_API_KEY
   ```

2. **安装依赖**（如果还没安装）
   ```bash
   uv sync
   ```

### 运行示例

```bash
# 1. Simple Agent
uv run python examples/simple_agent.py

# 2. Advanced Agent
uv run python examples/advanced_agent.py

# 3. RAG Agent
uv run python examples/rag_agent.py
```

## 📖 详细说明

### Simple Agent

最基础的 Agent 实现，直接使用 OpenAI API：

```python
from examples.simple_agent import SimpleAgent

# 创建 agent
agent = SimpleAgent(
    model="gpt-3.5-turbo",
    system_prompt="You are a helpful assistant."
)

# 对话
response = agent.chat("Hello!")
print(response)

# 重置对话
agent.reset_conversation()
```

**核心功能**:
- ✅ 基础对话
- ✅ 历史记录
- ✅ 自定义系统提示词

### Advanced Agent

使用 LangChain 的 Agent，可以调用工具：

```python
from examples.advanced_agent import AdvancedAgent

# 创建 agent
agent = AdvancedAgent(verbose=True)

# Agent 会自动选择合适的工具
response = agent.run("计算 100 * 25")
# Agent 会使用 Calculator 工具

response = agent.run("北京的天气怎么样？")
# Agent 会使用 Weather 工具
```

**核心功能**:
- ✅ 工具调用
- ✅ 自动工具选择
- ✅ 多轮对话
- ✅ 错误处理

**自定义工具**:
```python
from langchain.tools import Tool

def my_custom_tool(input: str) -> str:
    # 你的工具逻辑
    return f"处理结果: {input}"

tool = Tool(
    name="MyTool",
    func=my_custom_tool,
    description="这个工具的用途描述"
)

# 添加到 agent.tools 列表
```

### RAG Agent

检索增强生成，基于文档回答问题：

```python
from examples.rag_agent import RAGAgent

# 创建 RAG agent
agent = RAGAgent()

# 添加文档
documents = [
    "你的文档内容 1",
    "你的文档内容 2",
]
agent.add_documents(documents)

# 查询
result = agent.query("关于文档的问题")
print(result["answer"])
print(result["sources"])  # 查看引用来源
```

**核心功能**:
- ✅ 文档向量化
- ✅ 相似度搜索
- ✅ 上下文注入
- ✅ 来源追踪

**使用场景**:
- 📄 企业知识库问答
- 📚 文档分析
- 🔍 内容检索
- 💼 客服机器人

## 🛠️ 自定义和扩展

### 添加新的工具

在 `advanced_agent.py` 中添加：

```python
def your_tool_function(input: str) -> str:
    # 实现你的工具逻辑
    return result

# 在 AdvancedAgent.__init__ 中添加
Tool(
    name="YourTool",
    func=your_tool_function,
    description="工具描述（帮助 Agent 决定何时使用）"
)
```

### 更换模型

所有示例都支持切换模型：

```python
# 使用 GPT-4
agent = SimpleAgent(model="gpt-4")
agent = AdvancedAgent(model="gpt-4")
agent = RAGAgent(model="gpt-4")

# 使用 GPT-4 Turbo
agent = SimpleAgent(model="gpt-4-turbo-preview")
```

### 连接外部 API

修改工具函数以调用实际 API：

```python
import requests

def get_weather(city: str) -> str:
    # 调用真实的天气 API
    api_key = os.getenv("WEATHER_API_KEY")
    response = requests.get(
        f"https://api.weather.com/v1/current?city={city}&apikey={api_key}"
    )
    return response.json()
```

## 🧪 测试

每个示例都包含内置的测试函数。你也可以创建单元测试：

```bash
# 创建测试文件
# tests/test_agents.py

uv run pytest tests/
```

## 📊 性能优化建议

1. **使用流式输出**（适用于长回复）
   ```python
   for chunk in client.chat.completions.create(
       model="gpt-3.5-turbo",
       messages=messages,
       stream=True
   ):
       print(chunk.choices[0].delta.content, end="")
   ```

2. **缓存嵌入向量**（RAG Agent）
   - 使用持久化存储
   - 避免重复计算

3. **批量处理**
   - 一次处理多个查询
   - 减少 API 调用次数

## 🐛 常见问题

### Q: OpenAI API 调用失败
A: 检查：
- `.env` 文件中的 `OPENAI_API_KEY` 是否正确
- API 账户是否有余额
- 网络连接是否正常

### Q: ChromaDB 报错
A: 确保安装了 chromadb：
```bash
uv add chromadb
```

### Q: 工具没有被调用
A: 检查：
- 工具的 `description` 是否清晰
- 问题是否明确需要该工具
- 尝试更明确的提示词

## 🎓 学习资源

- [OpenAI API 文档](https://platform.openai.com/docs)
- [LangChain 文档](https://python.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [RAG 技术详解](https://arxiv.org/abs/2005.11401)

## 💡 下一步

1. **尝试运行所有三个示例**
2. **修改系统提示词，观察行为变化**
3. **添加自己的工具**
4. **连接真实的数据源（数据库、API）**
5. **构建完整的应用**

## 🤝 贡献

欢迎改进这些示例！如果你有更好的实现或新的示例想法，请提交 PR。

---

Happy Coding! 🚀
