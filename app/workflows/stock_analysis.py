"""
LangGraph工作流 - 股票分析
"""
from typing import Dict, Any, TypedDict, List
from langgraph.graph import StateGraph, END
from app.agents.planner import planner_agent
from app.agents.news import news_agent
from app.agents.financial import financial_agent
from app.agents.risk import risk_agent
from app.agents.investment import investment_agent
from app.agents.report import report_agent
import logging
import asyncio

logger = logging.getLogger(__name__)


class AnalysisState(TypedDict):
    """分析状态"""
    stock_symbol: str
    request_id: str
    plan: Dict[str, Any]
    news_data: Dict[str, Any]
    financial_data: Dict[str, Any]
    risk_data: Dict[str, Any]
    investment_advice: Dict[str, Any]
    report: Dict[str, Any]
    errors: List[str]


def create_stock_analysis_workflow():
    """
    创建股票分析工作流

    Returns:
        编译后的LangGraph应用
    """
    # 创建状态图
    workflow = StateGraph(AnalysisState)

    # 添加Agent节点
    workflow.add_node("planner", lambda state: asyncio.run(planner_agent.run(state)))
    workflow.add_node("news", lambda state: asyncio.run(news_agent.run(state)))
    workflow.add_node("financial", lambda state: asyncio.run(financial_agent.run(state)))
    workflow.add_node("risk", lambda state: asyncio.run(risk_agent.run(state)))
    workflow.add_node("investment", lambda state: asyncio.run(investment_agent.run(state)))
    workflow.add_node("report", lambda state: asyncio.run(report_agent.run(state)))

    # 定义流程
    workflow.set_entry_point("planner")

    # Planner之后，并行执行News和Financial
    workflow.add_edge("planner", "news")
    workflow.add_edge("planner", "financial")

    # News和Financial都完成后，执行Risk
    workflow.add_edge("news", "risk")
    workflow.add_edge("financial", "risk")

    # Risk完成后，执行Investment
    workflow.add_edge("risk", "investment")

    # Investment完成后，执行Report
    workflow.add_edge("investment", "report")

    # Report完成后，结束
    workflow.add_edge("report", END)

    # 编译工作流
    app = workflow.compile()

    logger.info("[Workflow] 股票分析工作流已创建")

    return app


async def run_stock_analysis_workflow(
    stock_symbol: str,
    request_id: str
) -> Dict[str, Any]:
    """
    运行股票分析工作流

    Args:
        stock_symbol: 股票代码
        request_id: 请求ID

    Returns:
        完整的分析结果
    """
    logger.info(f"[Workflow] 开始分析 {stock_symbol}, request_id={request_id}")

    # 初始化状态
    initial_state: AnalysisState = {
        "stock_symbol": stock_symbol,
        "request_id": request_id,
        "plan": {},
        "news_data": {},
        "financial_data": {},
        "risk_data": {},
        "investment_advice": {},
        "report": {},
        "errors": []
    }

    # 创建工作流
    app = create_stock_analysis_workflow()

    # 执行工作流
    try:
        # 注意：LangGraph的异步执行需要特殊处理
        # 这里我们手动执行各个节点以实现真正的并行
        final_state = await execute_workflow_async(initial_state)

        logger.info(f"[Workflow] 分析完成 {stock_symbol}")

        return final_state

    except Exception as e:
        logger.error(f"[Workflow] 工作流执行失败: {str(e)}", exc_info=True)
        initial_state["errors"].append(f"Workflow error: {str(e)}")
        return initial_state


async def execute_workflow_async(state: AnalysisState) -> AnalysisState:
    """
    异步执行工作流（支持真正的并行）

    Args:
        state: 初始状态

    Returns:
        最终状态
    """
    # 1. Planner Agent
    state = await planner_agent.run(state)

    # 2. 并行执行 News 和 Financial
    news_task = news_agent.run(state.copy())
    financial_task = financial_agent.run(state.copy())

    news_state, financial_state = await asyncio.gather(news_task, financial_task)

    # 合并结果
    state["news_data"] = news_state["news_data"]
    state["financial_data"] = financial_state["financial_data"]
    state["errors"].extend(news_state.get("errors", []))
    state["errors"].extend(financial_state.get("errors", []))

    # 3. Risk Agent
    state = await risk_agent.run(state)

    # 4. Investment Agent
    state = await investment_agent.run(state)

    # 5. Report Agent
    state = await report_agent.run(state)

    return state


# 全局工作流实例（可选，用于单例模式）
_workflow_instance = None


def get_workflow():
    """获取工作流单例"""
    global _workflow_instance
    if _workflow_instance is None:
        _workflow_instance = create_stock_analysis_workflow()
    return _workflow_instance
