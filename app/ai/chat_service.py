"""
AI聊天服务
chat_service.py,
"""
import logging
from typing import List, Dict, Optional
from app.core.ai_client import ai_client_manager

logger = logging.getLogger(__name__)


class ChatService:
    """AI聊天服务"""

    def __init__(self):
        """初始化聊天服务"""
        self.client = ai_client_manager.async_client
        self.default_model = ai_client_manager.default_model
        logger.info("ChatService初始化完成")

    async def chat(
        self,
        message: str,
        history: Optional[List[Dict[str, str]]] = None,
        model: str = "qwen"
    ) -> str:
        """
        AI聊天

        参数:
        - message: 用户消息
        - history: 聊天历史 [{"role": "user", "content": "..."}, ...]
        - model: 模型名称

        返回:
        - AI回复文本
        """
        try:
            # ============ 构建消息列表 ============
            messages = []

            # 添加系统提示
            messages.append({
                "role": "system",
                "content": "你是一个友好、专业的AI助手。请用简洁、清晰的语言回答用户问题。支持Markdown格式输出。"
            })

            # 添加历史消息（最近10条）
            if history:
                messages.extend(history[-10:])

            # 添加当前用户消息
            messages.append({
                "role": "user",
                "content": message
            })

            logger.info(f"发送聊天请求: model={model}, messages_count={len(messages)}")

            # ============ 获取模型配置 ============
            model_config = ai_client_manager.get_model_config(model)

            # ============ 调用通义千问API ============
            response = await self.client.chat.completions.create(
                model=model or self.default_model,
                messages=messages,
                **model_config
            )

            reply = response.choices[0].message.content
            logger.info(f"AI回复成功: reply_length={len(reply)}")

            return reply

        except Exception as e:
            logger.error(f"AI聊天失败: {str(e)}", exc_info=True)
            raise Exception(f"AI服务调用失败: {str(e)}")

    def get_models(self) -> List[str]:
        """获取支持的模型列表"""
        return ["qwen-plus", "qwen-turbo", "qwen-max"]
