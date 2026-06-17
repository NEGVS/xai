# Stock Analysis Multi-Agent System

基于 **FastAPI + LangGraph + Multi-Agent** 的智能股票分析系统

## 🌟 项目特性

- ✅ **Multi-Agent协作架构** - 7个专业Agent协同工作
- ✅ **LangGraph状态图编排** - 支持并行和串行执行
- ✅ **大模型智能决策** - 集成Claude/OpenAI进行分析
- ✅ **实时股票数据** - 使用yfinance获取市场数据
- ✅ **新闻情感分析** - 分析市场情绪和关键事件
- ✅ **风险评估** - 计算VaR、波动率等风险指标
- ✅ **投资建议** - 基于多维度数据生成建议
- ✅ **RESTful API** - 完整的API接口
- ✅ **自动文档** - FastAPI自动生成API文档

## 📋 系统架构

```
用户
  │
  ▼
FastAPI API
  │
  ▼
LangGraph Workflow
  │
  ├─► Planner Agent (任务规划)
  │
  ├─► News Agent (新闻分析) ────┐
  │                            ├─► Risk Agent (风险评估)
  ├─► Financial Agent (财务分析)─┘         │
                                          ▼
                                 Investment Agent (投资建议)
                                          │
                                          ▼
                                    Report Agent (报告生成)
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.11+
- pip 或 uv

### 2. 安装依赖

```bash
# 安装所有依赖
pip install -r requirements.txt

# 或使用uv（更快）
uv pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.template .env

# 编辑.env文件，配置你的API密钥
# 至少需要配置一个LLM API密钥：
# - OPENAI_API_KEY (OpenAI GPT)
# - ANTHROPIC_API_KEY (Claude，推荐)
```

### 4. 启动服务

```bash
# 使用启动脚本
./start.sh

# 或直接运行
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. 访问API文档

浏览器打开：
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/api/v1/agents/health

## 📖 API使用示例

### 分析股票

```bash
curl -X POST "http://localhost:8000/api/v1/analysis/stock" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "analysis_type": "full",
    "time_range": "1M"
  }'
```

### Python客户端示例

```python
import requests

# 分析Apple股票
response = requests.post(
    "http://localhost:8000/api/v1/analysis/stock",
    json={
        "symbol": "AAPL",
        "analysis_type": "full",
        "time_range": "1M",
        "include_news": True,
        "include_financial": True,
        "include_risk": True
    }
)

result = response.json()
print(f"分析成功: {result['success']}")
print(f"投资建议: {result['data']['investment']['recommendation']}")
print(f"风险级别: {result['data']['risk']['risk_level']}")
```

## 🤖 Agent说明

### 1. Planner Agent
- **职责**: 任务规划和执行策略
- **输出**: 执行计划（并行/串行策略）

### 2. News Agent
- **职责**: 收集和分析新闻
- **功能**: 情感分析、关键事件提取
- **数据源**: NewsAPI、模拟数据

### 3. Financial Agent
- **职责**: 财务数据和技术指标
- **功能**: 价格数据、技术指标（MA、RSI、MACD）、财务健康度
- **数据源**: Yahoo Finance (yfinance)

### 4. Risk Agent
- **职责**: 风险评估
- **功能**: 波动率计算、VaR计算、风险因素识别
- **输出**: 风险级别、风险评分

### 5. Investment Agent
- **职责**: 投资建议生成
- **功能**: BUY/HOLD/SELL建议、目标价位、止损价位
- **方法**: LLM生成 + 规则补充

### 6. Report Agent
- **职责**: 生成最终报告
- **功能**: 聚合所有数据、生成执行摘要
- **输出**: 结构化分析报告

## 📊 数据源

- **股票数据**: Yahoo Finance (免费，无需API key)
- **新闻数据**: NewsAPI (可选，需要API key) 或 模拟数据
- **LLM服务**: OpenAI GPT-4 或 Anthropic Claude

## 🔧 配置说明

### 必需配置

```bash
# 至少配置一个LLM API密钥
OPENAI_API_KEY=sk-...          # OpenAI
ANTHROPIC_API_KEY=sk-ant-...   # Claude (推荐)
```

### 可选配置

```bash
# 新闻API (可选，不配置会使用模拟数据)
NEWS_API_KEY=your_key

# 数据库 (可选，用于持久化)
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

## 📁 项目结构

```
xai/
├── app/
│   ├── agents/              # Agent实现
│   │   ├── base.py          # 基础Agent类
│   │   ├── planner.py       # 规划Agent
│   │   ├── news.py          # 新闻Agent
│   │   ├── financial.py     # 财务Agent
│   │   ├── risk.py          # 风险Agent
│   │   ├── investment.py    # 投资Agent
│   │   └── report.py        # 报告Agent
│   ├── api/                 # API路由
│   │   └── v1/
│   │       ├── stock.py     # 股票分析API
│   │       └── agents.py    # Agent管理API
│   ├── core/                # 核心配置
│   │   ├── config.py        # 配置管理
│   │   └── llm.py           # LLM服务
│   ├── schemas/             # 数据模型
│   │   ├── agent.py         # Agent相关模型
│   │   └── request.py       # 请求/响应模型
│   ├── tools/               # 工具集
│   │   ├── stock_api.py     # 股票数据工具
│   │   └── news_fetcher.py  # 新闻获取工具
│   ├── workflows/           # LangGraph工作流
│   │   └── stock_analysis.py
│   └── main.py              # FastAPI入口
├── requirements.txt         # 依赖列表
├── .env.template           # 环境变量模板
├── start.sh                # 启动脚本
└── README.md               # 本文件
```

## 🧪 测试示例

### 测试不同股票

```bash
# Apple
curl -X POST "http://localhost:8000/api/v1/analysis/stock" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}'

# Tesla
curl -X POST "http://localhost:8000/api/v1/analysis/stock" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "TSLA"}'

# Microsoft
curl -X POST "http://localhost:8000/api/v1/analysis/stock" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "MSFT"}'
```

### 健康检查

```bash
curl http://localhost:8000/api/v1/agents/health
```

## 🔍 故障排查

### 1. LLM API错误
```
Error: 至少需要配置一个LLM API Key
```
**解决**: 在 `.env` 中配置 `OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY`

### 2. 股票数据获取失败
```
Error: 无法获取股票数据
```
**解决**: 检查网络连接，确认股票代码正确（使用美股代码）

### 3. 依赖安装失败
```
Error: Could not find a version that satisfies...
```
**解决**: 
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 📈 性能优化

- **并行执行**: News和Financial Agent并行运行
- **缓存**: 可配置Redis缓存重复查询
- **异步**: 全异步API设计

## 🛣️ 开发路线图

- [x] 核心Agent实现
- [x] LangGraph工作流
- [x] FastAPI接口
- [x] 基础文档
- [ ] 数据库持久化
- [ ] Redis缓存
- [ ] 前端界面 (Vue3)
- [ ] Docker部署
- [ ] 监控告警
- [ ] 更多数据源

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**开发日期**: 2026-06-17  
**版本**: v0.1.0
