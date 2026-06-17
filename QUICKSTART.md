# 快速开始指南

欢迎使用 XAI AI Agent 开发环境！

## 🎯 5 分钟快速上手

### 第 1 步：环境配置（已完成 ✅）

你的环境已经配置好了：
- ✅ uv 包管理器已安装
- ✅ pyproject.toml 已配置
- ✅ 依赖正在安装中...

### 第 2 步：设置 API Key

```bash
# 编辑 .env 文件
nano .env

# 或使用你喜欢的编辑器
code .env
```

将 `your_openai_api_key_here` 替换为你的真实 OpenAI API key。

**获取 API Key**：https://platform.openai.com/api-keys

### 第 3 步：运行第一个 Agent

```bash
# 运行演示版本（无需 API key）
uv run python examples/simple_agent_demo.py

# 或运行真实版本（需要 API key）
uv run python examples/simple_agent.py
```

## 📁 项目结构

```
xai/
├── examples/              # AI Agent 示例
│   ├── simple_agent_demo.py    # 演示版（无需 API）
│   ├── simple_agent.py         # 基础 Agent
│   ├── advanced_agent.py       # 带工具的 Agent
│   ├── rag_agent.py            # RAG Agent
│   └── README.md               # 示例说明
├── app/                   # 你的应用代码
│   ├── agents/           # Agent 实现
│   ├── tools/            # Agent 工具
│   └── prompts/          # 提示模板
├── tests/                # 测试文件
├── .env                  # 环境变量（不提交）
├── pyproject.toml        # 项目配置
└── UV_COMPLETE_GUIDE.md  # uv 完整指南
```

## 🚀 常用命令

### 运行代码
```bash
# 运行 Python 脚本
uv run python script.py

# 运行测试
uv run pytest

# 启动 Jupyter
uv run jupyter notebook
```

### 管理依赖
```bash
# 添加新包
uv add package-name

# 安装开发依赖
uv sync --extra dev

# 安装所有可选依赖
uv sync --all-extras
```

### 代码质量
```bash
# 格式化代码
uv run ruff format .

# 检查代码
uv run ruff check .

# 自动修复
uv run ruff check --fix .
```

## 🎓 学习路径

### 初学者
1. 阅读 `examples/README.md`
2. 运行 `simple_agent_demo.py`
3. 修改系统提示词，观察变化
4. 尝试添加新的对话逻辑

### 进阶
1. 运行 `advanced_agent.py`
2. 添加自定义工具
3. 连接真实 API（天气、搜索等）
4. 构建多轮对话

### 高级
1. 运行 `rag_agent.py`
2. 添加自己的文档
3. 优化检索策略
4. 构建完整的知识问答系统

## 📚 文档

- `UV_COMPLETE_GUIDE.md` - uv 完整使用指南
- `UV_GUIDE.md` - uv 快速入门
- `CONDA_SETUP.md` - Conda 环境设置（备选方案）
- `examples/README.md` - AI Agent 示例说明

## 💡 实用技巧

### 1. 不要激活虚拟环境
```bash
# ❌ 不需要这样做
source .venv/bin/activate
python script.py

# ✅ 直接用 uv run
uv run python script.py
```

### 2. 快速测试代码
```bash
# 启动 Python REPL
uv run python

# 或 IPython（更好的交互体验）
uv run ipython
```

### 3. 环境变量
```bash
# 临时设置环境变量
OPENAI_API_KEY=sk-xxx uv run python script.py

# 或在 .env 文件中配置（推荐）
```

### 4. 查看依赖
```bash
# 查看所有已安装的包
uv pip list

# 查看项目依赖树
uv pip tree
```

## ⚠️ 常见问题

### Q: uv 命令找不到？
```bash
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

### Q: OpenAI API 调用失败？
检查：
1. `.env` 文件中的 API key 是否正确
2. API 账户是否有余额
3. 网络连接是否正常

### Q: 依赖安装失败？
```bash
# 清理并重试
rm -rf .venv uv.lock
uv sync
```

### Q: 想切换到 Conda？
Conda 环境已经配置好了（`xai`），可以随时切换：
```bash
conda activate xai
```

## 🎯 下一步

1. ✅ 确认依赖安装完成
2. 📝 配置 `.env` 文件（添加 API key）
3. 🚀 运行第一个示例
4. 🛠️ 开始构建你的 AI Agent！

## 🆘 获取帮助

- 查看详细文档：`UV_COMPLETE_GUIDE.md`
- 查看示例说明：`examples/README.md`
- OpenAI 文档：https://platform.openai.com/docs
- LangChain 文档：https://python.langchain.com/

---

**准备好了吗？开始你的 AI Agent 之旅！** 🚀

```bash
# 运行你的第一个 Agent
uv run python examples/simple_agent_demo.py
```
