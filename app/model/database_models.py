"""
数据库模型
"""
from sqlalchemy import Column, String, DateTime, Integer, Float, JSON, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime
import enum


class AnalysisStatus(str, enum.Enum):
    """分析状态"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class StockAnalysisRequest(Base):
    """股票分析请求表"""
    __tablename__ = "stock_analysis_requests"

    id = Column(String(36), primary_key=True)
    symbol = Column(String(10), nullable=False, index=True)
    analysis_type = Column(String(20), nullable=False)
    time_range = Column(String(10), nullable=False)

    status = Column(
        SQLEnum(AnalysisStatus),
        default=AnalysisStatus.PENDING,
        nullable=False
    )

    user_id = Column(String(36), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    error_message = Column(Text, nullable=True)


class AnalysisReport(Base):
    """分析报告表"""
    __tablename__ = "analysis_reports"

    report_id = Column(String(50), primary_key=True)
    request_id = Column(String(36), nullable=False, index=True)
    symbol = Column(String(10), nullable=False, index=True)

    # JSON字段存储各部分分析结果
    news_analysis = Column(JSON, nullable=True)
    financial_analysis = Column(JSON, nullable=True)
    risk_analysis = Column(JSON, nullable=True)
    investment_advice = Column(JSON, nullable=True)

    # 执行摘要
    executive_summary = Column(Text, nullable=True)

    # 推荐的图表
    charts = Column(JSON, nullable=True)

    # 执行时间（秒）
    execution_time = Column(Float, nullable=True)

    generated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class AgentExecution(Base):
    """Agent执行记录表"""
    __tablename__ = "agent_executions"

    id = Column(String(36), primary_key=True)
    report_id = Column(String(50), nullable=False, index=True)
    request_id = Column(String(36), nullable=False, index=True)

    agent_name = Column(String(50), nullable=False)

    status = Column(String(20), nullable=False)

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)

    # 执行时间（秒）
    execution_duration = Column(Float, nullable=True)

    # 输入输出（JSON）
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)

    # 错误信息
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class UserPreference(Base):
    """用户偏好设置表（未来扩展）"""
    __tablename__ = "user_preferences"

    user_id = Column(String(36), primary_key=True)

    # 偏好设置（JSON）
    preferences = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
