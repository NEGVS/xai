# AI Agent 开发环境使用指南

## 环境信息

- **包管理器**: uv (现代化、超快速)
- **Python 版本**: >= 3.11
- **项目配置**: pyproject.toml (现代 Python 标准)

## 快速开始

### 1. 激活环境

```bash
# uv 会自动管理虚拟环境，运行命令时自动激活
uv run python main.py
```

### 2. 安装依赖

```bash
# 同步所有依赖（生产环境）
uv sync

# 包含开发工具
uv sync --extra dev

# 包含 AI 工具
uv sync --extra ai-tools

# 安装所有可选依赖
uv sync --all-extras
```

### 3. 添加新包

```bash
# 添加生产依赖
uv add package-name

# 添加开发依赖
uv add --dev pytest

# 添加到特定组
uv add --optional ai-tools autogen
```

### 4. 运行代码

```bash
# 直接运行 Python 脚本
uv run python script.py

# 运行模块
uv run python -m app.main

# 运行测试
uv run pytest

# 启动 Jupyter
uv run jupyter notebook
```

## 开发工具

### 代码格式化 (Ruff)

```bash
# 格式化代码
uv run ruff format .

# 检查代码质量
uv run ruff check .

# 自动修复
uv run ruff check --fix .
```

### 类型检查 (MyPy)

```bash
uv run mypy app/
```

### 测试 (Pytest)

```bash
# 运行所有测试
uv run pytest

# 带覆盖率
uv run pytest --cov

# 运行特定测试
uv run pytest tests/test_agent.py
```

## 项目结构建议

```
xai/
├── app/                    # 应用代码
│   ├── __init__.py
│   ├── agents/            # AI agents
│   ├── tools/             # Agent 工具
│   ├── prompts/           # 提示模板
│   ├── models/            # 数据模型
│   └── utils/             # 工具函数
├── tests/                 # 测试
│   ├── __init__.py
│   ├── test_agents.py
│   └── test_tools.py
├── notebooks/             # Jupyter notebooks
├── data/                  # 数据文件
├── .env                   # 环境变量（不提交）
├── .env.example           # 环境变量模板
├── pyproject.toml         # 项目配置
├── uv.lock               # 锁定依赖版本
└── README.md
```

## 环境变量配置

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 填入你的 API 密钥

3. 在代码中使用：
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

## AI Agent 开发最佳实践

### 1. 结构化提示

```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI agent."),
    ("human", "{input}")
])
```

### 2. 使用工具

```python
from langchain.agents import Tool

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for math calculations"
    )
]
```

### 3. 错误处理

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
async def call_llm(prompt: str):
    # LLM 调用
    pass
```

### 4. 日志记录

```python
from rich.console import Console

console = Console()
console.log("[bold green]Agent started[/bold green]")
```

## 常用命令速查

```bash
# 环境管理
uv sync                    # 同步依赖
uv sync --all-extras       # 安装所有可选依赖
uv add package             # 添加依赖
uv remove package          # 移除依赖
uv pip list                # 列出已安装包

# 运行
uv run python script.py    # 运行脚本
uv run pytest              # 运行测试
uv run ruff format .       # 格式化代码

# 开发
uv run jupyter notebook    # 启动 Jupyter
uv run ipython             # 启动 IPython
```

## VS Code / PyCharm 配置

### VS Code

1. 安装 Python 扩展
2. 选择解释器：
   - Cmd+Shift+P
   - 输入 "Python: Select Interpreter"
   - 选择 `.venv/bin/python`

### PyCharm

1. Settings > Project > Python Interpreter
2. 添加解释器
3. 选择 Virtualenv Environment
4. 选择现有环境：`.venv`

## 性能对比

### uv vs pip 安装速度

- **pip**: ~2-5 分钟
- **conda**: ~5-10 分钟
- **uv**: ~10-30 秒 ⚡

### 为什么选择 uv？

✅ 极快的安装速度
✅ 更准确的依赖解析
✅ 现代化的工作流
✅ 自动虚拟环境管理
✅ 兼容 pip 生态

## 故障排除

### 问题：uv 命令找不到

```bash
# 添加到 PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 问题：依赖冲突

```bash
# 清理并重新安装
rm -rf .venv uv.lock
uv sync
```

### 问题：需要特定 Python 版本

```bash
# uv 可以自动安装和管理 Python 版本
uv python install 3.11
uv venv --python 3.11
```

## 学习资源

- [uv 官方文档](https://docs.astral.sh/uv/)
- [LangChain 文档](https://python.langchain.com/)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [Anthropic API 文档](https://docs.anthropic.com/)

## 下一步

1. ✅ 环境已配置
2. 📝 复制 .env.example 为 .env 并填入 API 密钥
3. 🧪 运行测试：`uv run pytest`
4. 🚀 开始开发你的 AI agent！
