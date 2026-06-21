"""
统一的API客户端管理服务
用于集中管理所有LLM和外部服务的API配置
"""
import os
from typing import Optional, Dict, Any
from openai import AsyncOpenAI, OpenAI
from app.core.config import settings


class APIClientManager:
    """
    统一的API客户端管理器
    实现单例模式，确保配置只加载一次
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APIClientManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化所有API客户端"""
        if self._initialized:
            return

        # OpenAI客户端
        self.openai_client: Optional[OpenAI] = None
        self.openai_async_client: Optional[AsyncOpenAI] = None

        # DashScope客户端（阿里云千问）
        self.dashscope_client: Optional[OpenAI] = None
        self.dashscope_async_client: Optional[AsyncOpenAI] = None

        # DeepSeek客户端
        self.deepseek_client: Optional[OpenAI] = None
        self.deepseek_async_client: Optional[AsyncOpenAI] = None

        # API Keys（从配置中获取）
        self.openai_api_key = settings.OPENAI_API_KEY
        self.anthropic_api_key = settings.ANTHROPIC_API_KEY
        self.dashscope_api_key = settings.DASHSCOPE_API_KEY
        self.google_api_key = settings.GOOGLE_API_KEY or settings.GEMINI_API_KEY
        self.deepseek_api_key = settings.DEEPSEEK_API_KEY
        self.news_api_key = settings.NEWS_API_KEY
        self.alpha_vantage_api_key = settings.ALPHA_VANTAGE_API_KEY

        # 初始化客户端
        self._init_clients()

        self._initialized = True

    def _init_clients(self):
        """初始化各个API客户端"""
        # 初始化OpenAI客户端
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
            self.openai_async_client = AsyncOpenAI(api_key=self.openai_api_key)

        # 初始化DashScope客户端（使用OpenAI兼容模式）
        if self.dashscope_api_key:
            self.dashscope_client = OpenAI(
                api_key=self.dashscope_api_key,
                base_url=settings.DASHSCOPE_BASE_URL
            )
            self.dashscope_async_client = AsyncOpenAI(
                api_key=self.dashscope_api_key,
                base_url=settings.DASHSCOPE_BASE_URL
            )

        # 初始化DeepSeek客户端
        if self.deepseek_api_key:
            self.deepseek_client = OpenAI(
                api_key=self.deepseek_api_key,
                base_url="https://api.deepseek.com"
            )
            self.deepseek_async_client = AsyncOpenAI(
                api_key=self.deepseek_api_key,
                base_url="https://api.deepseek.com"
            )

    def get_openai_client(self, async_mode: bool = False) -> Optional[OpenAI]:
        """获取OpenAI客户端"""
        if async_mode:
            return self.openai_async_client
        return self.openai_client

    def get_dashscope_client(self, async_mode: bool = False) -> Optional[OpenAI]:
        """获取DashScope客户端"""
        if async_mode:
            return self.dashscope_async_client
        return self.dashscope_client

    def get_deepseek_client(self, async_mode: bool = False) -> Optional[OpenAI]:
        """获取DeepSeek客户端"""
        if async_mode:
            return self.deepseek_async_client
        return self.deepseek_client

    def get_api_key(self, service: str) -> Optional[str]:
        """
        获取指定服务的API Key

        Args:
            service: 服务名称 (openai, anthropic, dashscope, google, gemini, deepseek, news, alpha_vantage)

        Returns:
            API Key或None
        """
        key_map = {
            "openai": self.openai_api_key,
            "anthropic": self.anthropic_api_key,
            "dashscope": self.dashscope_api_key,
            "google": self.google_api_key,
            "gemini": self.google_api_key,
            "deepseek": self.deepseek_api_key,
            "news": self.news_api_key,
            "alpha_vantage": self.alpha_vantage_api_key,
        }
        return key_map.get(service.lower())

    def has_service(self, service: str) -> bool:
        """
        检查服务是否可用

        Args:
            service: 服务名称

        Returns:
            是否可用
        """
        return self.get_api_key(service) is not None

    def get_available_llm_services(self) -> Dict[str, bool]:
        """
        获取所有可用的LLM服务

        Returns:
            服务名称到可用状态的映射
        """
        return {
            "openai": self.has_service("openai"),
            "anthropic": self.has_service("anthropic"),
            "dashscope": self.has_service("dashscope"),
            "google": self.has_service("google"),
            "deepseek": self.has_service("deepseek"),
        }

    def get_default_llm_client(self, async_mode: bool = False):
        """
        获取默认的LLM客户端（优先级：DashScope > OpenAI > DeepSeek）

        Args:
            async_mode: 是否返回异步客户端

        Returns:
            默认的LLM客户端
        """
        if self.dashscope_client:
            return self.get_dashscope_client(async_mode)
        elif self.openai_client:
            return self.get_openai_client(async_mode)
        elif self.deepseek_client:
            return self.get_deepseek_client(async_mode)
        else:
            raise ValueError("没有可用的LLM服务，请配置至少一个LLM API Key")


# 全局单例实例
api_client_manager = APIClientManager()
