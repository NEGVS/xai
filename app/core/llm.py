"""
LLM服务封装
"""
from typing import Optional, Dict, Any, List
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import settings


class LLMService:
    """LLM服务管理器"""

    def __init__(self):
        """初始化LLM服务"""
        self.dashscope_client: Optional[ChatOpenAI] = None

        # 初始化阿里云DashScope客户端（使用OpenAI兼容模式）
        if settings.DASHSCOPE_API_KEY:
            self.dashscope_client = ChatOpenAI(
                model=settings.DASHSCOPE_MODEL,
                api_key=settings.DASHSCOPE_API_KEY,
                base_url=settings.DASHSCOPE_BASE_URL,
                temperature=0.7
            )

        # 默认使用DashScope客户端
        self.default_client = self.dashscope_client

        if not self.default_client:
            raise ValueError("需要配置 DASHSCOPE_API_KEY 环境变量")

    def get_client(self, provider: str = "default"):
        """获取指定的LLM客户端"""
        if provider == "dashscope" and self.dashscope_client:
            return self.dashscope_client
        elif provider == "default":
            return self.default_client
        else:
            raise ValueError(f"LLM provider '{provider}' 不可用，当前仅支持 dashscope")

    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        情感分析

        Args:
            text: 要分析的文本

        Returns:
            包含sentiment_score和reasoning的字典
        """
        system_prompt = """你是一个专业的金融情感分析专家。
分析给定文本的情感倾向，返回-1到1之间的分数：
- 负面情感: -1.0 到 -0.3
- 中性情感: -0.3 到 0.3
- 正面情感: 0.3 到 1.0

请以JSON格式返回: {"score": <float>, "reasoning": "<string>"}"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"分析以下文本的情感:\n\n{text}")
        ]

        response = await self.default_client.ainvoke(messages)

        # 解析响应
        import json
        try:
            result = json.loads(response.content)
            return {
                "sentiment_score": result.get("score", 0.0),
                "reasoning": result.get("reasoning", "")
            }
        except json.JSONDecodeError:
            # 如果解析失败，返回中性
            return {"sentiment_score": 0.0, "reasoning": "无法解析LLM响应"}

    async def generate_investment_advice(
        self,
        news_data: Dict[str, Any],
        financial_data: Dict[str, Any],
        risk_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        生成投资建议

        Args:
            news_data: 新闻分析数据
            financial_data: 财务分析数据
            risk_data: 风险分析数据

        Returns:
            投资建议字典
        """
        system_prompt = """你是一位经验丰富的投资顾问。
基于提供的新闻、财务和风险数据，给出专业的投资建议。

返回JSON格式:
{
  "recommendation": "BUY" | "HOLD" | "SELL",
  "confidence": <0.0-1.0>,
  "target_price": <float | null>,
  "stop_loss": <float | null>,
  "time_horizon": "<3M|6M|1Y>",
  "reasoning": "<详细理由>"
}"""

        content = f"""
新闻分析:
{news_data}

财务数据:
{financial_data}

风险评估:
{risk_data}

请提供投资建议。
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=content)
        ]

        response = await self.default_client.ainvoke(messages)

        # 解析响应
        import json
        try:
            result = json.loads(response.content)
            return result
        except json.JSONDecodeError:
            return {
                "recommendation": "HOLD",
                "confidence": 0.5,
                "target_price": None,
                "stop_loss": None,
                "time_horizon": "3M",
                "reasoning": "数据不足，建议观望"
            }

    async def summarize_text(self, text: str, max_length: int = 200) -> str:
        """
        文本摘要

        Args:
            text: 要摘要的文本
            max_length: 最大长度

        Returns:
            摘要文本
        """
        system_prompt = f"你是一个专业的文本摘要助手。请将给定文本总结为不超过{max_length}字的简洁摘要。"

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=text)
        ]

        response = await self.default_client.ainvoke(messages)
        return response.content

    async def extract_key_events(self, news_articles: List[str]) -> List[str]:
        """
        从新闻中提取关键事件

        Args:
            news_articles: 新闻文章列表

        Returns:
            关键事件列表
        """
        system_prompt = """你是一个金融新闻分析专家。
从给定的新闻文章中提取3-5个最重要的事件。
每个事件用一句话概括，以列表形式返回。

返回JSON格式: {"events": ["事件1", "事件2", ...]}"""

        content = "\n\n".join([f"文章{i+1}:\n{article}" for i, article in enumerate(news_articles)])

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=content)
        ]

        response = await self.default_client.ainvoke(messages)

        # 解析响应
        import json
        try:
            result = json.loads(response.content)
            return result.get("events", [])
        except json.JSONDecodeError:
            return ["无法提取关键事件"]

    async def generate_report_summary(self, full_data: Dict[str, Any]) -> str:
        """
        生成执行摘要

        Args:
            full_data: 包含所有分析结果的完整数据

        Returns:
            执行摘要文本
        """
        system_prompt = """你是一个专业的金融分析报告撰写专家。
基于提供的完整分析数据，撰写一份简明扼要的执行摘要（200-300字）。
摘要应包含：当前市场表现、主要发现、风险提示和投资建议。"""

        import json
        content = f"完整分析数据:\n{json.dumps(full_data, ensure_ascii=False, indent=2)}"

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=content)
        ]

        response = await self.default_client.ainvoke(messages)
        return response.content


# 全局LLM服务实例
llm_service = LLMService()
