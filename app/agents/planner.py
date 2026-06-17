"""
Planner Agent - 任务规划
"""
from typing import Dict, Any
from app.agents.base import BaseAgent
import logging

logger = logging.getLogger(__name__)


class PlannerAgent(BaseAgent):
    """规划Agent - 分析任务并生成执行计划"""

    def __init__(self):
        super().__init__(
            name="PlannerAgent",
            description="分析用户请求，生成执行计划，决定Agent执行策略"
        )

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成执行计划

        Args:
            state: 包含stock_symbol等信息的状态

        Returns:
            更新了plan字段的状态
        """
        stock_symbol = state.get("stock_symbol")
        logger.info(f"[PlannerAgent] 为 {stock_symbol} 生成执行计划")

        # 生成执行计划
        plan = {
            "strategy": "full_analysis",
            "parallel_phase_1": ["news", "financial"],  # 并行执行
            "sequential_phase_2": ["risk", "investment"],  # 串行执行
            "final_phase": ["report"],
            "estimated_time": "45s",
            "priority": "normal"
        }

        # 更新状态
        state["plan"] = plan

        logger.info(f"[PlannerAgent] 执行计划已生成: {plan['strategy']}")

        return state


# 全局实例
planner_agent = PlannerAgent()
