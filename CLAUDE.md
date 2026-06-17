# Spring Boot + LangGraph + Multi-Agent 股票分析系统 - 设计文档

# 必须做到：
.env.example 提交
.env 永不提交
secrets 全部 os.getenv
pre-commit hook
gitleaks 扫描
CI check（进阶）

❌ 永远不要做：
写死 API Key
提交 .env
提交 RAG dump（你刚踩的坑）
commit log 里写 key
copy production key 到 demo

## 1. 项目概述

### 1.1 项目背景
本项目旨在构建一个基于AI Agent的智能股票分析系统，通过多Agent协作完成从数据收集、分析到投资建议的全流程自动化。系统同时作为AI Agent技术的demo平台，展示LangGraph、大模型集成、工具调用等关键技术。

### 1.2 核心目标
- **构建生产级AI Agent系统**：展示企业级Multi-Agent架构设计与实现
- **股票智能分析**：提供全方位的股票分析服务（新闻、财务、风险、投资建议）
- **技术栈整合**：Spring Boot（后端） + LangGraph（Agent编排） + 大模型（智能决策） + Vue3（前端）
- **可部署可扩展**：支持容器化部署，具备良好的可扩展性和可维护性

### 1.3 关键特性
- ✅ Multi-Agent协作架构
- ✅ LangGraph状态图编排
- ✅ 大模型智能决策（支持Claude、OpenAI等）
- ✅ 实时数据获取与分析
- ✅ RESTful API接口
- ✅ 前后端分离
- ✅ Docker容器化部署

---

## 2. 系统架构

### 2.1 总体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                         用户层                               │
│                     Vue3 前端应用                            │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST API
┌────────────────────▼────────────────────────────────────────┐
│                    Spring Boot 应用层                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Controller Layer                        │   │
│  │  - StockAnalysisController                          │   │
│  │  - AgentController                                  │   │
│  └──────────────────┬───────────────────────────────────┘   │
│                     │                                        │
│  ┌──────────────────▼───────────────────────────────────┐   │
│  │              Service Layer                           │   │
│  │  - AgentOrchestratorService                         │   │
│  │  - StockDataService                                 │   │
│  └──────────────────┬───────────────────────────────────┘   │
└────────────────────┼────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  LangGraph Agent层                          │
│                                                              │
│                    ┌─────────────┐                          │
│                    │Agent Gateway│                          │
│                    └──────┬──────┘                          │
│                           │                                 │
│      ┌────────────────────┼────────────────────┐           │
│      │                    │                    │           │
│  ┌───▼────┐        ┌──────▼─────┐      ┌──────▼─────┐    │
│  │Planner │        │News Agent  │      │Financial   │    │
│  │ Agent  │        │            │      │Agent       │    │
│  └───┬────┘        └──────┬─────┘      └──────┬─────┘    │
│      └────────────────────┼────────────────────┘           │
│                           │                                 │
│                    ┌──────▼─────┐                          │
│                    │Risk Agent  │                          │
│                    └──────┬─────┘                          │
│                           │                                 │
│                    ┌──────▼─────────┐                      │
│                    │Investment Agent│                      │
│                    └──────┬─────────┘                      │
│                           │                                 │
│                    ┌──────▼─────┐                          │
│                    │Report Agent│                          │
│                    └──────┬─────┘                          │
└───────────────────────────┼─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                      大模型层                                │
│  - Claude API (Anthropic)                                  │
│  - OpenAI API                                              │
│  - 其他LLM服务                                              │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                      外部服务层                              │
│  - 股票数据API (Yahoo Finance, Alpha Vantage等)            │
│  - 新闻API                                                 │
│  - 财务数据源                                               │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 技术栈

#### 后端
- **框架**: Spring Boot 3.x
- **语言**: Java 17+
- **Agent编排**: LangGraph (通过Python集成或Java实现)
- **大模型**: Claude API, OpenAI API
- **数据库**: PostgreSQL (持久化) + Redis (缓存)
- **消息队列**: RabbitMQ (异步任务)
- **日志**: SLF4J + Logback
- **监控**: Spring Boot Actuator + Prometheus

