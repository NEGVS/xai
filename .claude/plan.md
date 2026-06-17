# Spring Boot + LangGraph + Multi-Agent 股票分析系统 - 实施计划

## 当前环境分析

### ✅ 已具备条件
- **Python**: 3.12.13 (满足要求 >=3.11)
- **Java**: 21.0.1 (满足要求 Java 17+)
- **Maven**: 3.6.3 (可用于Spring Boot构建)
- **项目结构**: 已有基础的Python项目结构
- **环境配置**: 有 .env.example 和 pyproject.toml

### ⚠️ 需要安装/配置
- **LangGraph**: 需要安装
- **LangChain**: 需要安装完整版本
- **Spring Boot**: 需要创建新的后端模块
- **数据库**: PostgreSQL, Redis
- **前端**: Vue3项目
- **Docker**: 用于部署

### 📊 项目架构决策

基于当前项目是Python项目，我建议采用**混合架构**：

**方案A: Python为主 + FastAPI（推荐）**
- ✅ 利用现有Python项目结构
- ✅ LangGraph原生Python支持
- ✅ 快速开发，无需Java-Python桥接
- ✅ FastAPI性能优秀，异步支持好
- ✅ 符合现代AI项目技术栈
- ❌ 放弃Spring Boot生态

**方案B: Spring Boot + Python Agent服务（原设计）**
- ✅ 符合CLAUDE.md原始设计
- ✅ Spring Boot企业级特性
- ✅ 前后端清晰分离
- ❌ 需要Java-Python集成复杂度
- ❌ 开发周期长

**建议**: 采用**方案A**，理由：
1. 现有项目已经是Python生态
2. LangGraph和LangChain是Python原生
3. FastAPI可以提供完整的REST API
4. 开发效率更高
5. 如需Spring Boot特性，可后期重构API层

---

## 实施计划（基于FastAPI方案）

### Phase 1: 基础框架搭建 (2-3小时)

#### 1.1 依赖安装
```bash
# 安装LangGraph和相关依赖
pip install langgraph langchain langchain-openai langchain-anthropic
pip install yfinance alpha-vantage newsapi-python  # 数据源
pip install redis postgresql psycopg2-binary
pip install sqlalchemy alembic  # ORM和迁移
```

#### 1.2 项目结构重组
```
xai/
├── app/
│   ├── agents/           # Multi-Agent实现
│   │   ├── gateway.py
│   │   ├── planner.py
│   │   ├── news.py
│   │   ├── financial.py
│   │   ├── risk.py
│   │   ├── investment.py
│   │   └── report.py
│   ├── api/              # FastAPI路由
│   │   ├── v1/
│   │   │   ├── stock.py
│   │   │   └── agents.py
│   ├── core/             # 核心配置
│   │   ├── config.py
│   │   ├── database.py
│   │   └── llm.py
│   ├── models/           # 数据模型
│   │   ├── request.py
│   │   ├── report.py
│   │   └── agent.py
│   ├── services/         # 业务逻辑
│   │   ├── orchestrator.py
│   │   ├── stock_data.py
│   │   └── llm_service.py
│   ├── tools/            # Agent工具
│   │   ├── news_fetcher.py
│   │   ├── stock_api.py
│   │   └── calculator.py
│   ├── workflows/        # LangGraph工作流
│   │   └── stock_analysis.py
│   └── main.py           # FastAPI入口
├── tests/
├── docker-compose.yml
├── Dockerfile
├── .env
└── requirements.txt
```

#### 1.3 配置文件创建
- 数据库配置 (PostgreSQL + Redis)
- LLM配置 (OpenAI/Claude/etc)
- 日志配置
- API配置

---

### Phase 2: Agent核心开发 (6-8小时)

#### 2.1 Agent基础类
```python
# app/agents/base.py
class BaseAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    async def execute(self, state: dict) -> dict:
        raise NotImplementedError
```

#### 2.2 实现7个Agent
1. **AgentGateway** - 请求路由和状态管理
2. **PlannerAgent** - 任务规划
3. **NewsAgent** - 新闻收集和情感分析
4. **FinancialAgent** - 财务数据和技术指标
5. **RiskAgent** - 风险评估
6. **InvestmentAgent** - 投资建议
7. **ReportAgent** - 报告生成

每个Agent包含：
- 工具定义（Tool）
- 提示词（Prompt）
- 执行逻辑（Execute）
- 输出格式（Schema）

