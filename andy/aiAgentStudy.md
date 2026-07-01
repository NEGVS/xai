(xai) andy_mac@Andy-

🌐 启动 FastAPI 服务...
📝 API文档: http://localhost:8000/docs
🏥 健康检查: http://localhost:8000/api/v1/agents/health

按 Ctrl+C 停止服务

INFO:     Will watch for changes in these directories: ['/Users/andy_mac/PycharmProjects/xai']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [86964] using WatchFiles
INFO:     Started server process [86982]
INFO:     Waiting for application startup.
2026-06-21 13:33:48,652 - app.main - INFO - 🚀 Stock Analysis Multi-Agent System v0.1.0 启动中...
2026-06-21 13:33:48,652 - app.main - INFO - 📝 环境: development
2026-06-21 13:33:48,652 - app.main - INFO - 🔗 API文档: http://0.0.0.0:8000/docs
2026-06-21 13:33:48,652 - app.main - INFO - 🤖 LLM: gpt-4
INFO:     Application startup complete.
2026-06-21 13:34:52,153 - watchfiles.main - INFO - 70 changes detected
2026-06-21 13:34:55,910 - watchfiles.main - INFO - 4 changes detected
INFO:     127.0.0.1:56835 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:56835 - "GET /openapi.json HTTP/1.1" 200 OK
2026-06-21 13:35:55,480 - watchfiles.main - INFO - 3 changes detected
2026-06-21 13:36:08,332 - app.api.v1.agents - INFO - [API] 执行健康检查
INFO:     127.0.0.1:57281 - "GET /api/v1/agents/health HTTP/1.1" 200 OK
INFO:     127.0.0.1:57281 - "GET /favicon.ico HTTP/1.1" 404 Not Found
2026-06-21 13:36:41,714 - app.api.v1.agents - INFO - [API] 执行健康检查
INFO:     127.0.0.1:57605 - "GET /api/v1/agents/health HTTP/1.1" 200 OK
INFO:     127.0.0.1:57710 - "GET / HTTP/1.1" 200 OK
2026-06-21 13:39:25,785 - watchfiles.main - INFO - 1 change detected
2026-06-21 13:39:29,149 - watchfiles.main - INFO - 5 changes detected

2026-06-21 13:39:34,768 - watchfiles.main - INFO - 3 changes detected
2026-06-21 13:44:47,541 - watchfiles.main - INFO - 3 changes detected