#### 前端
- **框架**: Vue 3 + TypeScript
- **UI库**: Element Plus
- **状态管理**: Pinia
- **HTTP客户端**: Axios
- **图表**: ECharts

#### 部署
- **容器化**: Docker + Docker Compose
- **编排**: Kubernetes (可选)
- **CI/CD**: GitHub Actions / GitLab CI

---

## 3. Agent详细设计

### 3.1 Agent Gateway
**职责**: Agent系统的入口，负责请求路由、状态管理、Agent调度

**功能**:
- 接收来自Spring Boot的分析请求
- 初始化LangGraph状态图
- 协调各Agent的执行顺序
- 聚合Agent结果并返回

**输入**: 
```json
{
  "stockSymbol": "AAPL",
  "analysisType": "full",
  "timeRange": "1M"
}
```

**输出**: 完整的分析报告（JSON格式）

---

### 3.2 Planner Agent
**职责**: 分析任务规划，决定执行策略

**功能**:
- 解析用户请求，确定分析目标
- 评估所需数据源和Agent
- 生成执行计划（哪些Agent并行，哪些串行）
- 动态调整执行策略

**工具**:
- 任务分解工具
- 优先级评估工具

**示例输出**:
```json
{
  "plan": {
    "parallel_phase_1": ["news_agent", "financial_agent"],
    "sequential_phase_2": ["risk_agent", "investment_agent"],
    "final_phase": ["report_agent"]
  },
  "estimated_time": "45s"
}
```

---

### 3.3 News Agent
**职责**: 收集和分析股票相关新闻

**功能**:
- 从多个新闻源获取最新新闻
- 使用LLM进行情感分析
- 提取关键事件和影响因素
- 生成新闻摘要

**工具**:
- 新闻API调用工具
- 情感分析工具
- 文本摘要工具

**数据源**:
- NewsAPI
- Google News
- Financial Times API

**输出示例**:
```json
{
  "news_summary": "Apple发布新款iPhone，市场反应积极",
  "sentiment_score": 0.75,
  "key_events": [
    "新品发布会",
    "季度财报超预期"
  ],
  "impact_level": "high"
}
```

---

### 3.4 Financial Agent
**职责**: 分析财务数据和技术指标

**功能**:
- 获取实时股价、成交量
- 计算技术指标（MA, MACD, RSI等）
- 分析财报数据
- 生成财务健康度评分

**工具**:
- 股票数据API工具
- 技术指标计算工具
- 财报解析工具

**数据源**:
- Yahoo Finance
- Alpha Vantage
- SEC EDGAR

**输出示例**:
```json
{
  "current_price": 175.43,
  "price_change_1d": "+2.3%",
  "technical_indicators": {
    "MA_50": 172.5,
    "MA_200": 168.2,
    "RSI": 62,
    "MACD": "bullish"
  },
  "financial_health": {
    "pe_ratio": 28.5,
    "debt_to_equity": 1.2,
    "score": 8.5
  }
}
```

---

### 3.5 Risk Agent
**职责**: 评估投资风险

**功能**:
- 分析历史波动率
- 计算VaR (Value at Risk)
- 评估市场风险、行业风险
- 综合新闻和财务数据评估风险

**工具**:
- 风险计算工具
- 历史数据分析工具
- 相关性分析工具

**输入**: News Agent + Financial Agent的输出

**输出示例**:
```json
{
  "risk_level": "medium",
  "volatility": 0.25,
  "var_95": -3.2,
  "risk_factors": [
    "市场整体下行",
    "供应链不确定性"
  ],
  "risk_score": 6.5
}
```

---

### 3.6 Investment Agent
**职责**: 生成投资建议

**功能**:
- 综合所有Agent的分析结果
- 使用LLM生成投资策略
- 提供买入/持有/卖出建议
- 设定目标价位和止损点

**工具**:
- 策略生成工具
- 价格预测工具

**输入**: 所有前置Agent的输出

