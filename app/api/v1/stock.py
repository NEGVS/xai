"""
股票分析API路由
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.request import (
    StockAnalysisRequest,
    StockAnalysisResponse,
    AnalysisHistoryQuery,
    AnalysisHistoryResponse
)
from app.workflows.stock_analysis import run_stock_analysis_workflow
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analysis", tags=["股票分析"])


@router.post("/stock", response_model=StockAnalysisResponse)
async def analyze_stock(request: StockAnalysisRequest):
    """
    执行股票分析

    Args:
        request: 股票分析请求

    Returns:
        分析结果
    """
    request_id = str(uuid.uuid4())

    logger.info(f"[API] 收到股票分析请求: {request.symbol}, request_id={request_id}")

    start_time = datetime.now()

    try:
        # 运行工作流
        result = await run_stock_analysis_workflow(
            stock_symbol=request.symbol.upper(),
            request_id=request_id
        )

        execution_time = (datetime.now() - start_time).total_seconds()

        # 更新执行时间
        if result.get("report"):
            result["report"]["execution_time"] = execution_time

        # 检查是否有错误
        if result.get("errors") and not result.get("report"):
            logger.error(f"[API] 分析失败: {result['errors']}")
            return StockAnalysisResponse(
                success=False,
                request_id=request_id,
                message=f"分析失败: {'; '.join(result['errors'])}",
                execution_time=execution_time
            )

        logger.info(f"[API] 分析成功: {request.symbol}, 耗时: {execution_time:.2f}秒")

        return StockAnalysisResponse(
            success=True,
            request_id=request_id,
            message="分析完成",
            data=result.get("report"),
            execution_time=execution_time
        )

    except Exception as e:
        logger.error(f"[API] 分析异常: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.get("/history", response_model=AnalysisHistoryResponse)
async def get_analysis_history(
    symbol: str = None,
    limit: int = 10,
    offset: int = 0
):
    """
    获取分析历史（TODO: 需要数据库支持）

    Args:
        symbol: 股票代码（可选）
        limit: 返回数量
        offset: 偏移量

    Returns:
        历史记录列表
    """
    # TODO: 从数据库查询
    # 目前返回空列表
    logger.info(f"[API] 查询历史记录: symbol={symbol}, limit={limit}, offset={offset}")

    return AnalysisHistoryResponse(
        success=True,
        total=0,
        items=[]
    )


@router.get("/report/{report_id}")
async def get_report(report_id: str):
    """
    获取单个报告（TODO: 需要数据库支持）

    Args:
        report_id: 报告ID

    Returns:
        报告详情
    """
    # TODO: 从数据库查询
    logger.info(f"[API] 查询报告: {report_id}")

    raise HTTPException(status_code=404, detail="报告未找到（数据库未实现）")
