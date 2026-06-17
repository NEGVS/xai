"""
Financial Agent - 财务数据分析
"""
from typing import Dict, Any
from app.agents.base import BaseAgent
from app.tools.stock_api import stock_data_tool
import logging

logger = logging.getLogger(__name__)


class FinancialAgent(BaseAgent):
    """财务Agent - 分析股票财务数据和技术指标"""

    def __init__(self):
        super().__init__(
            name="FinancialAgent",
            description="获取并分析股票价格、财务指标和技术指标"
        )

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行财务分析

        Args:
            state: 包含stock_symbol的状态

        Returns:
            更新了financial_data字段的状态
        """
        stock_symbol = state.get("stock_symbol")
        logger.info(f"[FinancialAgent] 为 {stock_symbol} 分析财务数据")

        # 1. 获取当前价格和基本数据
        price_data = stock_data_tool.get_current_price(stock_symbol)

        if "error" in price_data:
            logger.error(f"[FinancialAgent] 获取价格数据失败: {price_data['error']}")
            state["financial_data"] = {"error": price_data["error"]}
            state["errors"].append(f"FinancialAgent: {price_data['error']}")
            return state

        # 2. 获取财务指标
        financial_metrics = stock_data_tool.get_financial_metrics(stock_symbol)

        # 3. 计算技术指标
        technical_indicators = stock_data_tool.calculate_technical_indicators(stock_symbol)

        # 4. 计算财务健康度评分
        health_score = self._calculate_health_score(financial_metrics, technical_indicators)

        # 5. 获取历史数据（用于趋势分析）
        historical_data = stock_data_tool.get_historical_data(stock_symbol, period="1mo")

        # 6. 计算价格变化
        if historical_data and "close" in historical_data:
            closes = historical_data["close"]
            if len(closes) >= 5:
                price_change_5d = ((closes[-1] - closes[-5]) / closes[-5] * 100)
                price_change_5d_str = f"{price_change_5d:+.2f}%"
            else:
                price_change_5d_str = "N/A"
        else:
            price_change_5d_str = "N/A"

        # 7. 构建结果
        financial_data = {
            "current_price": price_data.get("current_price", 0),
            "price_change_1d": price_data.get("price_change_1d", "N/A"),
            "price_change_5d": price_change_5d_str,
            "volume": price_data.get("volume", 0),
            "market_cap": price_data.get("market_cap"),
            "high_52w": price_data.get("high_52w"),
            "low_52w": price_data.get("low_52w"),

            "technical_indicators": {
                "MA_20": technical_indicators.get("MA_20"),
                "MA_50": technical_indicators.get("MA_50"),
                "MA_200": technical_indicators.get("MA_200"),
                "RSI": technical_indicators.get("RSI"),
                "MACD": technical_indicators.get("MACD"),
                "MACD_line": technical_indicators.get("MACD_line"),
                "Signal_line": technical_indicators.get("Signal_line"),
            },

            "financial_health": {
                "pe_ratio": financial_metrics.get("pe_ratio"),
                "pb_ratio": financial_metrics.get("pb_ratio"),
                "debt_to_equity": financial_metrics.get("debt_to_equity"),
                "roe": financial_metrics.get("roe"),
                "profit_margin": financial_metrics.get("profit_margin"),
                "score": health_score
            }
        }

        state["financial_data"] = financial_data

        logger.info(
            f"[FinancialAgent] 分析完成: 当前价格=${price_data.get('current_price', 0):.2f}, "
            f"健康评分={health_score:.1f}"
        )

        return state

    def _calculate_health_score(
        self,
        financial_metrics: Dict[str, Any],
        technical_indicators: Dict[str, Any]
    ) -> float:
        """
        计算财务健康度评分 (0-10)

        Args:
            financial_metrics: 财务指标
            technical_indicators: 技术指标

        Returns:
            健康度评分
        """
        score = 5.0  # 基础分

        # PE Ratio 评分 (较低更好)
        pe_ratio = financial_metrics.get("pe_ratio")
        if pe_ratio:
            if pe_ratio < 15:
                score += 1.0
            elif pe_ratio > 30:
                score -= 1.0

        # ROE 评分 (较高更好)
        roe = financial_metrics.get("roe")
        if roe:
            if roe > 0.15:  # 15%
                score += 1.0
            elif roe < 0.05:
                score -= 1.0

        # Debt to Equity 评分 (较低更好)
        debt_to_equity = financial_metrics.get("debt_to_equity")
        if debt_to_equity is not None:
            if debt_to_equity < 0.5:
                score += 1.0
            elif debt_to_equity > 2.0:
                score -= 1.0

        # Profit Margin 评分 (较高更好)
        profit_margin = financial_metrics.get("profit_margin")
        if profit_margin:
            if profit_margin > 0.2:  # 20%
                score += 1.0
            elif profit_margin < 0.05:
                score -= 1.0

        # RSI 评分 (50-70 为理想)
        rsi = technical_indicators.get("RSI")
        if rsi:
            if 50 <= rsi <= 70:
                score += 0.5
            elif rsi > 80 or rsi < 20:
                score -= 0.5

        # MACD 评分
        macd_status = technical_indicators.get("MACD")
        if macd_status == "bullish":
            score += 0.5
        elif macd_status == "bearish":
            score -= 0.5

        # 限制在 0-10 范围内
        return max(0.0, min(10.0, score))


# 全局实例
financial_agent = FinancialAgent()
