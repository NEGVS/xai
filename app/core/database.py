"""
数据库连接和会话管理
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# 创建数据库引擎
try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        echo=settings.DEBUG
    )
    logger.info(f"数据库引擎已创建: {settings.DATABASE_URL.split('@')[0]}@...")
except Exception as e:
    logger.warning(f"数据库连接失败: {str(e)}")
    engine = None

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None

# 创建基类
Base = declarative_base()


def get_db():
    """
    获取数据库会话（依赖注入）

    Yields:
        数据库会话
    """
    if SessionLocal is None:
        raise RuntimeError("数据库未配置")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库（创建所有表）"""
    if engine is None:
        logger.warning("数据库未配置，跳过初始化")
        return

    try:
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表已创建")
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
