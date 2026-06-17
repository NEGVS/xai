"""
Agent相关的数据模型
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class AgentType(str, Enum):
    """Agent类型"""
    GATEWAY = "gateway"
    PLANNER = "planner"
    NEWS = "news"
    FINANCIAL = "financial"
    RISK = "risk"
    INVESTMENT = "investment"
    REPORT = "report"


class AgentStatus(str, Enum):
    """Agent执行状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class AnalysisState(BaseModel):
    """LangGraph状态模型"""
    stock_symbol: str
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.now)

    # 各Agent的输出
    plan: Optional[Dict[str, Any]] = None
    news_data: Optional[Dict[str, Any]] = None
    financial_data: Optional[Dict[str, Any]] = None
    risk_data: Optional[Dict[str, Any]] = None
    investment_advice: Optional[Dict[str, Any]] = None
    report: Optional[Dict[str, Any]] = None

    # 错误追踪
    errors: List[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "stock_symbol": "AAPL",
                "request_id": "req_123456",
                "plan": {"strategy": "full_analysis"},
                "errors": []
            }
        }


class AgentExecutionResult(BaseModel):
    """Agent执行结果"""
    agent_type: AgentType
    status: AgentStatus
    output: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_time: float  # 秒
    timestamp: datetime = Field(default_factory=datetime.now)


class NewsAnalysisResult(BaseModel):
    """新闻分析结果"""
    news_summary: str
    sentiment_score: float = Field(ge=-1.0, le=1.0, description="情感分数 [-1, 1]")
    key_events: List[str]
    impact_level: str = Field(pattern="^(low|medium|high)$")
    articles_count: int
    sources: List[str]


class FinancialAnalysisResult(BaseModel):
    """财务分析结果"""
    current_price: float
    price_change_1d: str
    price_change_5d: Optional[str] = None

    technical_indicators: Dict[str, Any] = Field(
        description="技术指标: MA_50, MA_200, RSI, MACD等"
    )

    financial_health: Dict[str, Any] = Field(
        description="财务健康度: PE ratio, debt_to_equity, score等"
    )

    volume: int
    market_cap: Optional[float] = None


class RiskAnalysisResult(BaseModel):
    """风险分析结果"""
    risk_level: str = Field(pattern="^(low|medium|high)$")
    volatility: float = Field(description="波动率")
    var_95: float = Field(description="95% VaR")
    risk_factors: List[str]
    risk_score: float = Field(ge=0.0, le=10.0, description="风险评分 [0-10]")


class InvestmentAdviceResult(BaseModel):
    """投资建议结果"""
    recommendation: str = Field(pattern="^(BUY|HOLD|SELL)$")
    confidence: float = Field(ge=0.0, le=1.0, description="置信度 [0-1]")
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None
    time_horizon: str = Field(description="投资时间范围，如 '3M', '6M', '1Y'")
    reasoning: str = Field(description="投资建议的详细理由")


class AnalysisReport(BaseModel):
    """完整分析报告"""
    report_id: str
    stock_symbol: str
    timestamp: datetime
    executive_summary: str

    news: Optional[NewsAnalysisResult] = None
    financial: Optional[FinancialAnalysisResult] = None
    risk: Optional[RiskAnalysisResult] = None
    investment: Optional[InvestmentAdviceResult] = None

    charts: List[str] = Field(
        default_factory=list,
        description="建议图表类型"
    )

    execution_time: float = Field(description="总执行时间（秒）")
