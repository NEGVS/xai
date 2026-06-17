"""
股票数据获取工具
"""
from typing import Dict, Any, Optional
import yfinance as yf
from datetime import datetime, timedelta


class StockDataTool:
    """股票数据工具"""

    def __init__(self):
        self.name = "stock_data_tool"
        self.description = "获取股票实时数据、历史价格和基本面信息"

    def get_current_price(self, symbol: str) -> Dict[str, Any]:
        """
        获取当前股价

        Args:
            symbol: 股票代码

        Returns:
            包含当前价格、涨跌幅等信息的字典
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            # 获取历史数据计算涨跌
            hist = stock.history(period="5d")

            current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
            previous_close = info.get('previousClose', current_price)

            price_change_1d = ((current_price - previous_close) / previous_close * 100) if previous_close else 0

            return {
                "current_price": current_price,
                "previous_close": previous_close,
                "price_change_1d": f"{price_change_1d:+.2f}%",
                "volume": info.get('volume', 0),
                "market_cap": info.get('marketCap'),
                "high_52w": info.get('fiftyTwoWeekHigh'),
                "low_52w": info.get('fiftyTwoWeekLow'),
            }
        except Exception as e:
            return {"error": str(e)}

    def get_historical_data(
        self,
        symbol: str,
        period: str = "1mo"
    ) -> Dict[str, Any]:
        """
        获取历史数据

        Args:
            symbol: 股票代码
            period: 时间周期 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)

        Returns:
            历史数据字典
        """
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period)

            if hist.empty:
                return {"error": "无法获取历史数据"}

            return {
                "dates": hist.index.strftime('%Y-%m-%d').tolist(),
                "open": hist['Open'].tolist(),
                "high": hist['High'].tolist(),
                "low": hist['Low'].tolist(),
                "close": hist['Close'].tolist(),
                "volume": hist['Volume'].tolist(),
            }
        except Exception as e:
            return {"error": str(e)}

    def get_financial_metrics(self, symbol: str) -> Dict[str, Any]:
        """
        获取财务指标

        Args:
            symbol: 股票代码

        Returns:
            财务指标字典
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            return {
                "pe_ratio": info.get('forwardPE') or info.get('trailingPE'),
                "pb_ratio": info.get('priceToBook'),
                "ps_ratio": info.get('priceToSalesTrailing12Months'),
                "debt_to_equity": info.get('debtToEquity'),
                "roe": info.get('returnOnEquity'),
                "profit_margin": info.get('profitMargins'),
                "operating_margin": info.get('operatingMargins'),
                "revenue_growth": info.get('revenueGrowth'),
                "earnings_growth": info.get('earningsGrowth'),
                "dividend_yield": info.get('dividendYield'),
            }
        except Exception as e:
            return {"error": str(e)}

    def calculate_technical_indicators(
        self,
        symbol: str,
        period: str = "3mo"
    ) -> Dict[str, Any]:
        """
        计算技术指标

        Args:
            symbol: 股票代码
            period: 时间周期

        Returns:
            技术指标字典
        """
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period)

            if hist.empty:
                return {"error": "无法获取数据"}

            close_prices = hist['Close']

            # 计算移动平均线
            ma_20 = close_prices.rolling(window=20).mean().iloc[-1]
            ma_50 = close_prices.rolling(window=50).mean().iloc[-1]
            ma_200 = close_prices.rolling(window=200).mean().iloc[-1] if len(close_prices) >= 200 else None

            # 计算RSI
            delta = close_prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1] if not rsi.empty else 50

            # 计算MACD
            ema_12 = close_prices.ewm(span=12, adjust=False).mean()
            ema_26 = close_prices.ewm(span=26, adjust=False).mean()
            macd_line = ema_12 - ema_26
            signal_line = macd_line.ewm(span=9, adjust=False).mean()
            macd_histogram = macd_line - signal_line

            macd_status = "bullish" if macd_histogram.iloc[-1] > 0 else "bearish"

            return {
                "MA_20": round(ma_20, 2) if ma_20 else None,
                "MA_50": round(ma_50, 2) if ma_50 else None,
                "MA_200": round(ma_200, 2) if ma_200 else None,
                "RSI": round(current_rsi, 2),
                "MACD": macd_status,
                "MACD_line": round(macd_line.iloc[-1], 2),
                "Signal_line": round(signal_line.iloc[-1], 2),
            }
        except Exception as e:
            return {"error": str(e)}

    def get_company_info(self, symbol: str) -> Dict[str, Any]:
        """
        获取公司基本信息

        Args:
            symbol: 股票代码

        Returns:
            公司信息字典
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            return {
                "name": info.get('longName') or info.get('shortName'),
                "sector": info.get('sector'),
                "industry": info.get('industry'),
                "country": info.get('country'),
                "website": info.get('website'),
                "description": info.get('longBusinessSummary', '')[:500],  # 限制长度
                "employees": info.get('fullTimeEmployees'),
            }
        except Exception as e:
            return {"error": str(e)}


# 全局实例
stock_data_tool = StockDataTool()
