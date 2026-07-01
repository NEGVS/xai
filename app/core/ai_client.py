"""
AI客户端管理器 - 统一管理AI客户端和模型配置
"""
import os
from typing import Optional
from openai import AsyncOpenAI, OpenAI
from app.core.config import settings


class AIClientManager:
    """AI客户端管理器 - 单例模式"""

    _instance: Optional['AIClientManager'] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化AI客户端"""
        if self._initialized:
            return

        # ============ 阿里云DashScope配置 ============
        self.dashscope_api_key = settings.DASHSCOPE_API_KEY or os.getenv("DASHSCOPE_API_KEY")
        if not self.dashscope_api_key:
            raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")

        self.dashscope_base_url = settings.DASHSCOPE_BASE_URL
        self.default_model = settings.DASHSCOPE_MODEL

        # ============ 创建同步和异步客户端 ============
        self._async_client = AsyncOpenAI(
            api_key=self.dashscope_api_key,
            base_url=self.dashscope_base_url,
        )

        self._sync_client = OpenAI(
            api_key=self.dashscope_api_key,
            base_url=self.dashscope_base_url,
        )

        # ============ 模型配置 ============
        self.model_config = {
            "qwen-plus": {"temperature": 0.7, "max_tokens": 2000, "top_p": 0.8},
            "qwen-turbo": {"temperature": 0.7, "max_tokens": 1500, "top_p": 0.8},
            "qwen-max": {"temperature": 0.7, "max_tokens": 6000, "top_p": 0.8},
            "qwen3.5-plus": {"temperature": 0.7, "max_tokens": 2000, "top_p": 0.8},
        }

        self._initialized = True

    @property
    def async_client(self) -> AsyncOpenAI:
        """获取异步客户端"""
        return self._async_client

    @property
    def sync_client(self) -> OpenAI:
        """获取同步客户端"""
        return self._sync_client

    def get_model_config(self, model: str = None) -> dict:
        """
        获取模型配置

        参数:
            model: 模型名称，如果为None则使用默认模型

        返回:
            模型配置字典
        """
        model = model or self.default_model
        return self.model_config.get(model, self.model_config["qwen-plus"])

    def get_available_models(self) -> list:
        """获取可用的模型列表"""
        return list(self.model_config.keys())


# ============ 全局单例实例 ============
ai_client_manager = AIClientManager()
