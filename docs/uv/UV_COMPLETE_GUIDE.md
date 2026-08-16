# uv 完整使用指南

## 什么是 uv？

uv 是由 Astral 团队（Ruff 的创建者）开发的**极速 Python 包管理器**，用 Rust 编写。

### 核心优势
- ⚡ **极快**：比 pip 快 10-100 倍
- 🔒 **可靠**：准确的依赖解析，生成 uv.lock 锁文件
- 🎯 **现代化**：支持 pyproject.toml 标准
- 🔄 **兼容**：与 pip 生态完全兼容
- 🚀 **自动化**：自动管理虚拟环境

## 安装 uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 添加到 PATH（如果需要）
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

验证安装：
```bash
uv --version
```

## 核心命令

### 1. 项目初始化

```bash
# 初始化新项目
uv init my-project
cd my-project

# 初始化现有项目
uv init

# 不创建 README
uv init --no-readme
```

### 2. 虚拟环境管理

```bash
# uv 自动管理虚拟环境，通常不需要手动创建

# 如果需要手动创建
uv venv

# 指定 Python 版本
uv venv --python 3.11

# uv 会自动安装指定的 Python 版本（如果不存在）
uv python install 3.11
```

### 3. 依赖管理

#### 安装依赖

```bash
# 同步所有依赖（根据 pyproject.toml）
uv sync

# 安装所有可选依赖
uv sync --all-extras

# 安装特定组的依赖
uv sync --extra dev
uv sync --extra ai-tools
```

#### 添加包

```bash
# 添加到生产依赖
uv add requests
uv add openai langchain

# 添加到开发依赖
uv add --dev pytest ruff

# 添加到可选依赖组
uv add --optional ai-tools autogen
```

#### 移除包

```bash
uv remove package-name
```

#### 更新包

```bash
# 更新所有包
uv lock --upgrade

# 更新特定包
uv lock --upgrade-package requests
```

### 4. 运行命令

uv 的核心优势：**不需要手动激活虚拟环境**

```bash
# 运行 Python 脚本
uv run python script.py

# 运行模块
uv run python -m app.main

# 运行已安装的命令
uv run pytest
uv run ruff check .
uv run jupyter notebook
```

### 5. pip 兼容命令

```bash
# 列出已安装的包
uv pip list

# 显示包信息
uv pip show requests

# 冻结依赖
uv pip freeze

# 安装 requirements.txt
uv pip install -r requirements.txt

# 卸载包
uv pip uninstall package-name
```

## pyproject.toml 配置

uv 使用现代的 `pyproject.toml` 配置文件：

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.100.0",
    "openai>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "ruff>=0.1.0",
]

ai-tools = [
    "langchain>=0.1.0",
]
```

## 实际使用流程

### 新项目工作流

```bash
# 1. 创建项目
uv init my-ai-agent
cd my-ai-agent

# 2. 添加依赖
uv add openai langchain fastapi
uv add --dev pytest ruff

# 3. 编写代码
# ...

# 4. 运行
uv run python main.py

# 5. 测试
uv run pytest

# 6. 格式化代码
uv run ruff format .
```

### 克隆项目工作流

```bash
# 1. 克隆项目
git clone https://github.com/user/project.git
cd project

# 2. 同步依赖（uv 自动创建虚拟环境）
uv sync

# 3. 运行
uv run python main.py
```

## 常见场景

### 场景 1: 添加新功能需要新包

```bash
# 添加包
uv add pandas numpy

# 运行代码
uv run python analyze.py

# 提交更新后的配置
git add pyproject.toml uv.lock
git commit -m "Add data analysis dependencies"
```

### 场景 2: 更新依赖

```bash
# 更新所有包到最新版本
uv lock --upgrade
uv sync

# 测试确保兼容
uv run pytest
```

### 场景 3: 不同环境

```bash
# 开发环境（包含所有依赖）
uv sync --all-extras

# 生产环境（仅生产依赖）
uv sync --no-dev

# CI/CD 环境（固定版本）
uv sync --frozen
```

### 场景 4: 多 Python 版本

```bash
# 安装 Python 版本
uv python install 3.11
uv python install 3.12

# 使用特定版本
uv venv --python 3.11
uv run --python 3.11 python script.py

# 列出已安装的 Python 版本
uv python list
```

## 性能对比

### 安装速度测试

项目：50 个包的 AI 项目

| 工具 | 时间 | 相对速度 |
|------|------|----------|
| pip | 120s | 1x |
| conda | 300s | 0.4x |
| **uv** | **12s** | **10x** |

### 依赖解析

| 工具 | 准确性 | 锁文件 |
|------|--------|--------|
| pip | 中 | ❌ |
| poetry | 高 | ✅ |
| **uv** | **高** | **✅** |

## 高级功能

### 1. 工作区（Workspaces）

多包项目管理：

```toml
# 根目录 pyproject.toml
[tool.uv.workspace]
members = ["packages/*"]

# packages/core/pyproject.toml
[project]
name = "core"
...