#### 2.3 工具开发
- `YahooFinanceTool` - 股票数据
- `NewsAPITool` - 新闻获取
- `TechnicalIndicatorTool` - 技术指标计算
- `RiskCalculatorTool` - 风险计算

---

### Phase 3: LangGraph工作流 (3-4小时)

#### 3.1 状态定义
```python
from typing import TypedDict, List, Dict, Optional

class AnalysisState(TypedDict):
    stock_symbol: str
    request_id: str
    plan: Optional[Dict]
    news_data: Optional[Dict]
    financial_data: Optional[Dict]
    risk_data: Optional[Dict]
    investment_advice: Optional[Dict]
    report: Optional[Dict]
    errors: List[str]
```

#### 3.2 工作流编排
```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AnalysisState)

# 添加节点
workflow.add_node("planner", planner_agent)
workflow.add_node("news", news_agent)
workflow.add_node("financial", financial_agent)
workflow.add_node("risk", risk_agent)
workflow.add_node("investment", investment_agent)
workflow.add_node("report", report_agent)

# 定义流程
workflow.set_entry_point("planner")
workflow.add_conditional_edges("planner", should_continue)
workflow.add_edge("news", "risk")
workflow.add_edge("financial", "risk")
workflow.add_edge("risk", "investment")
workflow.add_edge("investment", "report")
workflow.add_edge("report", END)

app = workflow.compile()
```

#### 3.3 并行执行优化
- News Agent 和 Financial Agent 并行执行
- 错误处理和重试机制
- 超时控制

---

### Phase 4: FastAPI接口开发 (3-4小时)

#### 4.1 REST API端点
```python
# POST /api/v1/analysis/stock - 股票分析
# GET  /api/v1/analysis/history - 历史记录
# GET  /api/v1/analysis/report/{id} - 获取报告
# GET  /api/v1/agents/health - 健康检查
# GET  /api/v1/agents/status - Agent状态
```

#### 4.2 WebSocket支持（可选）
- 实时推送分析进度
- 流式返回结果

#### 4.3 数据持久化
- SQLAlchemy ORM模型
- 请求记录
- 报告存储
- Agent执行日志

---

### Phase 5: 前端开发 (4-6小时)

#### 5.1 Vue3项目初始化
```bash
npm create vue@latest frontend
cd frontend
npm install
npm install axios element-plus echarts pinia
```

#### 5.2 核心页面
1. **股票分析页面**
   - 股票代码输入
   - 分析类型选择
   - 实时进度显示
   
2. **报告展示页面**
   - 新闻摘要卡片
   - 财务指标图表
   - 风险评分可视化
   - 投资建议展示

3. **历史记录页面**
   - 分析历史列表
   - 筛选和搜索

#### 5.3 数据可视化
- ECharts股价走势图
- 技术指标图表
- 风险分布雷达图

---

### Phase 6: 数据源集成 (2-3小时)

#### 6.1 股票数据API
- **yfinance** (免费，无需API key)
  - 实时股价
  - 历史数据
  - 基本面数据

- **Alpha Vantage** (需要API key)
  - 备用数据源
  - 更多技术指标

#### 6.2 新闻API
- **NewsAPI** (需要API key)
  - 全球新闻
  - 股票相关新闻

- **备用**: Google News RSS

#### 6.3 财报数据
- **Yahoo Finance**
- **SEC EDGAR API** (美股)

---

### Phase 7: 测试与优化 (2-3小时)

#### 7.1 单元测试
```python
# tests/agents/test_news_agent.py
async def test_news_agent():
    agent = NewsAgent(llm, tools)
    result = await agent.execute({"stock_symbol": "AAPL"})
    assert "sentiment_score" in result
```

#### 7.2 集成测试
- 完整工作流测试
- API端点测试
- 数据库操作测试

#### 7.3 性能优化
- Agent并行执行
- 缓存策略（Redis）
- 数据库索引优化

---

### Phase 8: Docker部署 (1-2小时)

#### 8.1 Dockerfile
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 8.2 docker-compose.yml
```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: stock_analysis
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
  
  redis:
    image: redis:7-alpine
  
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
  
  frontend:
    build: ./frontend
    ports:
      - "80:80"
```

---

## 关键技术实现细节

### 1. LangGraph状态管理
```python
from langgraph.graph import StateGraph

def create_workflow():
    workflow = StateGraph(AnalysisState)
    
    # 并行执行News和Financial
    workflow.add_node("parallel_start", lambda x: x)
    workflow.add_conditional_edges(
        "parallel_start",
        lambda x: ["news", "financial"]
    )
    
    return workflow.compile()
```

