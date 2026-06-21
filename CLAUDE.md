# Spring Boot + LangGraph + Multi-Agent 股票分析系统 - 设计文档


# 使用的模型

    def __init__(
            self,
            api_key: Optional[str] = None,
            base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1",
            default_model: str = "qwen3.5-plus",
            fallback_models: List[str] = ["qwen3.5-plus", "qwen-turbo"],
    ):
      
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.base_url = base_url
        self.default_model = default_model
        self.fallback_models = fallback_models

        if not self.api_key:
            raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量，或在初始化时传入 api_key 参数")

后面的项目只是使用 DASHSCOPE_API_KEY 的模型（已经配置到设备的环境变量了），之前使用其他的是 临时、测试使用。

# 必须做到：
你是顶尖软件工程师，你只需要写好代码即可，没有让你测试、总结时请不要测试、总结 这个过程太浪费时间了。你只需正确无误的写好代码，需要测试、总结时我会告诉你。

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
## 环境管理
Conda 管 Python 版本 + 全局环境隔离，UV 管项目依赖、极速安装

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

# 项目设计文档
.claude/design.md
.claude/plan.md