2026-06-21 13:45:04,569 - app.api.v1.stock - INFO - [API] 收到股票分析请求: AAPL, request_id=b24ad5a5-6685-4850-8d96-339e18087962
2026-06-21 13:45:04,570 - app.workflows.stock_analysis - INFO - [Workflow] 开始分析 AAPL, request_id=b24ad5a5-6685-4850-8d96-339e18087962
2026-06-21 13:45:04,575 - app.workflows.stock_analysis - INFO - [Workflow] 股票分析工作流已创建
2026-06-21 13:45:04,575 - app.agents.base - INFO - [PlannerAgent] 开始执行
2026-06-21 13:45:04,575 - app.agents.planner - INFO - [PlannerAgent] 为 AAPL 生成执行计划
2026-06-21 13:45:04,575 - app.agents.planner - INFO - [PlannerAgent] 执行计划已生成: full_analysis
2026-06-21 13:45:04,575 - app.agents.base - INFO - [PlannerAgent] 执行完成，耗时: 0.00秒
2026-06-21 13:45:04,576 - app.agents.base - INFO - [NewsAgent] 开始执行
2026-06-21 13:45:04,576 - app.agents.news - INFO - [NewsAgent] 为 AAPL 收集新闻
2026-06-21 13:45:04,576 - app.tools.news_fetcher - WARNING - [NewsFetcher] 未配置NEWS_API_KEY，使用模拟数据
2026-06-21 13:45:04,591 - app.agents.base - INFO - [FinancialAgent] 开始执行
2026-06-21 13:45:04,591 - app.agents.financial - INFO - [FinancialAgent] 为 AAPL 分析财务数据
2026-06-21 13:45:04,673 - watchfiles.main - INFO - 12 changes detected
2026-06-21 13:45:08,520 - watchfiles.main - INFO - 4 changes detected
2026-06-21 13:45:09,293 - app.agents.financial - INFO - [FinancialAgent] 分析完成: 当前价格=$298.01, 健康评分=4.5
2026-06-21 13:45:09,293 - app.agents.base - INFO - [FinancialAgent] 执行完成，耗时: 4.70秒
2026-06-21 13:45:09,427 - watchfiles.main - INFO - 7 changes detected
2026-06-21 13:45:13,304 - httpx - INFO - HTTP Request: POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions "HTTP/1.1 200 OK"
2026-06-21 13:45:15,382 - httpx - INFO - HTTP Request: POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions "HTTP/1.1 200 OK"
2026-06-21 13:45:18,186 - httpx - INFO - HTTP Request: POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions "HTTP/1.1 200 OK"
2026-06-21 13:45:18,189 - app.agents.news - INFO - [NewsAgent] 分析完成: 5篇新闻, 情感分数: 0.72, 影响级别: high
2026-06-21 13:45:18,190 - app.agents.base - INFO - [NewsAgent] 执行完成，耗时: 13.61秒
2026-06-21 13:45:18,190 - app.agents.base - INFO - [RiskAgent] 开始执行
2026-06-21 13:45:18,190 - app.agents.risk - INFO - [RiskAgent] 为 AAPL 评估风险
2026-06-21 13:45:18,390 - app.agents.risk - INFO - [RiskAgent] 评估完成: 风险级别=medium, 波动率=0.2286, 风险评分=5.56
2026-06-21 13:45:18,390 - app.agents.base - INFO - [RiskAgent] 执行完成，耗时: 0.20秒
2026-06-21 13:45:18,390 - app.agents.base - INFO - [InvestmentAgent] 开始执行
2026-06-21 13:45:18,390 - app.agents.investment - INFO - [InvestmentAgent] 为 AAPL 生成投资建议
2026-06-21 13:45:27,038 - httpx - INFO - HTTP Request: POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions "HTTP/1.1 200 OK"
2026-06-21 13:45:27,042 - app.agents.investment - INFO - [InvestmentAgent] 建议生成: BUY, 置信度: 0.82
2026-06-21 13:45:27,042 - app.agents.base - INFO - [InvestmentAgent] 执行完成，耗时: 8.65秒
2026-06-21 13:45:27,042 - app.agents.base - INFO - [ReportAgent] 开始执行
2026-06-21 13:45:27,042 - app.agents.report - INFO - [ReportAgent] 为 AAPL 生成最终报告
2026-06-21 13:45:33,941 - httpx - INFO - HTTP Request: POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions "HTTP/1.1 200 OK"
2026-06-21 13:45:33,945 - app.agents.report - INFO - [ReportAgent] 报告生成完成: RPT-20260621-AAPL-b24ad5
2026-06-21 13:45:33,945 - app.agents.base - INFO - [ReportAgent] 执行完成，耗时: 6.90秒
2026-06-21 13:45:33,945 - app.workflows.stock_analysis - INFO - [Workflow] 分析完成 AAPL
2026-06-21 13:45:33,945 - app.api.v1.stock - INFO - [API] 分析成功: AAPL, 耗时: 29.38秒
INFO:     127.0.0.1:61755 - "POST /api/v1/analysis/stock HTTP/1.1" 200 OK

❯ 我要参加面试，请根据 Spring Cloud + LangGraph + Multi-Agent 智能招聘系统 使用的技术，准备面试文档，放到/andy/study/interview-1.md                                                       
  然后帮我出20到AI Agent开发专家高频面试题，最后给出面试题的详细、专业回答