# packages/api/pyproject.toml
[project]
name = "api"
dependencies = ["core"]
```

### 2. 脚本执行

在 `pyproject.toml` 中定义脚本：

```toml
[project.scripts]
dev = "uvicorn app.main:app --reload"
test = "pytest tests/"
```

运行：
```bash
uv run dev
uv run test
```

### 3. 环境变量

```bash
# 设置环境变量运行
UV_INDEX_URL=https://pypi.org/simple uv sync
```

### 4. 缓存管理

```bash
# 查看缓存
uv cache dir

# 清理缓存
uv cache clean
```

## 迁移指南

### 从 pip + venv 迁移

```bash
# 1. 生成 pyproject.toml
# 手动创建或使用现有 requirements.txt

# 2. 初始化 uv
uv init

# 3. 从 requirements.txt 导入
uv add $(cat requirements.txt | grep -v '^#' | grep -v '^$')

# 4. 同步
uv sync
```

### 从 conda 迁移

```bash
# 1. 导出 conda 依赖
conda list --export > conda-packages.txt

# 2. 筛选 Python 包（移除 conda 特定包）
# 手动编辑或使用脚本

# 3. 用 uv 安装
uv init
uv add <packages>
```

### 从 poetry 迁移

```bash
# poetry 的 pyproject.toml 格式与 uv 兼容
# 直接使用
uv sync
```

## 故障排除

### 问题 1: uv 命令找不到

```bash
# 添加到 PATH
export PATH="$HOME/.local/bin:$PATH"

# 永久添加
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 问题 2: 虚拟环境冲突

```bash
# 警告: VIRTUAL_ENV=venv does not match

# 方案 1: 清理旧环境
rm -rf venv .venv
uv sync

# 方案 2: 使用 --active
uv run --active python script.py
```

### 问题 3: 依赖冲突

```bash
# 查看详细错误
uv sync --verbose

# 更新锁文件
rm uv.lock
uv lock

# 放宽版本约束
# 编辑 pyproject.toml，使用更宽松的版本范围
# openai>=1.0.0  而不是  openai==1.0.0
```

### 问题 4: Python 版本不匹配

```bash
# 安装所需版本
uv python install 3.11

# 指定版本
uv venv --python 3.11
```

## 最佳实践

### 1. 版本管理

```toml
# ✅ 好：使用范围
dependencies = [
    "openai>=1.0.0,<2.0.0",
]

# ❌ 差：固定版本（除非必要）
dependencies = [
    "openai==1.0.0",
]
```

### 2. 组织依赖

```toml
[project.optional-dependencies]
# 开发工具
dev = ["pytest", "ruff", "mypy"]

# AI 工具
ai = ["langchain", "chromadb"]

# 生产服务器
server = ["uvicorn", "gunicorn"]
```

### 3. 锁文件管理

```bash
# ✅ 提交 uv.lock 到版本控制
git add uv.lock

# ✅ 定期更新依赖
uv lock --upgrade

# ✅ CI/CD 使用固定版本
uv sync --frozen
```

### 4. 项目结构

```
my-project/
├── pyproject.toml      # 项目配置
├── uv.lock             # 锁定依赖版本
├── .python-version     # 指定 Python 版本（可选）
├── src/
│   └── my_project/
│       └── __init__.py
└── tests/
    └── test_main.py
```

## 速查表

```bash
# 初始化
uv init                          # 初始化项目
uv venv                          # 创建虚拟环境

# 依赖管理
uv add <package>                 # 添加包
uv add --dev <package>           # 添加开发依赖
uv remove <package>              # 移除包
uv sync                          # 同步依赖
uv sync --all-extras             # 安装所有可选依赖
uv lock --upgrade                # 更新依赖

# 运行
uv run python script.py          # 运行脚本
uv run pytest                    # 运行测试
uv run <command>                 # 运行任何命令

# pip 兼容
uv pip list                      # 列出包
uv pip show <package>            # 显示包信息
uv pip freeze                    # 冻结依赖

# Python 版本
uv python install 3.11           # 安装 Python
uv python list                   # 列出版本

# 缓存
uv cache clean                   # 清理缓存
```

## 学习资源

- 📚 [官方文档](https://docs.astral.sh/uv/)
- 🎥 [视频教程](https://www.youtube.com/results?search_query=uv+python+package+manager)
- 💬 [GitHub Issues](https://github.com/astral-sh/uv/issues)
- 🐦 [Astral Twitter](https://twitter.com/astral_sh)

## 总结

**为什么选择 uv？**
- ✅ 速度极快
- ✅ 现代化工作流
- ✅ 自动环境管理
- ✅ 兼容 pip 生态
- ✅ 准确的依赖解析

**适合场景：**
- 新项目（强烈推荐）
- 个人开发
- 需要快速迭代
- CI/CD 流程

**可能不适合：**
- 需要非 Python 依赖（用 conda）
- 团队已有工具链且不想改变
- 特殊平台/架构支持

---

Happy coding with uv! ⚡