**输出示例**:
```json
{
  "recommendation": "BUY",
  "confidence": 0.82,
  "target_price": 185.0,
  "stop_loss": 168.0,
  "time_horizon": "3M",
  "reasoning": "技术面强势突破，基本面稳健，短期看涨"
}
```

---

### 3.7 Report Agent
**职责**: 生成最终分析报告

**功能**:
- 聚合所有Agent的输出
- 生成结构化报告
- 提供可视化数据建议
- 生成自然语言摘要

**工具**:
- 报告生成工具
- 模板引擎

**输出示例**:
```json
{
  "report_id": "RPT-20260617-AAPL-001",
  "timestamp": "2026-06-17T10:30:00Z",
  "stock_symbol": "AAPL",
  "executive_summary": "Apple股票目前呈现强势上涨趋势...",
  "sections": {
    "news": {...},
    "financial": {...},
    "risk": {...},
    "investment": {...}
  },
  "charts": [
    "price_trend",
    "technical_indicators",
    "risk_distribution"
  ]
}
```

---

## 4. LangGraph工作流设计

### 4.1 状态图定义

```python
from langgraph.graph import StateGraph, END

# 定义状态
class AnalysisState(TypedDict):
    stock_symbol: str
    plan: Dict
    news_data: Dict
    financial_data: Dict
    risk_data: Dict
    investment_advice: Dict
    report: Dict
    errors: List[str]

# 构建状态图
workflow = StateGraph(AnalysisState)

# 添加节点
workflow.add_node("planner", planner_agent)
workflow.add_node("news", news_agent)
workflow.add_node("financial", financial_agent)
workflow.add_node("risk", risk_agent)
workflow.add_node("investment", investment_agent)
workflow.add_node("report", report_agent)

# 定义边
workflow.set_entry_point("planner")
workflow.add_edge("planner", "news")
workflow.add_edge("planner", "financial")
workflow.add_edge("news", "risk")
workflow.add_edge("financial", "risk")
workflow.add_edge("risk", "investment")
workflow.add_edge("investment", "report")
workflow.add_edge("report", END)

# 编译
app = workflow.compile()
```

### 4.2 执行流程

1. **用户发起请求** → Agent Gateway
2. **Planner Agent** 分析任务，生成执行计划
3. **并行执行**: News Agent + Financial Agent
4. **Risk Agent** 基于前两者的结果进行风险评估
5. **Investment Agent** 生成投资建议
6. **Report Agent** 生成最终报告
7. **返回结果** → Spring Boot → 前端

---

## 5. API设计

### 5.1 REST API端点

#### 5.1.1 股票分析接口
```
POST /api/v1/analysis/stock
```

**请求体**:
```json
{
  "symbol": "AAPL",
  "analysisType": "full",
  "timeRange": "1M",
  "includeNews": true,
  "includeFinancial": true,
  "includeRisk": true
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "reportId": "RPT-20260617-AAPL-001",
    "timestamp": "2026-06-17T10:30:00Z",
    "analysis": {
      "news": {...},
      "financial": {...},
      "risk": {...},
      "investment": {...}
    }
  },
  "executionTime": "42s"
}
```

#### 5.1.2 获取分析历史
```
GET /api/v1/analysis/history?symbol=AAPL&limit=10
```

#### 5.1.3 获取单个报告
```
GET /api/v1/analysis/report/{reportId}
```

#### 5.1.4 Agent健康检查
```
GET /api/v1/agents/health
```

**响应**:
```json
{
  "status": "healthy",
  "agents": {
    "planner": "active",
    "news": "active",
    "financial": "active",
    "risk": "active",
    "investment": "active",
    "report": "active"
  },
  "llm_status": "connected"
}
```

---

## 6. 数据模型

### 6.1 核心实体

#### StockAnalysisRequest
```java
@Entity
@Table(name = "analysis_requests")
public class StockAnalysisRequest {
    @Id
    private String id;
    private String symbol;
    private String analysisType;
    private LocalDateTime createdAt;
    private String status; // PENDING, PROCESSING, COMPLETED, FAILED
    private String userId;
}
```