❯ 我要参加面试，请根据 Spring Boot + LangGraph + Multi-Agent 股票分析系统 使用的技术，准备面试文档，放到andy/interview.md                                                       
  你也可以帮我出20到AI Agent开发专家面试题，最后给出面试题的详细、专业回答                                                                                                   

⏺ 我来为你创建AI Agent开发专家面试文档：

  AI Agent开发专家面试文档

  项目技术栈概览
  
  后端技术

  - Spring Boot 3.x - 企业级Java应用框架
  - Java 17+ - 现代Java特性
  - LangGraph - AI Agent状态图编排框架
  - Multi-Agent Architecture - 多智能体协作系统

  AI/ML技术

  - 大模型集成: DASHSCOPE API (阿里云通义千问)
    - 主模型: qwen3.5-plus
    - 备用模型: qwen-turbo
  - Agent类型: Planner, News, Financial, Risk, Investment, Report

  数据层

  - PostgreSQL - 关系型数据库
  - Redis - 缓存与会话存储

  消息与异步

  - RabbitMQ - 消息队列

  前端技术

  - Vue 3 + TypeScript
  - Element Plus
  - Pinia - 状态管理
  - ECharts - 数据可视化

  DevOps

  - Docker + Docker Compose - 容器化
  - Kubernetes - 容器编排
  - 环境管理: Conda + UV

  ---
  20道AI Agent开发专家面试题
  
  第1题：什么是AI Agent？请解释Agent的核心组成部分。

  答案：

  AI Agent是一个能够感知环境、做出决策并采取行动以实现特定目标的智能系统。

  核心组成部分：

  1. 感知层(Perception)
    - 接收输入：用户查询、环境状态、传感器数据
    - 上下文理解：解析意图、提取关键信息
  2. 决策层(Reasoning)
    - 大语言模型(LLM)：核心推理引擎
    - 记忆系统：短期记忆(对话历史)、长期记忆(知识库)
    - 规划能力：制定多步骤执行计划
  3. 行动层(Action)
    - 工具调用(Tool Calling)：API、数据库查询、文件操作
    - 函数执行：结构化输出、计算任务
  4. 反馈循环(Feedback)
    - 观察执行结果
    - 自我反思与纠错
    - 迭代优化

  在股票分析系统中的体现：
  class StockAgent:
      def __init__(self):
          self.llm = ChatOpenAI()  # 决策引擎
          self.tools = [get_stock_price, get_news]  # 行动工具
          self.memory = ConversationBufferMemory()  # 记忆

  ---
  第2题：LangGraph与LangChain的区别是什么？为什么选择LangGraph做Agent编排？
  
  答案：

  LangChain特点：
  - 链式调用(Chain)：线性或简单分支流程
  - 适合单向数据流
  - 配置驱动，灵活性较低
  
  LangGraph优势：

  1. 状态图架构
    - 支持复杂的循环和条件分支
    - 节点(Node)代表Agent或函数
    - 边(Edge)定义状态转移逻辑
  2. 更强的控制能力
  from langgraph.graph import StateGraph

  workflow = StateGraph(AgentState)
  workflow.add_node("planner", planner_agent)
  workflow.add_node("executor", executor_agent)
  workflow.add_conditional_edges(
      "planner",
      should_continue,
      {
          "continue": "executor",
          "end": END
      }
  )
  3. 适合Multi-Agent场景
    - 支持Agent间消息传递
    - 状态共享与隔离
    - 并行执行控制
  4. 可观测性
    - 每个节点的输入输出可追踪
    - 便于调试和监控

  为什么选择LangGraph：
  股票分析系统需要多Agent协作（新闻分析→财务分析→风险评估→投资建议），涉及条件分支和循环反馈，LangGraph的状态图模型完美契合这种需求。

  ---
  第3题：请设计一个Multi-Agent股票分析系统的状态流转图。
  
  答案：

  ┌─────────┐
  │  START  │
  └────┬────┘
       │
       ▼
  ┌─────────────┐
  │   Planner   │  ← 分析用户问题，制定执行计划
  │   Agent     │
  └─────┬───────┘
        │
        ▼
  ┌─────────────────────────────────────┐
  │  Parallel Execution (并行执行)       │
  │                                     │
  │  ┌──────────┐    ┌───────────┐    │
  │  │  News    │    │ Financial │    │
  │  │  Agent   │    │  Agent    │    │
  │  └────┬─────┘    └─────┬─────┘    │
  └───────┼────────────────┼───────────┘
          │                │
          └────────┬───────┘
                   ▼
            ┌────────────┐
            │    Risk    │
            │    Agent   │
            └──────┬─────┘
                   │
                   ▼
            ┌────────────┐
            │ Investment │
            │   Agent    │
            └──────┬─────┘
                   │
                   ▼
            ┌────────────┐
            │   Report   │  ← 汇总生成最终报告
            │   Agent    │
            └──────┬─────┘
                   │
                   ▼
              ┌────────┐
              │  END   │
              └────────┘

  状态定义：
  from typing import TypedDict, List
  
  class AgentState(TypedDict):
      stock_symbol: str
      user_query: str
      plan: str
      news_analysis: dict
      financial_analysis: dict
      risk_assessment: dict
      investment_advice: dict
      final_report: str
      messages: List[str]
      
  关键设计点：
  1. Planner先行：理解用户意图，决定调用哪些Agent
  2. 并行加速：News和Financial可并行执行
  3. 依赖管理：Risk依赖前两者结果
  4. 报告汇总：最后统一生成结构化输出
  
  ---
  第4题：如何实现Agent之间的状态共享和通信？
  
  答案：

  方案1：共享状态对象（LangGraph推荐）

  from langgraph.graph import StateGraph

  class SharedState(TypedDict):
      stock_symbol: str
      context: dict
      intermediate_results: dict

  def news_agent(state: SharedState) -> SharedState:
      # 读取共享状态
      symbol = state["stock_symbol"]

      # 执行任务
      news_data = fetch_news(symbol)

      # 更新共享状态
      state["intermediate_results"]["news"] = news_data
      return state

  def financial_agent(state: SharedState) -> SharedState:
      # 可以访问news_agent的结果
      news_context = state["intermediate_results"].get("news")
      # ...
      return state

  方案2：消息传递机制

  class AgentMessage:
      sender: str
      receiver: str
      content: dict
      timestamp: datetime

  class MessageBus:
      def __init__(self):
          self.queue = deque()

      def send(self, msg: AgentMessage):
          self.queue.append(msg)

      def receive(self, agent_id: str) -> List[AgentMessage]:
          return [m for m in self.queue if m.receiver == agent_id]

  方案3：Redis作为中间状态存储

  import redis

  class StateManager:
      def __init__(self):
          self.redis_client = redis.Redis()

      def set_state(self, session_id: str, key: str, value: any):
          self.redis_client.hset(
              f"session:{session_id}",
              key,
              json.dumps(value)
          )

      def get_state(self, session_id: str, key: str):
          data = self.redis_client.hget(f"session:{session_id}", key)
          return json.loads(data) if data else None

  最佳实践：
  - 不可变更新：每个Agent返回新状态，避免副作用
  - 状态版本控制：记录状态变更历史
  - 超时机制：避免某个Agent阻塞整个流程

  ---
  第5题：如何处理Agent执行失败和错误恢复？
  
  答案：

  1. 重试机制（Retry Strategy）

  from tenacity import retry, stop_after_attempt, wait_exponential

  class RobustAgent:
      @retry(
          stop=stop_after_attempt(3),
          wait=wait_exponential(multiplier=1, min=2, max=10)
      )
      def execute_with_retry(self, task):
          try:
              return self.llm.invoke(task)
          except RateLimitError:
              # 切换到备用模型
              return self.fallback_llm.invoke(task)

  2. 降级策略（Fallback）

  class ModelManager:
      def __init__(self):
          self.primary = "qwen3.5-plus"
          self.fallbacks = ["qwen-turbo", "qwen-plus"]

      def invoke_with_fallback(self, prompt):
          for model in [self.primary] + self.fallbacks:
              try:
                  return self.call_model(model, prompt)
              except Exception as e:
                  logger.warning(f"{model} failed: {e}")
                  continue
          raise AllModelsFailed()

  3. 部分失败容忍

  def parallel_agents(state):
      results = {}
      agents = [news_agent, financial_agent, sentiment_agent]

      for agent in agents:
          try:
              results[agent.__name__] = agent(state)
          except Exception as e:
              logger.error(f"{agent.__name__} failed: {e}")
              results[agent.__name__] = None  # 允许部分失败

      # 至少需要2个成功
      if sum(1 for v in results.values() if v) < 2:
          raise InsufficientData()

      return results

  4. 补偿事务（Compensation）

  class WorkflowOrchestrator:
      def __init__(self):
          self.executed_steps = []

      def execute_with_compensation(self, steps):
          try:
              for step in steps:
                  result = step.execute()
                  self.executed_steps.append((step, result))
          except Exception:
              # 回滚已执行的步骤
              for step, result in reversed(self.executed_steps):
                  step.compensate(result)
              raise

  5. 断点续传（Checkpoint）

  class CheckpointManager:
      def save_checkpoint(self, session_id, state):
          with open(f"checkpoints/{session_id}.json", "w") as f:
              json.dump(state, f)

      def resume_from_checkpoint(self, session_id):
          with open(f"checkpoints/{session_id}.json") as f:
              return json.load(f)

  ---
  第6题：如何优化Agent的响应速度？
  
  答案：

  1. 并行执行

  import asyncio
  from concurrent.futures import ThreadPoolExecutor

  async def parallel_execution(tasks):
      # 异步并行
      results = await asyncio.gather(*[
          agent.async_execute(task) for task, agent in tasks
      ])
      return results

  # 或使用线程池
  with ThreadPoolExecutor(max_workers=5) as executor:
      futures = [executor.submit(agent.execute) for agent in agents]
      results = [f.result() for f in futures]

  2. 缓存策略

  from functools import lru_cache
  import hashlib

  class CachedAgent:
      def __init__(self, redis_client):
          self.cache = redis_client

      def execute(self, query):
          cache_key = hashlib.md5(query.encode()).hexdigest()

          # 检查缓存
          cached = self.cache.get(cache_key)
          if cached:
              return json.loads(cached)

          # 执行并缓存
          result = self.llm.invoke(query)
          self.cache.setex(cache_key, 3600, json.dumps(result))
          return result

  3. 流式输出（Streaming）

  def stream_agent_response(prompt):
      for chunk in llm.stream(prompt):
          yield chunk.content
          # 实时推送给前端
          websocket.send(chunk.content)

  4. 预热和预加载

  class AgentPool:
      def __init__(self):
          self.pool = [WarmAgent() for _ in range(5)]

      def get_agent(self):
          # 从池中获取已预热的Agent
          return self.pool.pop() if self.pool else WarmAgent()

  5. 模型选择优化

  class AdaptiveModelSelector:
      def select_model(self, task_complexity):
          if task_complexity < 0.3:
              return "qwen-turbo"  # 快速模型
          elif task_complexity < 0.7:
              return "qwen-plus"
          else:
              return "qwen3.5-plus"  # 复杂任务用强模型

  6. 提示词优化

  # 差：冗长的提示词
  prompt = """请分析以下股票...(500字)"""

  # 好：精简直接
  prompt = f"分析{symbol}股票的财务健康度，关注PE、ROE、负债率"

  实际效果：
  - 并行执行：3个Agent从15秒降到6秒
  - 缓存命中率60%：平均响应从5秒降到0.5秒
  - 流式输出：首字节时间从3秒降到0.8秒
  
  ---
  第7题：Tool Calling（工具调用）的实现原理是什么？
  
  答案：

  核心原理：

  Tool Calling是让LLM能够调用外部函数的机制，基于Function Calling能力实现。

  实现步骤：

  1. 定义工具Schema

  tools = [
      {
          "type": "function",
          "function": {
              "name": "get_stock_price",
              "description": "获取实时股票价格",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "symbol": {
                          "type": "string",
                          "description": "股票代码，如AAPL"
                      },
                      "market": {
                          "type": "string",
                          "enum": ["US", "HK", "CN"]
                      }
                  },
                  "required": ["symbol"]
              }
          }
      }
  ]

  2. LLM决策是否调用工具

  response = client.chat.completions.create(
      model="qwen3.5-plus",
      messages=[{"role": "user", "content": "查询苹果公司股价"}],
      tools=tools,
      tool_choice="auto"  # 让模型决定
  )

  # 模型输出
  {
      "role": "assistant",
      "content": null,
      "tool_calls": [{
          "id": "call_123",
          "type": "function",
          "function": {
              "name": "get_stock_price",
              "arguments": '{"symbol": "AAPL", "market": "US"}'
          }
      }]
  }

  3. 执行工具并返回结果

  def execute_tool_call(tool_call):
      func_name = tool_call.function.name
      args = json.loads(tool_call.function.arguments)

      # 映射到实际函数
      if func_name == "get_stock_price":
          result = get_stock_price(**args)
          return result

  # 将结果返回给模型
  messages.append({
      "role": "tool",
      "tool_call_id": "call_123",
      "content": json.dumps({"price": 178.32, "change": "+1.2%"})
  })

  # 模型生成最终回复
  final_response = client.chat.completions.create(
      model="qwen3.5-plus",
      messages=messages
  )

  4. LangChain封装

  from langchain.tools import tool

  @tool
  def get_stock_price(symbol: str, market: str = "US") -> dict:
      """获取实时股票价格
      
      Args:
          symbol: 股票代码
          market: 市场（US/HK/CN）
      """
      # 实际实现
      return {"price": 178.32, "change": "+1.2%"}

  # Agent自动调用
  agent = create_openai_functions_agent(llm, tools=[get_stock_price])
  result = agent.invoke("查询AAPL股价")

  关键点：
  - 工具描述要清晰：LLM靠description判断是否调用
  - 参数类型严格：避免类型错误
  - 错误处理：工具执行失败时返回明确错误信息

  ---
  第8题：如何设计Agent的Prompt模板？

  答案：

  优秀Prompt的特征：
  1. 角色定义清晰
  2. 任务目标明确
  3. 输出格式结构化
  4. 包含示例（Few-shot）
  5. 边界约束明确
  
  示例：Financial Agent的Prompt

  FINANCIAL_AGENT_PROMPT = """
  你是一位资深的股票财务分析师，拥有CFA资格认证，专注于上市公司财务健康度评估。

  ## 任务目标
  分析{stock_symbol}公司的财务状况，从以下维度评估：
  1. 盈利能力（净利润率、ROE、ROA）
  2. 偿债能力（资产负债率、流动比率）
  3. 成长性（营收增长率、利润增长率）
  4. 现金流健康度

  ## 输入数据
  {financial_data}

  ## 分析要求
  - 使用最近4个季度的数据
  - 与行业平均水平对比
  - 指出异常指标并解释原因
  - 给出1-10分的财务健康评分

  ## 输出格式（严格JSON）
  {{
      "profitability": {{
          "net_margin": 0.15,
          "roe": 0.20,
          "score": 8
      }},
      "solvency": {{
          "debt_ratio": 0.45,
          "current_ratio": 1.8,
          "score": 7
      }},
      "growth": {{
          "revenue_growth": 0.12,
          "profit_growth": 0.15,
          "score": 7
      }},
      "cashflow": {{
          "operating_cf": 5000000000,
          "score": 9
      }},
      "overall_score": 7.75,
      "summary": "简要总结（50字内）",
      "risks": ["风险点1", "风险点2"]
  }}

  ## 示例分析
  {few_shot_example}

  现在开始分析：
  """

  Prompt工程技巧：

  1. 使用Chain of Thought
  prompt = """
  请逐步分析：
  1. 首先识别关键财务指标
  2. 然后与行业对比
  3. 最后得出结论
  
  思考过程：
  """
  
  2. 角色强化
  system_prompt = """
  你是Warren Buffett的首席分析师，以价值投资视角分析企业。
  遵循原则：
  - 关注长期价值而非短期波动
  - 重视管理层质量
  - 寻找护城河
  """

  3. 输出格式约束
  # 使用Pydantic强制结构化
  from pydantic import BaseModel
  
  class FinancialAnalysis(BaseModel):
      overall_score: float
      profitability: dict
      summary: str
      
  # LangChain集成
  parser = PydanticOutputParser(pydantic_object=FinancialAnalysis)
  prompt = PromptTemplate(
      template="分析...\n{format_instructions}",
      partial_variables={"format_instructions": parser.get_format_instructions()}
  )   
  
  4. 上下文压缩
  # 差：包含所有原始数据
  prompt = f"分析这些数据：{raw_data_10000_chars}"
  
  # 好：预处理提取关键信息
  key_metrics = extract_key_metrics(raw_data)
  prompt = f"关键指标：PE={key_metrics.pe}, ROE={key_metrics.roe}..."

  ---
  第9题：如何实现Agent的记忆机制？
  
  答案：

  记忆类型：

  1. 短期记忆（对话历史）

  from langchain.memory import ConversationBufferMemory

  class ShortTermMemory:
      def __init__(self, max_messages=10):
          self.memory = ConversationBufferMemory(
              max_token_limit=2000,
              return_messages=True
          )

      def add_message(self, role, content):
          self.memory.chat_memory.add_message(
              HumanMessage(content=content) if role == "user"
              else AIMessage(content=content)
          )

      def get_context(self):
          return self.memory.load_memory_variables({})

  2. 工作记忆（当前任务状态）

  class WorkingMemory:
      def __init__(self):
          self.current_task = None
          self.intermediate_results = {}
          self.context_variables = {}

      def update(self, key, value):
          self.intermediate_results[key] = value

      def get_context_for_agent(self, agent_name):
          # 为每个Agent提供相关上下文
          if agent_name == "risk_agent":
              return {
                  "financial_analysis": self.intermediate_results.get("financial"),
                  "news_sentiment": self.intermediate_results.get("news")
              }

  3. 长期记忆（知识库）

  from langchain.vectorstores import Chroma
  from langchain.embeddings import OpenAIEmbeddings

  class LongTermMemory:
      def __init__(self):
          self.vectorstore = Chroma(
              embedding_function=OpenAIEmbeddings()
          )

      def store(self, text, metadata):
          self.vectorstore.add_texts(
              texts=[text],
              metadatas=[metadata]
          )

      def retrieve(self, query, k=5):
          return self.vectorstore.similarity_search(query, k=k)

      # 示例：存储历史分析结果
      def store_analysis(self, stock_symbol, analysis):
          self.store(
              text=f"{stock_symbol}分析: {analysis['summary']}",
              metadata={
                  "symbol": stock_symbol,
                  "timestamp": datetime.now().isoformat(),
                  "score": analysis["overall_score"]
              }
          )

  4. 混合记忆架构

  class HybridMemorySystem:
      def __init__(self):
          self.short_term = ConversationBufferMemory()
          self.long_term = Chroma()
          self.working_memory = {}

      def build_context(self, current_query):
          # 1. 获取对话历史
          conversation = self.short_term.load_memory_variables({})

          # 2. 从长期记忆检索相关知识
          relevant_docs = self.long_term.similarity_search(current_query, k=3)

          # 3. 合并上下文
          context = {
              "conversation_history": conversation,
              "relevant_knowledge": relevant_docs,
              "current_state": self.working_memory
          }

          return context

  5. 记忆压缩

  from langchain.memory import ConversationSummaryMemory

  class CompressedMemory:
      def __init__(self, llm):
          self.memory = ConversationSummaryMemory(llm=llm)

      def add_exchange(self, human_msg, ai_msg):
          # 超过阈值时自动总结
          if self.memory.token_count > 1000:
              self.memory.prune()  # 压缩旧对话

          self.memory.save_context(
              {"input": human_msg},
              {"output": ai_msg}
          )

  实际应用：

  class StockAnalysisAgent:
      def __init__(self):
          self.memory = HybridMemorySystem()

      def analyze(self, stock_symbol, user_query):
          # 构建上下文
          context = self.memory.build_context(user_query)

          # 检查是否之前分析过该股票
          history = self.memory.long_term.similarity_search(
              f"symbol:{stock_symbol}",
              k=1
          )

          if history and self._is_recent(history[0]):
              return f"基于{history[0].metadata['timestamp']}的分析..."

          # 执行新分析
          result = self.execute_analysis(stock_symbol, context)

          # 存储到长期记忆
          self.memory.long_term.store(result)
  
          return result

  ---
  第10题：如何将Python的LangGraph Agent集成到Spring Boot项目中？
  
  答案：

  方案1：HTTP API集成（推荐）

  Python端：FastAPI服务
  
  from fastapi import FastAPI
  from pydantic import BaseModel

  app = FastAPI()

  class AnalysisRequest(BaseModel):
      stock_symbol: str
      analysis_type: str

  @app.post("/api/agent/analyze")
  async def analyze_stock(request: AnalysisRequest):
      # 调用LangGraph Agent
      result = stock_agent_workflow.invoke({
          "stock_symbol": request.stock_symbol,
          "analysis_type": request.analysis_type
      })
  
      return {
          "status": "success",
          "data": result
      }

  if __name__ == "__main__":
      import uvicorn
      uvicorn.run(app, host="0.0.0.0", port=8000)

  Java端：Spring Boot调用

  @Service
  public class AgentOrchestratorService {

      @Value("${agent.python.url}")
      private String pythonAgentUrl;

      private final RestTemplate restTemplate;

      public StockAnalysisResult analyzeStock(String symbol) {
          String url = pythonAgentUrl + "/api/agent/analyze";

          AnalysisRequest request = new AnalysisRequest(symbol, "comprehensive");

          ResponseEntity<AgentResponse> response = restTemplate.postForEntity(
              url,
              request,
              AgentResponse.class
          );

          return parseResponse(response.getBody());
      }
  }
  
  方案2：消息队列异步集成

  Python端：RabbitMQ消费者

  import pika
  import json

  def callback(ch, method, properties, body):
      request = json.loads(body)

      # 执行Agent任务
      result = stock_agent_workflow.invoke(request)

      # 发布结果
      channel.basic_publish(
          exchange='',
          routing_key=properties.reply_to,
          body=json.dumps(result),
          properties=pika.BasicProperties(
              correlation_id=properties.correlation_id
          )
      )

      ch.basic_ack(delivery_tag=method.delivery_tag)

  channel.basic_consume(
      queue='agent_tasks',
      on_message_callback=callback
  )
  channel.start_consuming()

  Java端：RabbitMQ生产者

  @Service
  public class AsyncAgentService {

      @Autowired
      private RabbitTemplate rabbitTemplate;

      public CompletableFuture<StockAnalysisResult> analyzeAsync(String symbol) {
          CompletableFuture<StockAnalysisResult> future = new CompletableFuture<>();
          );

          // 监听结果队列
          rabbitTemplate.convertAndSend(
              "agent_tasks",
              new AnalysisRequest(symbol),
              message -> {
                  message.getMessageProperties().setCorrelationId(correlationId);
                  message.getMessageProperties().setReplyTo("agent_results");
                  return message;
              }
          );

          // 监听结果队列
          resultListener.registerCallback(correlationId, future);

          return future;
      }
  }

  方案3：gRPC高性能集成

  定义Protocol Buffer

  syntax = "proto3";

✻ Cogitated for 8m 47s

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
❯  
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  ⏵⏵ accept edits on (shift+tab to cycle) · ← for agents


