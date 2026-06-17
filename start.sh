#!/bin/bash
# 启动股票分析API服务

echo "🚀 启动 Stock Analysis Multi-Agent System..."
echo ""

# 检查.env文件
if [ ! -f .env ]; then
    echo "⚠️  .env 文件不存在，从模板复制..."
    cp .env.template .env
    echo "✅ 已创建 .env 文件，请配置你的API密钥"
    echo ""
fi

# 检查是否配置了LLM API密钥
if ! grep -q "your_" .env; then
    echo "✅ API密钥已配置"
else
    echo "⚠️  请先配置 .env 文件中的API密钥（OPENAI_API_KEY 或 ANTHROPIC_API_KEY）"
    echo ""
fi

# 启动服务
echo "🌐 启动FastAPI服务..."
echo "📝 API文档: http://localhost:8000/docs"
echo "🏥 健康检查: http://localhost:8000/api/v1/agents/health"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
