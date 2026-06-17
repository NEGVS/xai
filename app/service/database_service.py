"""
数据库服务层
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.model.database_models import (
    StockAnalysisRequest,
    AnalysisReport,
    AgentExecution,
    AnalysisStatus
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DatabaseService:
    """数据库服务"""

    @staticmethod
    def create_analysis_request(
        db: Session,
        request_id: str,
        symbol: str,
        analysis_type: str,
        time_range: str,
        user_id: Optional[str] = None
    ) -> StockAnalysisRequest:
        """
        创建分析请求记录

        Args:
            db: 数据库会话
            request_id: 请求ID
            symbol: 股票代码
            analysis_type: 分析类型
            time_range: 时间范围
            user_id: 用户ID（可选）

        Returns:
            分析请求对象
        """
        request = StockAnalysisRequest(
            id=request_id,
            symbol=symbol,
            analysis_type=analysis_type,
            time_range=time_range,
            user_id=user_id,
            status=AnalysisStatus.PROCESSING
        )
        db.add(request)
        db.commit()
        db.refresh(request)

        logger.info(f"[DB] 创建分析请求: {request_id} ({symbol})")
        return request

    @staticmethod
    def update_request_status(
        db: Session,
        request_id: str,
        status: AnalysisStatus,
        error_message: Optional[str] = None
    ):
        """更新请求状态"""
        request = db.query(StockAnalysisRequest).filter(
            StockAnalysisRequest.id == request_id
        ).first()

        if request:
            request.status = status
            request.updated_at = datetime.now()

            if status == AnalysisStatus.COMPLETED or status == AnalysisStatus.FAILED:
                request.completed_at = datetime.now()

            if error_message:
                request.error_message = error_message

            db.commit()
            logger.info(f"[DB] 更新请求状态: {request_id} -> {status}")

    @staticmethod
    def save_report(
        db: Session,
        report_data: dict
    ) -> AnalysisReport:
        """
        保存分析报告

        Args:
            db: 数据库会话
            report_data: 报告数据

        Returns:
            分析报告对象
        """
        report = AnalysisReport(
            report_id=report_data.get("report_id"),
            request_id=report_data.get("request_id", "unknown"),
            symbol=report_data.get("stock_symbol"),
            news_analysis=report_data.get("news"),
            financial_analysis=report_data.get("financial"),
            risk_analysis=report_data.get("risk"),
            investment_advice=report_data.get("investment"),
            executive_summary=report_data.get("executive_summary"),
            charts=report_data.get("charts"),
            execution_time=report_data.get("execution_time")
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        logger.info(f"[DB] 保存报告: {report.report_id}")
        return report

    @staticmethod
    def get_report_by_id(
        db: Session,
        report_id: str
    ) -> Optional[AnalysisReport]:
        """根据ID获取报告"""
        return db.query(AnalysisReport).filter(
            AnalysisReport.report_id == report_id
        ).first()

    @staticmethod
    def get_reports_by_symbol(
        db: Session,
        symbol: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[AnalysisReport]:
        """根据股票代码获取报告列表"""
        return db.query(AnalysisReport).filter(
            AnalysisReport.symbol == symbol
        ).order_by(
            AnalysisReport.generated_at.desc()
        ).limit(limit).offset(offset).all()

    @staticmethod
    def get_all_reports(
        db: Session,
        limit: int = 10,
        offset: int = 0
    ) -> List[AnalysisReport]:
        """获取所有报告列表"""
        return db.query(AnalysisReport).order_by(
            AnalysisReport.generated_at.desc()
        ).limit(limit).offset(offset).all()

    @staticmethod
    def record_agent_execution(
        db: Session,
        execution_id: str,
        report_id: str,
        request_id: str,
        agent_name: str,
        status: str,
        start_time: datetime,
        end_time: Optional[datetime] = None,
        input_data: Optional[dict] = None,
        output_data: Optional[dict] = None,
        error_message: Optional[str] = None
    ) -> AgentExecution:
        """记录Agent执行"""
        execution_duration = None
        if end_time and start_time:
            execution_duration = (end_time - start_time).total_seconds()

        execution = AgentExecution(
            id=execution_id,
            report_id=report_id,
            request_id=request_id,
            agent_name=agent_name,
            status=status,
            start_time=start_time,
            end_time=end_time,
            execution_duration=execution_duration,
            input_data=input_data,
            output_data=output_data,
            error_message=error_message
        )

        db.add(execution)
        db.commit()

        logger.debug(f"[DB] 记录Agent执行: {agent_name} ({execution_id})")
        return execution


# 全局服务实例
db_service = DatabaseService()
