"""
News Agent - 新闻收集和分析
"""
from typing import Dict, Any, List
from app.agents.base import BaseAgent
from app.core.llm import llm_service
from app.tools.news_fetcher import news_fetcher
import logging

logger = logging.getLogger(__name__)


class NewsAgent(BaseAgent):
    """新闻Agent - 收集和分析股票相关新闻"""

    def __init__(self):
        super().__init__(
            name="NewsAgent",
            description="收集股票相关新闻，进行情感分析和事件提取"
        )

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行新闻分析

        Args:
            state: 包含stock_symbol的状态

        Returns:
            更新了news_data字段的状态
        """
        stock_symbol = state.get("stock_symbol")
        logger.info(f"[NewsAgent] 为 {stock_symbol} 收集新闻")

        # 1. 获取新闻
        news_articles = await news_fetcher.fetch_stock_news(stock_symbol, limit=10)

        if not news_articles or "error" in news_articles:
            logger.warning(f"[NewsAgent] 无法获取新闻: {news_articles.get('error', '未知错误')}")
            state["news_data"] = {
                "error": "无法获取新闻数据",
                "news_summary": "暂无新闻数据",
                "sentiment_score": 0.0,
                "key_events": [],
                "impact_level": "unknown",
                "articles_count": 0,
                "sources": []
            }
            return state

        # 2. 合并所有新闻文本进行情感分析
        all_news_text = "\n\n".join([
            f"{article['title']} - {article.get('description', '')}"
            for article in news_articles
        ])

        # 3. 情感分析
        sentiment_result = await llm_service.analyze_sentiment(all_news_text[:4000])  # 限制长度
        sentiment_score = sentiment_result.get("sentiment_score", 0.0)

        # 4. 提取关键事件
        article_texts = [
            f"{article['title']}. {article.get('description', '')}"
            for article in news_articles[:5]  # 只用前5篇
        ]
        key_events = await llm_service.extract_key_events(article_texts)

        # 5. 生成新闻摘要
        news_summary = await llm_service.summarize_text(all_news_text[:3000], max_length=200)

        # 6. 确定影响级别
        impact_level = self._determine_impact_level(sentiment_score, len(key_events))

        # 7. 提取新闻源
        sources = list(set([article.get("source", "Unknown") for article in news_articles]))

        # 8. 构建结果
        news_data = {
            "news_summary": news_summary,
            "sentiment_score": sentiment_score,
            "key_events": key_events,
            "impact_level": impact_level,
            "articles_count": len(news_articles),
            "sources": sources,
            "sample_articles": news_articles[:3]  # 保存前3篇作为样本
        }

        state["news_data"] = news_data

        logger.info(
            f"[NewsAgent] 分析完成: {len(news_articles)}篇新闻, "
            f"情感分数: {sentiment_score:.2f}, "
            f"影响级别: {impact_level}"
        )

        return state

    def _determine_impact_level(self, sentiment_score: float, event_count: int) -> str:
        """
        确定影响级别

        Args:
            sentiment_score: 情感分数
            event_count: 关键事件数量

        Returns:
            影响级别: low, medium, high
        """
        abs_score = abs(sentiment_score)

        if abs_score > 0.6 or event_count >= 4:
            return "high"
        elif abs_score > 0.3 or event_count >= 2:
            return "medium"
        else:
            return "low"


# 全局实例
news_agent = NewsAgent()
