"""
AI聊天接口
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import logging
from app.ai.chat_service import ChatService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])

# ============ 初始化聊天服务 ============
chat_service = ChatService()


class ChatHistoryItem(BaseModel):
    """聊天历史项"""
    role: str = Field(..., description="角色: user或assistant")
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseModel):
    """聊天请求"""
    message: str = Field(..., description="用户消息")
    history: Optional[List[ChatHistoryItem]] = Field(default=None, description="聊天历史")
    model: str = Field(default="qwen", description="模型名称")
    stream: bool = Field(default=False, description="是否流式返回")


class ChatResponse(BaseModel):
    """聊天响应"""
    response: str = Field(..., description="AI回复")
    model: str = Field(..., description="使用的模型")
    tokens_used: Optional[int] = Field(default=None, description="使用的token数")


@router.post("", response_model=ChatResponse, summary="AI聊天")
async def chat(request: ChatRequest):
    """
    AI聊天接口

    参数:
    - message: 用户消息
    - history: 聊天历史（可选）
    - model: 模型名称（默认qwen）
    - stream: 是否流式返回（默认false）

    返回:
    - response: AI回复
    - model: 使用的模型
    - tokens_used: 使用的token数
    """
    try:
        logger.info(f"收到聊天请求: message={request.message[:50]}..., model={request.model}")

        # ============ 转换历史格式 ============
        history = []
        if request.history:
            history = [{"role": item.role, "content": item.content} for item in request.history]

        # ============ 调用聊天服务 ============
        response_text = await chat_service.chat(
            message=request.message,
            history=history,
            model=request.model
        )

        return ChatResponse(
            response=response_text,
            model=request.model,
            tokens_used=None
        )

    except Exception as e:
        logger.error(f"聊天失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"聊天失败: {str(e)}")


@router.get("/health", summary="健康检查")
async def health():
    """聊天服务健康检查"""
    return {"status": "ok", "service": "chat"}
