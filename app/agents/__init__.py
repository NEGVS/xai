"""
更新__init__.py以导出所有Agent
"""
from app.agents.base import BaseAgent
from app.agents.planner import planner_agent
from app.agents.news import news_agent
from app.agents.financial import financial_agent
from app.agents.risk import risk_agent
from app.agents.investment import investment_agent
from app.agents.report import report_agent

__all__ = [
    "BaseAgent",
    "planner_agent",
    "news_agent",
    "financial_agent",
    "risk_agent",
    "investment_agent",
    "report_agent",
]
