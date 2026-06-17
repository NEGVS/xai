"""
快速测试脚本 - 测试股票分析功能
"""
import asyncio
import sys
sys.path.insert(0, '/Users/andy_mac/PycharmProjects/xai')

from app.workflows.stock_analysis import run_stock_analysis_workflow
import uuid
import json


async def test_stock_analysis():
    """测试股票分析工作流"""

    print("=" * 60)
    print("🧪 股票分析系统测试")
    print("=" * 60)
    print()

    # 测试股票代码
    test_symbol = "AAPL"
    request_id = str(uuid.uuid4())

    print(f"📊 测试股票: {test_symbol}")
    print(f"🆔 请求ID: {request_id}")
    print()
    print("⏳ 开始分析...")
    print()

    try:
        # 运行分析
        result = await run_stock_analysis_workflow(
            stock_symbol=test_symbol,
            request_id=request_id
        )

        # 打印结果
        print("=" * 60)
        print("✅ 分析完成!")
        print("=" * 60)
        print()

        # 检查错误
        if result.get("errors"):
            print("⚠️  发现错误:")
            for error in result["errors"]:
                print(f"   - {error}")
            print()

        # 打印报告
        if result.get("report"):
            report = result["report"]

            print(f"📋 报告ID: {report['report_id']}")
            print(f"📈 股票代码: {report['stock_symbol']}")
            print()

            # 执行摘要
            print("📝 执行摘要:")
            print("-" * 60)
            print(report.get('executive_summary', '无'))
            print()

            # 新闻分析
            if report.get('news'):
                news = report['news']
                print("📰 新闻分析:")
                print(f"   情感分数: {news.get('sentiment_score', 0):.2f}")
                print(f"   影响级别: {news.get('impact_level', 'unknown')}")
                print(f"   新闻数量: {news.get('articles_count', 0)}")
                if news.get('key_events'):
                    print(f"   关键事件:")
                    for event in news['key_events'][:3]:
                        print(f"      • {event}")
                print()

            # 财务分析
            if report.get('financial'):
                financial = report['financial']
                print("💰 财务分析:")
                print(f"   当前价格: ${financial.get('current_price', 0):.2f}")
                print(f"   日内涨跌: {financial.get('price_change_1d', 'N/A')}")
                print(f"   成交量: {financial.get('volume', 0):,}")

                tech = financial.get('technical_indicators', {})
                print(f"   RSI: {tech.get('RSI', 'N/A')}")
                print(f"   MACD: {tech.get('MACD', 'N/A')}")

                health = financial.get('financial_health', {})
                print(f"   健康评分: {health.get('score', 'N/A')}/10")
                print()

            # 风险评估
            if report.get('risk'):
                risk = report['risk']
                print("⚠️  风险评估:")
                print(f"   风险级别: {risk.get('risk_level', 'unknown').upper()}")
                print(f"   风险评分: {risk.get('risk_score', 0):.2f}/10")
                print(f"   波动率: {risk.get('volatility', 0):.4f}")
                print(f"   VaR(95%): {risk.get('var_95', 0):.2f}%")
                if risk.get('risk_factors'):
                    print(f"   风险因素:")
                    for factor in risk['risk_factors'][:3]:
                        print(f"      • {factor}")
                print()

            # 投资建议
            if report.get('investment'):
                investment = report['investment']
                recommendation = investment.get('recommendation', 'HOLD')

                # 根据建议设置emoji
                emoji = {"BUY": "🟢", "HOLD": "🟡", "SELL": "🔴"}.get(recommendation, "⚪")

                print(f"{emoji} 投资建议:")
                print(f"   推荐: {recommendation}")
                print(f"   置信度: {investment.get('confidence', 0)*100:.0f}%")
                if investment.get('target_price'):
                    print(f"   目标价: ${investment['target_price']:.2f}")
                if investment.get('stop_loss'):
                    print(f"   止损价: ${investment['stop_loss']:.2f}")
                print(f"   时间范围: {investment.get('time_horizon', 'N/A')}")
                print()
                print(f"   理由: {investment.get('reasoning', '无')}")
                print()

            # 执行时间
            print(f"⏱️  执行时间: {report.get('execution_time', 0):.2f}秒")

        else:
            print("❌ 未生成报告")
            print()
            print("完整结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print()
    print("🔧 请确保已配置 .env 文件中的 LLM API 密钥")
    print("   (OPENAI_API_KEY 或 ANTHROPIC_API_KEY)")
    print()
    input("按回车开始测试...")
    print()

    asyncio.run(test_stock_analysis())
