"""
简单的API测试客户端
"""
import requests
import json
import time


def test_health():
    """测试健康检查"""
    print("🏥 测试健康检查...")
    try:
        response = requests.get("http://localhost:8000/api/v1/agents/health")
        result = response.json()

        print(f"   状态: {result['status']}")
        print(f"   LLM: {result['llm_status']}")
        print(f"   Agent数量: {len(result['agents'])}")

        for agent in result['agents']:
            status_emoji = "✅" if agent['status'] == 'active' else "❌"
            print(f"   {status_emoji} {agent['agent_name']}: {agent['status']}")

        print()
        return True
    except Exception as e:
        print(f"   ❌ 失败: {str(e)}")
        print()
        return False


def test_stock_analysis(symbol="AAPL"):
    """测试股票分析"""
    print(f"📊 测试股票分析: {symbol}")
    print("   请求中...")

    start_time = time.time()

    try:
        response = requests.post(
            "http://localhost:8000/api/v1/analysis/stock",
            json={
                "symbol": symbol,
                "analysis_type": "full",
                "time_range": "1M"
            },
            timeout=180  # 3分钟超时
        )

        elapsed = time.time() - start_time

        if response.status_code == 200:
            result = response.json()

            if result['success']:
                print(f"   ✅ 分析成功 (耗时: {elapsed:.1f}秒)")

                data = result.get('data', {})

                # 打印关键信息
                if data.get('investment'):
                    inv = data['investment']
                    print(f"   💡 建议: {inv.get('recommendation', 'N/A')}")
                    print(f"   📈 置信度: {inv.get('confidence', 0)*100:.0f}%")

                if data.get('financial'):
                    fin = data['financial']
                    print(f"   💰 当前价格: ${fin.get('current_price', 0):.2f}")

                if data.get('risk'):
                    risk = data['risk']
                    print(f"   ⚠️  风险级别: {risk.get('risk_level', 'N/A')}")

                print()
                return True
            else:
                print(f"   ❌ 分析失败: {result.get('message', '未知错误')}")
                print()
                return False
        else:
            print(f"   ❌ HTTP {response.status_code}: {response.text}")
            print()
            return False

    except requests.exceptions.Timeout:
        print(f"   ⏱️  超时 (已等待 {time.time() - start_time:.1f}秒)")
        print()
        return False
    except Exception as e:
        print(f"   ❌ 失败: {str(e)}")
        print()
        return False


def main():
    """主测试流程"""
    print()
    print("=" * 60)
    print("🧪 Stock Analysis API 测试")
    print("=" * 60)
    print()
    print("⚠️  请确保API服务已启动: ./start.sh")
    print()

    # 1. 测试健康检查
    if not test_health():
        print("❌ 健康检查失败，请检查服务是否运行")
        return

    # 2. 测试股票分析
    print("开始股票分析测试...")
    print()

    test_symbols = ["AAPL"]  # 可以添加更多: ["AAPL", "TSLA", "MSFT"]

    for symbol in test_symbols:
        test_stock_analysis(symbol)
        time.sleep(1)  # 避免请求过快

    print("=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