#### AnalysisReport
```java
@Entity
@Table(name = "analysis_reports")
public class AnalysisReport {
    @Id
    private String reportId;
    private String requestId;
    private String symbol;
    
    @Column(columnDefinition = "jsonb")
    private String newsAnalysis;
    
    @Column(columnDefinition = "jsonb")
    private String financialAnalysis;
    
    @Column(columnDefinition = "jsonb")
    private String riskAnalysis;
    
    @Column(columnDefinition = "jsonb")
    private String investmentAdvice;
    
    private LocalDateTime generatedAt;
}
```

#### AgentExecution
```java
@Entity
@Table(name = "agent_executions")
public class AgentExecution {
    @Id
    private String id;
    private String reportId;
    private String agentName;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private String status;
    private String errorMessage;
    
    @Column(columnDefinition = "jsonb")
    private String input;
    
    @Column(columnDefinition = "jsonb")
    private String output;
}
```

---

## 7. 部署架构

### 7.1 Docker Compose配置

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: stock_analysis
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"

  spring-boot-app:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/stock_analysis
      SPRING_REDIS_HOST: redis
      RABBITMQ_HOST: rabbitmq
      CLAUDE_API_KEY: ${CLAUDE_API_KEY}
    depends_on:
      - postgres
      - redis
      - rabbitmq

  vue-frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - spring-boot-app

volumes:
  postgres_data:
