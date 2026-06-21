#!/bin/bash
# ============================================================================
# 项目启动脚本 - start.sh
# ============================================================================
# 用途: 启动股票分析 Multi-Agent 系统的 FastAPI 服务
# 环境管理: Conda (Python版本 + 环境隔离) + UV (依赖管理)
# 运行方式: ./start.sh 或 bash start.sh
# ============================================================================

set -e  # 遇到错误立即退出

echo "🚀 启动 Stock Analysis Multi-Agent System..."
echo ""

# ============================================================================
# 步骤1: 检查 Conda 环境
# ============================================================================
if [ -z "$CONDA_DEFAULT_ENV" ]; then
    echo "❌ Conda 环境未激活"
    echo "   请先激活 Conda 环境: conda activate <环境名>"
    exit 1
fi
echo "✅ Conda 环境: $CONDA_DEFAULT_ENV"
echo "   Python: $(python --version)"
echo ""

# ============================================================================
# 步骤2: 检查 UV 是否安装
# ============================================================================
if ! command -v uv &> /dev/null; then
    echo "❌ UV 未安装"
    echo "   安装方法: pip install uv"
    exit 1
fi
echo "✅ UV 版本: $(uv --version)"
echo ""

# ============================================================================
# 步骤3: 使用 UV 同步依赖
# ============================================================================
if [ -f "pyproject.toml" ]; then
    echo "📦 检查项目依赖..."
    if [ ! -d ".venv" ] && [ ! -f "uv.lock" ]; then
        echo "   首次运行，安装依赖（使用 UV）..."
        uv sync
    else
        echo "   依赖已同步"
    fi
    echo ""
else
    echo "⚠️  未找到 pyproject.toml，跳过 UV 依赖同步"
    echo ""
fi

# ============================================================================
# 步骤4: 检查环境配置文件 (.env)
# ============================================================================
if [ ! -f .env ]; then
    echo "⚠️  .env 文件不存在，从模板复制..."
    if [ -f .env.template ]; then
        cp .env.template .env
        echo "✅ 已创建 .env 文件，请配置你的API密钥"
    elif [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ 已创建 .env 文件，请配置你的API密钥"
    else
        echo "❌ 未找到 .env.template 或 .env.example"
        exit 1
    fi
    echo "???"
fi

# ============================================================================
# 步骤5: 验证 DASHSCOPE_API_KEY 配置
# ============================================================================
source .env
if [ -z "$DASHSCOPE_API_KEY" ]; then
    echo "❌ DASHSCOPE_API_KEY 未设置"
    echo "   请在 .env 文件中配置阿里云通义千问 API 密钥"
    exit 1
fi

if [[ "$DASHSCOPE_API_KEY" == *"your_"* ]]; then
    echo "⚠️  DASHSCOPE_API_KEY 仍为占位符"
    echo "   请替换为真实的 API 密钥"
    echo ""
else
    echo "✅ DASHSCOPE_API_KEY 已配置"
    echo ""
fi

# ============================================================================
# 步骤6: 启动 FastAPI 服务
# ============================================================================
echo "🌐 启动 FastAPI 服务..."
echo "📝 API文档: http://127.0.0.1:8000/docs"
echo "🏥 健康检查: http://127.0.0.1:8000/api/v1/agents/health"
echo ""
echo "按 Ctrl+C 停止服务"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 使用 UV 运行 Uvicorn（如果 pyproject.toml 中配置了脚本）
# 否则使用标准 Python 模块方式
if uv run --help &> /dev/null && [ -f "pyproject.toml" ]; then
    uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
fi



#使用Python模块方式启动uvicorn，uvicorn 是什么意思？中文回答
 #
 #⏺ Uvicorn 是一个高性能的 ASGI（异步服务器网关接口）Web 服务器，专门用于运行 Python 异步 Web 应用。
 #
 #  核心概念
 #
 #  1. Uvicorn 的作用
 #
 #  - Web 服务器：类似于 Nginx、Apache，但专门为 Python 异步应用设计
 #  - 运行 FastAPI：FastAPI 框架必须通过 ASGI 服务器才能运行，Uvicorn 是最常用的选择
 #  - 高性能：基于 uvloop 和 httptools，比传统 WSGI 服务器（如 Gunicorn）更快
 #
 #  2. 为什么需要 Uvicorn？
 #
 #  # app/main.py 中定义的 FastAPI 应用
 #  app = FastAPI()  # 这只是一个应用对象，不是服务器
 #
 #  @app.get("/")
 #  def read_root():
 #      return {"message": "Hello"}
 #
 #  - FastAPI 只是框架，它定义了路由、接口逻辑
 #  - Uvicorn 是服务器，它监听端口、处理 HTTP 请求、调用 FastAPI 应用
 #
 #  3. Python 模块方式启动的含义
 #
 #  # 方式1: Python 模块方式（推荐）
 #  python -m uvicorn app.main:app
 #
 #  # 方式2: 直接命令方式
 #  uvicorn app.main:app
 #
 #  区别：
 #  - python -m uvicorn：通过 Python 解释器加载 uvicorn 模块，确保使用当前 Python 环境
 #  - uvicorn：直接调用系统中的 uvicorn 命令，可能因环境变量问题找不到正确版本
 #
 #  4. app.main:app 的含义
 #
 #  - app.main：Python 模块路径（对应 app/main.py 文件）
 #  - :app：该文件中的变量名（FastAPI 应用实例）
 #
 #  相当于：
 #  from app.main import app  # 导入 FastAPI 应用实例
 #  uvicorn.run(app)           # 用 Uvicorn 服务器运行它
 #
 #  类比理解
 #
 #  ┌──────────────┬──────┬────────────────────────────────────────────┐
 #  │     组件     │ 类比 │                    说明                    │
 #  ├──────────────┼──────┼────────────────────────────────────────────┤
 #  - uvicorn：直接调用系统中的 uvicorn 命令，可能因环境变量问题找不到正确版本
 #
 #  4. app.main:app 的含义
 #
 #  - app.main：Python 模块路径（对应 app/main.py 文件）
 #  - :app：该文件中的变量名（FastAPI 应用实例）
 #
 #  相当于：
 #  from app.main import app  # 导入 FastAPI 应用实例
 #  uvicorn.run(app)           # 用 Uvicorn 服务器运行它
 #
 #  类比理解
 #
 #  ┌──────────────┬──────┬────────────────────────────────────────────┐
 #  │     组件     │ 类比 │                    说明                    │
 #  ├──────────────┼──────┼────────────────────────────────────────────┤
 #  │ FastAPI      │ 厨师 │ 知道怎么做菜（处理业务逻辑）               │
 #  ├──────────────┼──────┼────────────────────────────────────────────┤
 #  │ Uvicorn      │ 餐厅 │ 接待客人、传递订单、上菜（处理 HTTP 请求） │
 #  ├──────────────┼──────┼────────────────────────────────────────────┤
 #  │ app.main:app │ 菜单 │ 告诉餐厅找哪个厨师、做什么菜               │
 #  └──────────────┴──────┴────────────────────────────────────────────┘
 #
 #  没有餐厅（Uvicorn），厨师（FastAPI）再厉害也无法接待客人。
