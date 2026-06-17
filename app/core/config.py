"""
核心配置文件
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """应用配置"""

    # 应用配置
    APP_NAME: str = "Stock Analysis Multi-Agent System"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = Field(default=False, validation_alias="DEBUG")
    ENVIRONMENT: str = Field(default="development", validation_alias="ENVIRONMENT")

    # API配置
    API_HOST: str = Field(default="0.0.0.0", validation_alias="API_HOST")
    API_PORT: int = Field(default=8000, validation_alias="API_PORT")
    API_PREFIX: str = "/api/v1"

    # LLM配置
    OPENAI_API_KEY: Optional[str] = Field(default=None, validation_alias="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4", validation_alias="OPENAI_MODEL")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, validation_alias="ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = Field(default="claude-3-sonnet-20240229", validation_alias="ANTHROPIC_MODEL")

    # 数据库配置
    DATABASE_URL: str = Field(
        default="postgresql://admin:password@localhost:5432/stock_analysis",
        validation_alias="DATABASE_URL"
    )

    # Redis配置
    REDIS_URL: str = Field(default="redis://localhost:6379", validation_alias="REDIS_URL")

    # 数据源API配置
    NEWS_API_KEY: Optional[str] = Field(default=None, validation_alias="NEWS_API_KEY")
    ALPHA_VANTAGE_API_KEY: Optional[str] = Field(default=None, validation_alias="ALPHA_VANTAGE_API_KEY")

    # Agent配置
    MAX_RETRY_COUNT: int = 3
    AGENT_TIMEOUT: int = 120  # 秒
    ENABLE_PARALLEL_EXECUTION: bool = True

    # 缓存配置
    CACHE_TTL: int = 3600  # 秒
    ENABLE_CACHE: bool = True

    # 日志配置
    LOG_LEVEL: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    class Config:
        env_file = ".env"
        case_sensitive = True


# 全局配置实例
settings = Settings()
