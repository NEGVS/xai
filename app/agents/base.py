"""
Agent基础类
"""
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Agent基础类"""

    def __init__(self, name: str, description: str):
        """
        初始化Agent

        Args:
            name: Agent名称
            description: Agent描述
        """
        self.name = name
        self.description = description
        self.execution_count = 0
        self.last_execution_time: Optional[datetime] = None

    @abstractmethod
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行Agent逻辑

        Args:
            state: 当前状态

        Returns:
            更新后的状态
        """
        pass

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        运行Agent（包含日志和错误处理）

        Args:
            state: 当前状态

        Returns:
            更新后的状态
        """
        logger.info(f"[{self.name}] 开始执行")
        start_time = datetime.now()

        try:
            result_state = await self.execute(state)
            self.execution_count += 1
            self.last_execution_time = datetime.now()

            execution_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"[{self.name}] 执行完成，耗时: {execution_time:.2f}秒")

            return result_state

        except Exception as e:
            logger.error(f"[{self.name}] 执行失败: {str(e)}", exc_info=True)
            # 将错误添加到状态中
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(f"{self.name}: {str(e)}")
            return state

    def get_status(self) -> Dict[str, Any]:
        """获取Agent状态"""
        return {
            "name": self.name,
            "description": self.description,
            "execution_count": self.execution_count,
            "last_execution_time": self.last_execution_time.isoformat() if self.last_execution_time else None,
            "status": "active"
        }
