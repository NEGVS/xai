"""
FastAPI主应用
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import stock, agents, chat
from app.core.config import settings
import logging

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动事件
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} 启动中...")
    logger.info(f"📝 环境: {settings.ENVIRONMENT}")

    # 显示可访问的URL（0.0.0.0不能直接在浏览器访问）
    host_display = "127.0.0.1" if settings.API_HOST == "0.0.0.0" else settings.API_HOST
    logger.info(f"🔗 API文档: http://{host_display}:{settings.API_PORT}/docs")
    logger.info(f"🤖 LLM: {settings.DASHSCOPE_MODEL} (DashScope)")
    logger.info(f""" ⏺ 0.0.0.0 是服务器监听地址，浏览器无法直接访问。请使用以下地址：
     
    http://127.0.0.1:8000/docs 或 http://localhost:8000/docs
  
    启动成功 """)

    yield

    # 关闭事件
    logger.info(f"👋 {settings.APP_NAME} 关闭中...")


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="基于LangGraph的Multi-Agent股票分析系统",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(stock.router, prefix=settings.API_PREFIX)
app.include_router(agents.router, prefix=settings.API_PREFIX)
app.include_router(chat.router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Stock Analysis Multi-Agent System API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": f"{settings.API_PREFIX}/agents/health"
    }


@app.get("/health")
async def health_check():
    """简单的健康检查"""
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
