"""
新闻获取工具
"""
from typing import List, Dict, Any, Optional
import os
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class NewsFetcher:
    """新闻获取工具"""

    def __init__(self):
        self.news_api_key = os.getenv("NEWS_API_KEY")

    async def fetch_stock_news(
        self,
        symbol: str,
        limit: int = 10,
        days: int = 7
    ) -> List[Dict[str, Any]]:
        """
        获取股票相关新闻

        Args:
            symbol: 股票代码
            limit: 新闻数量限制
            days: 获取最近几天的新闻

        Returns:
            新闻列表
        """
        # 如果有NewsAPI key，使用NewsAPI
        if self.news_api_key:
            return await self._fetch_from_newsapi(symbol, limit, days)
        else:
            # 否则使用模拟数据（用于测试）
            logger.warning("[NewsFetcher] 未配置NEWS_API_KEY，使用模拟数据")
            return self._get_mock_news(symbol, limit)

    async def _fetch_from_newsapi(
        self,
        symbol: str,
        limit: int,
        days: int
    ) -> List[Dict[str, Any]]:
        """从NewsAPI获取新闻"""
        try:
            import httpx

            from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

            url = "https://newsapi.org/v2/everything"
            params = {
                "q": symbol,
                "from": from_date,
                "sortBy": "relevancy",
                "pageSize": limit,
                "language": "en",
                "apiKey": self.news_api_key
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == "ok":
                    articles = data.get("articles", [])
                    return [
                        {
                            "title": article.get("title", ""),
                            "description": article.get("description", ""),
                            "url": article.get("url", ""),
                            "source": article.get("source", {}).get("name", "Unknown"),
                            "published_at": article.get("publishedAt", ""),
                            "content": article.get("content", "")[:500]  # 限制长度
                        }
                        for article in articles
                    ]
                else:
                    logger.error(f"[NewsFetcher] NewsAPI错误: {data}")
                    return {"error": "NewsAPI返回错误"}

        except Exception as e:
            logger.error(f"[NewsFetcher] 获取新闻失败: {str(e)}")
            return {"error": str(e)}

    def _get_mock_news(self, symbol: str, limit: int) -> List[Dict[str, Any]]:
        """获取模拟新闻数据（用于测试）"""
        mock_articles = [
            {
                "title": f"{symbol} Reports Strong Q4 Earnings, Beats Expectations",
                "description": f"{symbol} announced quarterly earnings that exceeded analyst expectations, driven by strong sales growth.",
                "url": "https://example.com/article1",
                "source": "Financial Times",
                "published_at": datetime.now().isoformat(),
                "content": f"{symbol} has reported impressive Q4 results with revenue growth of 15%..."
            },
            {
                "title": f"Analysts Upgrade {symbol} Stock Rating",
                "description": f"Major investment firms have upgraded their rating on {symbol} following positive market trends.",
                "url": "https://example.com/article2",
                "source": "Bloomberg",
                "published_at": (datetime.now() - timedelta(days=1)).isoformat(),
                "content": f"Several analysts have raised their price targets for {symbol}..."
            },
            {
                "title": f"{symbol} Announces New Product Launch",
                "description": f"{symbol} unveiled its latest product innovation at a major tech conference.",
                "url": "https://example.com/article3",
                "source": "TechCrunch",
                "published_at": (datetime.now() - timedelta(days=2)).isoformat(),
                "content": f"The new product from {symbol} features cutting-edge technology..."
            },
            {
                "title": f"Market Volatility Affects {symbol} Stock Price",
                "description": f"{symbol} shares experienced fluctuations amid broader market uncertainty.",
                "url": "https://example.com/article4",
                "source": "Reuters",
                "published_at": (datetime.now() - timedelta(days=3)).isoformat(),
                "content": f"Investors remain cautious as {symbol} navigates market headwinds..."
            },
            {
                "title": f"{symbol} CEO Discusses Future Growth Strategy",
                "description": f"In a recent interview, {symbol}'s CEO outlined ambitious plans for expansion.",
                "url": "https://example.com/article5",
                "source": "CNBC",
                "published_at": (datetime.now() - timedelta(days=4)).isoformat(),
                "content": f"The leadership team at {symbol} is focused on innovation and market share..."
            }
        ]

        return mock_articles[:limit]


# 全局实例
news_fetcher = NewsFetcher()
