"""
API请求和响应模型
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class AnalysisType(str, Enum):
    """分析类型"""
    FULL = "full"  # 完整分析
    QUICK = "quick"  # 快速分析（仅新闻+价格）
    DEEP = "deep"  # 深度分析（包含更多数据源）


class TimeRange(str, Enum):
    """时间范围"""
    ONE_DAY = "1D"
    ONE_WEEK = "1W"
    ONE_MONTH = "1M"
    THREE_MONTHS = "3M"
    SIX_MONTHS = "6M"
    ONE_YEAR = "1Y"


class StockAnalysisRequest(BaseModel):
    """股票分析请求"""
    symbol: str = Field(
        ...,
        description="股票代码，如 AAPL, TSLA",
        min_length=1,
        max_length=10
    )
    analysis_type: AnalysisType = Field(
        default=AnalysisType.FULL,
        description="分析类型"
    )
    time_range: TimeRange = Field(
        default=TimeRange.ONE_MONTH,
        description="分析时间范围"
    )
    include_news: bool = Field(default=True, description="是否包含新闻分析")
    include_financial: bool = Field(default=True, description="是否包含财务分析")
    include_risk: bool = Field(default=True, description="是否包含风险评估")

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "analysis_type": "full",
                "time_range": "1M",
                "include_news": True,
                "include_financial": True,
                "include_risk": True
            }
        }


class StockAnalysisResponse(BaseModel):
    """股票分析响应"""
    success: bool
    request_id: str
    message: Optional[str] = None
    data: Optional[dict] = None
    execution_time: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class AgentHealthStatus(BaseModel):
    """Agent健康状态"""
    agent_name: str
    status: str = Field(pattern="^(active|inactive|error)$")
    last_check: datetime
    error_message: Optional[str] = None


class SystemHealthResponse(BaseModel):
    """系统健康检查响应"""
    status: str = Field(pattern="^(healthy|degraded|unhealthy)$")
    agents: List[AgentHealthStatus]
    llm_status: str
    database_status: str
    cache_status: str
    timestamp: datetime = Field(default_factory=datetime.now)


class AnalysisHistoryQuery(BaseModel):
    """分析历史查询参数"""
    symbol: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class AnalysisHistoryItem(BaseModel):
    """分析历史项"""
    report_id: str
    symbol: str
    analysis_type: str
    timestamp: datetime
    status: str
    execution_time: float


class AnalysisHistoryResponse(BaseModel):
    """分析历史响应"""
    success: bool
    total: int
    items: List[AnalysisHistoryItem]
    timestamp: datetime = Field(default_factory=datetime.now)