```

### 7.2 Kubernetes部署（可选）

提供Deployment、Service、Ingress等配置文件用于生产环境部署。

---

## 8. 开发规范

### 8.1 代码结构

```
xai/
├── backend/
│   ├── src/main/java/com/xai/
│   │   ├── controller/
│   │   │   ├── StockAnalysisController.java
│   │   │   └── AgentController.java
│   │   ├── service/
│   │   │   ├── AgentOrchestratorService.java
│   │   │   ├── StockDataService.java
│   │   │   └── LLMService.java
│   │   ├── agent/
│   │   │   ├── AgentGateway.java
│   │   │   ├── PlannerAgent.java
│   │   │   ├── NewsAgent.java
│   │   │   ├── FinancialAgent.java
│   │   │   ├── RiskAgent.java
│   │   │   ├── InvestmentAgent.java
│   │   │   └── ReportAgent.java
│   │   ├── model/
│   │   │   ├── entity/
│   │   │   └── dto/
│   │   ├── repository/
│   │   ├── config/
│   │   └── util/
│   ├── src/main/resources/
│   │   ├── application.yml
│   │   └── langgraph/
│   │       └── workflow.py
│   └── pom.xml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── store/
│   │   ├── api/
│   │   └── App.vue
│   └── package.json
├── docker-compose.yml
└── README.md
```

### 8.2 命名规范

- **类名**: PascalCase (例: `StockAnalysisController`)
- **方法名**: camelCase (例: `analyzeStock`)
- **常量**: UPPER_SNAKE_CASE (例: `MAX_RETRY_COUNT`)
- **包名**: lowercase (例: `com.xai.agent`)

### 8.3 日志规范

```java
@Slf4j
public class NewsAgent {
    public NewsAnalysisResult analyze(String symbol) {
        log.info("Starting news analysis for symbol: {}", symbol);
        try {
            // 业务逻辑
            log.debug("Fetched {} news articles", articles.size());
            return result;
        } catch (Exception e) {
            log.error("News analysis failed for symbol: {}", symbol, e);
            throw new AgentExecutionException("News analysis failed", e);
        }
    }
}
```

---

## 9. 安全性设计

### 9.1 API安全
- **认证**: JWT Token
- **授权**: Role-Based Access Control (RBAC)
- **限流**: 使用Bucket4j或Spring Cloud Gateway限流
- **HTTPS**: 生产环境强制HTTPS

### 9.2 数据安全
- **敏感数据加密**: API Key使用环境变量或密钥管理服务
- **SQL注入防护**: 使用JPA/MyBatis参数化查询
- **XSS防护**: 前端输入校验和输出转义

### 9.3 LLM安全
- **Prompt注入防护**: 对用户输入进行清洗
- **输出验证**: 验证LLM输出的格式和内容
- **成本控制**: 设置token使用上限

---

## 10. 监控与运维

### 10.1 监控指标

- **系统指标**: CPU、内存、磁盘使用率
- **应用指标**: API响应时间、错误率、吞吐量
- **Agent指标**: 各Agent执行时间、成功率、失败原因
- **LLM指标**: Token消耗、API调用次数、成本

### 10.2 日志管理

- **集中式日志**: ELK Stack (Elasticsearch + Logstash + Kibana)
- **日志级别**: ERROR, WARN, INFO, DEBUG
- **结构化日志**: JSON格式

### 10.3 告警

- **Agent失败**: Agent执行失败超过阈值
- **API异常**: API错误率 > 5%
- **资源告警**: CPU/内存使用 > 80%
- **LLM成本**: 每日Token消耗超预算

---

## 11. 测试策略

### 11.1 单元测试
- 使用JUnit 5 + Mockito
- 覆盖率目标: > 80%
- 重点测试Agent逻辑和Service层

### 11.2 集成测试
- 使用Testcontainers进行数据库测试
- 测试Agent之间的交互
- 测试LangGraph工作流

### 11.3 端到端测试
- 使用Selenium或Playwright
- 测试完整的用户场景

---

## 12. 开发路线图

### Phase 1: 基础框架 (2周)
- [ ] Spring Boot项目搭建
- [ ] 数据库设计与初始化
- [ ] 基础API框架
- [ ] Docker环境配置

### Phase 2: Agent开发 (4周)
- [ ] 实现Agent Gateway
- [ ] 实现Planner Agent
- [ ] 实现News Agent
- [ ] 实现Financial Agent
- [ ] 实现Risk Agent
- [ ] 实现Investment Agent
- [ ] 实现Report Agent

### Phase 3: LangGraph集成 (2周)
- [ ] LangGraph工作流设计
- [ ] Agent编排实现
- [ ] 状态管理
- [ ] 错误处理

### Phase 4: 前端开发 (3周)
- [ ] Vue3项目搭建
- [ ] 主要页面开发
- [ ] 数据可视化
- [ ] API集成

### Phase 5: 测试与优化 (2周)
- [ ] 单元测试
- [ ] 集成测试
- [ ] 性能优化
- [ ] 安全加固

### Phase 6: 部署上线 (1周)
- [ ] 生产环境配置
- [ ] 监控告警配置
- [ ] 文档完善
- [ ] 发布上线

---

## 13. 参考资源

### 技术文档
- [Spring Boot官方文档](https://spring.io/projects/spring-boot)
- [LangGraph文档](https://langchain-ai.github.io/langgraph/)
- [Claude API文档](https://docs.anthropic.com/)
- [Vue3官方文档](https://vuejs.org/)

### 数据源
- [Yahoo Finance API](https://www.yahoofinanceapi.com/)
- [Alpha Vantage](https://www.alphavantage.co/)
- [NewsAPI](https://newsapi.org/)

---

## 14. 常见问题

### Q1: 如何选择大模型？
**A**: 根据任务复杂度选择：
- Claude Opus/Sonnet: 复杂推理任务（投资建议、风险评估）
- Claude Haiku: 简单任务（数据提取、分类）
- 混合使用以平衡成本和性能

### Q2: Agent执行失败如何处理？
**A**: 实现重试机制和降级策略：
- 单个Agent失败不影响其他Agent
- 3次重试后标记失败
- 提供部分结果（如果可能）

### Q3: 如何控制LLM成本？
**A**: 
- 使用缓存减少重复调用
- 选择合适的模型（不总是用最大的模型）
- 设置token使用上限
- 监控和预算告警

---

## 15. 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

---

## 16. 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

---

**最后更新**: 2026-06-17  
**维护者**: AI Agent Team  
**联系方式**: team@xai.com
