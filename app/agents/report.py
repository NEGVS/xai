"""
Report Agent - 报告生成
"""
from typing import Dict, Any
from app.agents.base import BaseAgent
from app.core.llm import llm_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ReportAgent(BaseAgent):
    """报告Agent - 生成最终分析报告"""

    def __init__(self):
        super().__init__(
            name="ReportAgent",
            description="聚合所有Agent的输出，生成结构化分析报告"
        )

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成最终报告

        Args:
            state: 包含所有Agent输出的完整状态

        Returns:
            更新了report字段的状态
        """
        stock_symbol = state.get("stock_symbol")
        request_id = state.get("request_id")

        logger.info(f"[ReportAgent] 为 {stock_symbol} 生成最终报告")

        # 收集所有数据
        news_data = state.get("news_data", {})
        financial_data = state.get("financial_data", {})
        risk_data = state.get("risk_data", {})
        investment_advice = state.get("investment_advice", {})

        # 生成报告ID
        report_id = f"RPT-{datetime.now().strftime('%Y%m%d')}-{stock_symbol}-{request_id[:6]}"

        # 生成执行摘要
        try:
            full_data = {
                "stock_symbol": stock_symbol,
                "news": news_data,
                "financial": financial_data,
                "risk": risk_data,
                "investment": investment_advice
            }
            executive_summary = await llm_service.generate_report_summary(full_data)
        except Exception as e:
            logger.warning(f"[ReportAgent] LLM摘要生成失败: {str(e)}, 使用规则生成")
            executive_summary = self._generate_rule_based_summary(
                stock_symbol, news_data, financial_data, risk_data, investment_advice
            )

        # 确定推荐的图表类型
        charts = self._determine_charts(financial_data, risk_data)

        # 构建最终报告
        report = {
            "report_id": report_id,
            "stock_symbol": stock_symbol,
            "timestamp": datetime.now().isoformat(),
            "executive_summary": executive_summary,

            "news": {
                "summary": news_data.get("news_summary", "无新闻数据"),
                "sentiment_score": news_data.get("sentiment_score", 0.0),
                "key_events": news_data.get("key_events", []),
                "impact_level": news_data.get("impact_level", "unknown"),
                "articles_count": news_data.get("articles_count", 0),
                "sources": news_data.get("sources", [])
            },

            "financial": {
                "current_price": financial_data.get("current_price", 0),
                "price_change_1d": financial_data.get("price_change_1d", "N/A"),
                "price_change_5d": financial_data.get("price_change_5d", "N/A"),
                "volume": financial_data.get("volume", 0),
                "market_cap": financial_data.get("market_cap"),
                "technical_indicators": financial_data.get("technical_indicators", {}),
                "financial_health": financial_data.get("financial_health", {})
            },

            "risk": {
                "risk_level": risk_data.get("risk_level", "unknown"),
                "volatility": risk_data.get("volatility", 0.0),
                "var_95": risk_data.get("var_95", 0.0),
                "risk_factors": risk_data.get("risk_factors", []),
                "risk_score": risk_data.get("risk_score", 5.0)
            },

            "investment": {
                "recommendation": investment_advice.get("recommendation", "HOLD"),
                "confidence": investment_advice.get("confidence", 0.5),
                "target_price": investment_advice.get("target_price"),
                "stop_loss": investment_advice.get("stop_loss"),
                "time_horizon": investment_advice.get("time_horizon", "3M"),
                "reasoning": investment_advice.get("reasoning", "")
            },

            "charts": charts,
            "execution_time": 0.0  # 将在orchestrator中计算
        }

        state["report"] = report

        logger.info(f"[ReportAgent] 报告生成完成: {report_id}")

        return state

    def _generate_rule_based_summary(
        self,
        stock_symbol: str,
        news_data: Dict[str, Any],
        financial_data: Dict[str, Any],
        risk_data: Dict[str, Any],
        investment_advice: Dict[str, Any]
    ) -> str:
        """
        基于规则生成执行摘要

        Args:
            stock_symbol: 股票代码
            news_data: 新闻数据
            financial_data: 财务数据
            risk_data: 风险数据
            investment_advice: 投资建议

        Returns:
            执行摘要文本
        """
        current_price = financial_data.get("current_price", 0)
        price_change = financial_data.get("price_change_1d", "N/A")
        sentiment_score = news_data.get("sentiment_score", 0)
        risk_level = risk_data.get("risk_level", "未知")
        recommendation = investment_advice.get("recommendation", "HOLD")

        sentiment_desc = "正面" if sentiment_score > 0.3 else "负面" if sentiment_score < -0.3 else "中性"
        risk_desc = {"low": "较低", "medium": "中等", "high": "较高"}.get(risk_level, "未知")
        rec_desc = {"BUY": "买入", "HOLD": "持有", "SELL": "卖出"}.get(recommendation, "持有")

        summary = f"""
{stock_symbol} 股票分析报告

当前市场表现：
{stock_symbol} 当前价格为 ${current_price:.2f}，日内变化 {price_change}。

新闻与市场情绪：
基于对最近 {news_data.get('articles_count', 0)} 篇新闻的分析，市场情绪呈{sentiment_desc}态势（情感分数: {sentiment_score:.2f}）。
{f"关键事件包括：{', '.join(news_data.get('key_events', [])[:3])}" if news_data.get('key_events') else ""}

技术与基本面分析：
技术指标显示 RSI 为 {financial_data.get('technical_indicators', {}).get('RSI', 'N/A')}，
MACD 呈{financial_data.get('technical_indicators', {}).get('MACD', '未知')}趋势。
财务健康度评分为 {financial_data.get('financial_health', {}).get('score', 'N/A')}/10。

风险评估：
综合风险水平为{risk_desc}（风险评分: {risk_data.get('risk_score', 'N/A')}/10）。
主要风险因素：{', '.join(risk_data.get('risk_factors', [])[:2])}。

投资建议：
综合以上分析，建议{rec_desc}，置信度 {investment_advice.get('confidence', 0.5)*100:.0f}%。
{f"目标价位 ${investment_advice.get('target_price', 'N/A')}，" if investment_advice.get('target_price') else ""}
{f"止损价位 ${investment_advice.get('stop_loss', 'N/A')}。" if investment_advice.get('stop_loss') else ""}
        """.strip()

        return summary

    def _determine_charts(
        self,
        financial_data: Dict[str, Any],
        risk_data: Dict[str, Any]
    ) -> list:
        """
        确定推荐的图表类型

        Args:
            financial_data: 财务数据
            risk_data: 风险数据

        Returns:
            图表类型列表
        """
        charts = ["price_trend"]  # 价格走势是基础图表

        # 如果有技术指标数据，推荐技术指标图
        if financial_data.get("technical_indicators"):
            charts.append("technical_indicators")

        # 如果有风险数据，推荐风险分布图
        if risk_data.get("risk_factors"):
            charts.append("risk_distribution")

        # 推荐财务健康度雷达图
        if financial_data.get("financial_health"):
            charts.append("financial_health_radar")

        return charts


# 全局实例
report_agent = ReportAgent()
