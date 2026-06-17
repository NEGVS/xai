"""
Agent状态和健康检查API
"""
from fastapi import APIRouter
from app.schemas.request import SystemHealthResponse, AgentHealthStatus
from app.agents.planner import planner_agent
from app.agents.news import news_agent
from app.agents.financial import financial_agent
from app.agents.risk import risk_agent
from app.agents.investment import investment_agent
from app.agents.report import report_agent
from app.core.llm import llm_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agents", tags=["Agent管理"])


@router.get("/health", response_model=SystemHealthResponse)
async def get_system_health():
    """
    系统健康检查

    Returns:
        系统健康状态
    """
    logger.info("[API] 执行健康检查")

    # 检查所有Agent
    agents = [
        planner_agent,
        news_agent,
        financial_agent,
        risk_agent,
        investment_agent,
        report_agent
    ]

    agent_statuses = []
    all_healthy = True

    for agent in agents:
        try:
            status_info = agent.get_status()
            agent_status = AgentHealthStatus(
                agent_name=status_info["name"],
                status="active",
                last_check=datetime.now(),
                error_message=None
            )
        except Exception as e:
            agent_status = AgentHealthStatus(
                agent_name=agent.name,
                status="error",
                last_check=datetime.now(),
                error_message=str(e)
            )
            all_healthy = False

        agent_statuses.append(agent_status)

    # 检查LLM服务
    try:
        llm_client = llm_service.get_client()
        llm_status = "connected" if llm_client else "disconnected"
    except Exception as e:
        llm_status = f"error: {str(e)}"
        all_healthy = False

    # 数据库状态（TODO: 实现真实检查）
    database_status = "not_configured"

    # 缓存状态（TODO: 实现真实检查）
    cache_status = "not_configured"

    # 确定整体状态
    if all_healthy and llm_status == "connected":
        overall_status = "healthy"
    elif all_healthy:
        overall_status = "degraded"
    else:
        overall_status = "unhealthy"

    return SystemHealthResponse(
        status=overall_status,
        agents=agent_statuses,
        llm_status=llm_status,
        database_status=database_status,
        cache_status=cache_status
    )


@router.get("/status")
async def get_agents_status():
    """
    获取所有Agent的详细状态

    Returns:
        Agent状态列表
    """
    logger.info("[API] 获取Agent状态")

    agents = [
        planner_agent,
        news_agent,
        financial_agent,
        risk_agent,
        investment_agent,
        report_agent
    ]

    statuses = []
    for agent in agents:
        try:
            status = agent.get_status()
            statuses.append(status)
        except Exception as e:
            statuses.append({
                "name": agent.name,
                "error": str(e)
            })

    return {
        "success": True,
        "agents": statuses,
        "timestamp": datetime.now().isoformat()
    }
