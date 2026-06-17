"""
更新schemas __init__.py
"""
from app.schemas.agent import (
    AgentType,
    AgentStatus,
    AnalysisState,
    AgentExecutionResult,
    NewsAnalysisResult,
    FinancialAnalysisResult,
    RiskAnalysisResult,
    InvestmentAdviceResult,
    AnalysisReport,
)

from app.schemas.request import (
    AnalysisType,
    TimeRange,
    StockAnalysisRequest,
    StockAnalysisResponse,
    AgentHealthStatus,
    SystemHealthResponse,
    AnalysisHistoryQuery,
    AnalysisHistoryItem,
    AnalysisHistoryResponse,
)

__all__ = [
    # Agent schemas
    "AgentType",
    "AgentStatus",
    "AnalysisState",
    "AgentExecutionResult",
    "NewsAnalysisResult",
    "FinancialAnalysisResult",
    "RiskAnalysisResult",
    "InvestmentAdviceResult",
    "AnalysisReport",

    # Request schemas
    "AnalysisType",
    "TimeRange",
    "StockAnalysisRequest",
    "StockAnalysisResponse",
    "AgentHealthStatus",
    "SystemHealthResponse",
    "AnalysisHistoryQuery",
    "AnalysisHistoryItem",
    "AnalysisHistoryResponse",
]
