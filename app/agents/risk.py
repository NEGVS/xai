"""
Risk Agent - 风险评估
"""
from typing import Dict, Any, List
from app.agents.base import BaseAgent
from app.tools.stock_api import stock_data_tool
import logging
import math

logger = logging.getLogger(__name__)


class RiskAgent(BaseAgent):
    """风险Agent - 评估投资风险"""

    def __init__(self):
        super().__init__(
            name="RiskAgent",
            description="分析历史波动率、计算VaR、评估综合风险"
        )

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行风险评估

        Args:
            state: 包含stock_symbol, news_data, financial_data的状态

        Returns:
            更新了risk_data字段的状态
        """
        stock_symbol = state.get("stock_symbol")
        news_data = state.get("news_data", {})
        financial_data = state.get("financial_data", {})

        logger.info(f"[RiskAgent] 为 {stock_symbol} 评估风险")

        # 1. 获取历史数据计算波动率
        historical_data = stock_data_tool.get_historical_data(stock_symbol, period="3mo")

        if "error" in historical_data:
            logger.error(f"[RiskAgent] 获取历史数据失败: {historical_data['error']}")
            state["risk_data"] = {"error": historical_data["error"]}
            return state

        # 2. 计算波动率
        volatility = self._calculate_volatility(historical_data.get("close", []))

        # 3. 计算VaR (Value at Risk)
        var_95 = self._calculate_var(historical_data.get("close", []), confidence=0.95)

        # 4. 识别风险因素
        risk_factors = self._identify_risk_factors(news_data, financial_data, volatility)

        # 5. 计算风险评分
        risk_score = self._calculate_risk_score(
            volatility,
            news_data.get("sentiment_score", 0),
            financial_data.get("financial_health", {}).get("score", 5.0)
        )

        # 6. 确定风险级别
        risk_level = self._determine_risk_level(risk_score)

        # 7. 构建结果
        risk_data = {
            "risk_level": risk_level,
            "volatility": round(volatility, 4),
            "var_95": round(var_95, 2),
            "risk_factors": risk_factors,
            "risk_score": round(risk_score, 2)
        }

        state["risk_data"] = risk_data

        logger.info(
            f"[RiskAgent] 评估完成: 风险级别={risk_level}, "
            f"波动率={volatility:.4f}, "
            f"风险评分={risk_score:.2f}"
        )

        return state

    def _calculate_volatility(self, prices: List[float]) -> float:
        """
        计算历史波动率（年化标准差）

        Args:
            prices: 价格列表

        Returns:
            波动率
        """
        if len(prices) < 2:
            return 0.0

        # 计算日收益率
        returns = []
        for i in range(1, len(prices)):
            if prices[i-1] > 0:
                daily_return = (prices[i] - prices[i-1]) / prices[i-1]
                returns.append(daily_return)

        if not returns:
            return 0.0

        # 计算标准差
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        std_dev = math.sqrt(variance)

        # 年化波动率 (假设252个交易日)
        annualized_volatility = std_dev * math.sqrt(252)

        return annualized_volatility

    def _calculate_var(self, prices: List[float], confidence: float = 0.95) -> float:
        """
        计算VaR (Value at Risk)

        Args:
            prices: 价格列表
            confidence: 置信水平

        Returns:
            VaR值 (百分比)
        """
        if len(prices) < 2:
            return 0.0

        # 计算日收益率
        returns = []
        for i in range(1, len(prices)):
            if prices[i-1] > 0:
                daily_return = (prices[i] - prices[i-1]) / prices[i-1]
                returns.append(daily_return)

        if not returns:
            return 0.0

        # 排序收益率
        sorted_returns = sorted(returns)

        # 找到对应置信水平的分位数
        index = int((1 - confidence) * len(sorted_returns))
        var = sorted_returns[index] * 100  # 转换为百分比

        return var

    def _identify_risk_factors(
        self,
        news_data: Dict[str, Any],
        financial_data: Dict[str, Any],
        volatility: float
    ) -> List[str]:
        """
        识别风险因素

        Args:
            news_data: 新闻数据
            financial_data: 财务数据
            volatility: 波动率

        Returns:
            风险因素列表
        """
        risk_factors = []

        # 高波动率风险
        if volatility > 0.4:
            risk_factors.append("历史波动率较高")

        # 负面新闻风险
        sentiment_score = news_data.get("sentiment_score", 0)
        if sentiment_score < -0.3:
            risk_factors.append("近期负面新闻较多")

        # 技术指标风险
        tech_indicators = financial_data.get("technical_indicators", {})
        rsi = tech_indicators.get("RSI")
        if rsi and rsi > 70:
            risk_factors.append("RSI超买信号（>70）")
        elif rsi and rsi < 30:
            risk_factors.append("RSI超卖信号（<30）")

        # 财务健康风险
        health_score = financial_data.get("financial_health", {}).get("score", 5.0)
        if health_score < 4.0:
            risk_factors.append("财务健康度较低")

        # 高负债风险
        debt_to_equity = financial_data.get("financial_health", {}).get("debt_to_equity")
        if debt_to_equity and debt_to_equity > 2.0:
            risk_factors.append("负债权益比过高")

        # 估值风险
        pe_ratio = financial_data.get("financial_health", {}).get("pe_ratio")
        if pe_ratio and pe_ratio > 40:
            risk_factors.append("市盈率较高，估值偏贵")

        # 如果没有发现明显风险
        if not risk_factors:
            risk_factors.append("未发现重大风险因素")

        return risk_factors

    def _calculate_risk_score(
        self,
        volatility: float,
        sentiment_score: float,
        health_score: float
    ) -> float:
        """
        计算综合风险评分 (0-10, 越高风险越大)

        Args:
            volatility: 波动率
            sentiment_score: 情感分数
            health_score: 财务健康度评分

        Returns:
            风险评分
        """
        risk_score = 5.0  # 基础分

        # 波动率贡献 (0-3分)
        if volatility > 0.5:
            risk_score += 3.0
        elif volatility > 0.3:
            risk_score += 2.0
        elif volatility > 0.15:
            risk_score += 1.0

        # 情感分数贡献 (-2 to +2分)
        # 负面情感增加风险，正面情感降低风险
        risk_score += (-sentiment_score * 2)

        # 财务健康度贡献 (-2 to +2分)
        # 健康度低增加风险
        if health_score < 4.0:
            risk_score += 2.0
        elif health_score < 6.0:
            risk_score += 1.0
        elif health_score > 8.0:
            risk_score -= 2.0
        elif health_score > 7.0:
            risk_score -= 1.0

        # 限制在 0-10 范围内
        return max(0.0, min(10.0, risk_score))

    def _determine_risk_level(self, risk_score: float) -> str:
        """
        确定风险级别

        Args:
            risk_score: 风险评分

        Returns:
            风险级别: low, medium, high
        """
        if risk_score >= 7.0:
            return "high"
        elif risk_score >= 4.0:
            return "medium"
        else:
            return "low"


# 全局实例
risk_agent = RiskAgent()
