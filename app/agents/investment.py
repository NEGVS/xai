"""
Investment Agent - 投资建议生成
"""
from typing import Dict, Any
from app.agents.base import BaseAgent
from app.core.llm import llm_service
import logging

logger = logging.getLogger(__name__)


class InvestmentAgent(BaseAgent):
    """投资Agent - 生成投资建议"""

    def __init__(self):
        super().__init__(
            name="InvestmentAgent",
            description="基于新闻、财务和风险数据生成投资建议"
        )

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成投资建议

        Args:
            state: 包含news_data, financial_data, risk_data的状态

        Returns:
            更新了investment_advice字段的状态
        """
        stock_symbol = state.get("stock_symbol")
        news_data = state.get("news_data", {})
        financial_data = state.get("financial_data", {})
        risk_data = state.get("risk_data", {})

        logger.info(f"[InvestmentAgent] 为 {stock_symbol} 生成投资建议")

        # 使用LLM生成投资建议
        try:
            advice = await llm_service.generate_investment_advice(
                news_data=news_data,
                financial_data=financial_data,
                risk_data=risk_data
            )

            # 如果LLM返回的建议缺少必要字段，使用规则生成
            if not advice.get("recommendation"):
                advice = self._generate_rule_based_advice(news_data, financial_data, risk_data)

            # 确保有当前价格信息
            current_price = financial_data.get("current_price", 0)

            # 如果LLM没有提供目标价和止损价，基于规则计算
            if not advice.get("target_price") and current_price:
                advice["target_price"] = self._calculate_target_price(
                    current_price,
                    advice.get("recommendation", "HOLD")
                )

            if not advice.get("stop_loss") and current_price:
                advice["stop_loss"] = self._calculate_stop_loss(
                    current_price,
                    risk_data.get("risk_level", "medium")
                )

            state["investment_advice"] = advice

            logger.info(
                f"[InvestmentAgent] 建议生成: {advice.get('recommendation', 'HOLD')}, "
                f"置信度: {advice.get('confidence', 0.5):.2f}"
            )

        except Exception as e:
            logger.error(f"[InvestmentAgent] 生成建议失败: {str(e)}")
            # 使用规则生成备用建议
            state["investment_advice"] = self._generate_rule_based_advice(
                news_data, financial_data, risk_data
            )

        return state

    def _generate_rule_based_advice(
        self,
        news_data: Dict[str, Any],
        financial_data: Dict[str, Any],
        risk_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        基于规则生成投资建议（备用方案）

        Args:
            news_data: 新闻数据
            financial_data: 财务数据
            risk_data: 风险数据

        Returns:
            投资建议字典
        """
        # 提取关键指标
        sentiment_score = news_data.get("sentiment_score", 0)
        health_score = financial_data.get("financial_health", {}).get("score", 5.0)
        risk_score = risk_data.get("risk_score", 5.0)
        risk_level = risk_data.get("risk_level", "medium")
        current_price = financial_data.get("current_price", 0)

        # 综合评分
        composite_score = (
            sentiment_score * 2 +  # 情感权重
            (health_score - 5) / 5 +  # 财务健康归一化
            (5 - risk_score) / 5  # 风险归一化（风险越低越好）
        )

        # 决策逻辑
        if composite_score > 1.5 and risk_level != "high":
            recommendation = "BUY"
            confidence = min(0.85, 0.6 + composite_score * 0.1)
            reasoning = "技术面和基本面均显示积极信号，情感分析偏正面，风险可控"
            time_horizon = "3M"
        elif composite_score < -1.5 or risk_level == "high":
            recommendation = "SELL"
            confidence = min(0.85, 0.6 + abs(composite_score) * 0.1)
            reasoning = "多项指标显示负面信号，建议规避风险"
            time_horizon = "1M"
        else:
            recommendation = "HOLD"
            confidence = 0.6
            reasoning = "市场信号混合，建议持有观望，等待更明确的趋势"
            time_horizon = "3M"

        return {
            "recommendation": recommendation,
            "confidence": round(confidence, 2),
            "target_price": self._calculate_target_price(current_price, recommendation),
            "stop_loss": self._calculate_stop_loss(current_price, risk_level),
            "time_horizon": time_horizon,
            "reasoning": reasoning
        }

    def _calculate_target_price(self, current_price: float, recommendation: str) -> float:
        """计算目标价"""
        if not current_price:
            return None

        if recommendation == "BUY":
            return round(current_price * 1.15, 2)  # 15% 上涨目标
        elif recommendation == "SELL":
            return round(current_price * 0.90, 2)  # 10% 下跌预期
        else:
            return round(current_price * 1.05, 2)  # 5% 保守目标

    def _calculate_stop_loss(self, current_price: float, risk_level: str) -> float:
        """计算止损价"""
        if not current_price:
            return None

        if risk_level == "high":
            return round(current_price * 0.92, 2)  # 8% 止损
        elif risk_level == "medium":
            return round(current_price * 0.90, 2)  # 10% 止损
        else:
            return round(current_price * 0.85, 2)  # 15% 止损


# 全局实例
investment_agent = InvestmentAgent()