### 2. LLM服务封装
```python
class LLMService:
    def __init__(self):
        self.openai = ChatOpenAI(model="gpt-4")
        self.claude = ChatAnthropic(model="claude-3-sonnet")
    
    async def analyze_sentiment(self, text: str) -> float:
        # 使用LLM进行情感分析
        pass
    
    async def generate_advice(self, data: dict) -> str:
        # 生成投资建议
        pass
```

### 3. 工具系统
```python
from langchain.tools import BaseTool

class YahooFinanceTool(BaseTool):
    name = "yahoo_finance"
    description = "获取股票实时数据和历史数据"
    
    def _run(self, symbol: str) -> dict:
        import yfinance as yf
        stock = yf.Ticker(symbol)
        return stock.info
```

---

## 开发优先级

### 🔴 P0 - 核心功能（必须实现）
1. LangGraph工作流基础框架
2. 3个核心Agent (News, Financial, Investment)
3. FastAPI基础接口
4. 基本的前端展示页面

### 🟡 P1 - 重要功能（应该实现）
1. 完整的7个Agent
2. 数据持久化
3. 错误处理和重试
4. 数据可视化

### 🟢 P2 - 增强功能（可选实现）
1. WebSocket实时推送
2. 缓存优化
3. 多数据源切换
4. 监控告警

---

## 技术风险与缓解

### 风险1: LLM API成本
**缓解**:
- 使用较小模型处理简单任务
- 实现结果缓存
- 设置token使用上限

### 风险2: 数据源API限制
**缓解**:
- 使用免费的yfinance作为主数据源
- 实现多数据源降级
- 本地缓存历史数据

### 风险3: Agent执行时间长
**缓解**:
- 并行执行独立Agent
- 异步处理
- 设置合理超时

---

## 时间估算

| 阶段 | 时间 | 累计 |
|------|------|------|
| Phase 1: 基础框架 | 2-3h | 3h |
| Phase 2: Agent开发 | 6-8h | 11h |
| Phase 3: LangGraph | 3-4h | 15h |
| Phase 4: API开发 | 3-4h | 19h |
| Phase 5: 前端开发 | 4-6h | 25h |
| Phase 6: 数据源集成 | 2-3h | 28h |
| Phase 7: 测试优化 | 2-3h | 31h |
| Phase 8: Docker部署 | 1-2h | 33h |

**总计**: 约33小时（4-5个工作日）

---

## 下一步行动

### 立即开始:
1. ✅ 安装LangGraph和依赖
2. ✅ 创建项目基础结构
3. ✅ 配置环境变量
4. ✅ 实现第一个Agent (NewsAgent)
5. ✅ 创建简单的LangGraph工作流测试

### 第一个里程碑（MVP）:
- 完成News Agent和Financial Agent
- 实现基础LangGraph工作流
- 提供一个API接口测试股票分析
- 命令行输出分析结果

---

## 决策点需要用户确认

### ❓ 1. 技术栈选择
**问题**: 使用FastAPI (Python) 还是 Spring Boot (Java)?
**建议**: FastAPI（原因：现有项目是Python，LangGraph原生支持）
**影响**: 架构设计、开发周期

### ❓ 2. LLM提供商
**问题**: 使用OpenAI、Claude还是其他?
**建议**: Claude (Sonnet) - 性价比高
**影响**: API成本、响应质量

### ❓ 3. 数据源
**问题**: 使用付费API还是免费数据源?
**建议**: 先用免费yfinance，后期可扩展
**影响**: 数据质量、API成本

### ❓ 4. 开发范围
**问题**: 完整实现还是MVP优先?
**建议**: MVP优先（P0功能）
**影响**: 开发时间、功能完整度

---

## 总结

本计划采用**Python + FastAPI + LangGraph**技术栈，充分利用现有项目基础，优先实现核心的Multi-Agent股票分析功能。

**核心优势**:
- ✅ 快速开发，利用现有Python生态
- ✅ LangGraph原生支持，无需桥接
- ✅ FastAPI性能优秀，文档自动生成
- ✅ 易于扩展和维护

**推荐实施路径**: 
Phase 1 → Phase 2 → Phase 3 → Phase 4（MVP）→ 评估 → Phase 5-8（完整版）
