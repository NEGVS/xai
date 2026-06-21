#!/usr/bin/env python3
"""
环境配置验证脚本
用于验证项目的环境变量配置是否正确
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_env_file():
    """检查 .env 文件是否存在"""
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"

    print("📄 环境文件检查")
    print("-" * 50)

    if env_example.exists():
        print("✅ .env.example 存在")
    else:
        print("❌ .env.example 不存在")
        return False

    if env_file.exists():
        print("✅ .env 文件存在")
    else:
        print("⚠️  .env 文件不存在，请从 .env.example 复制并配置")
        print("   运行: cp .env.example .env")
        return False

    return True

def check_gitignore():
    """检查 .gitignore 是否包含 .env"""
    gitignore_file = project_root / ".gitignore"

    print("\n🔒 Git 安全检查")
    print("-" * 50)

    if not gitignore_file.exists():
        print("❌ .gitignore 不存在")
        return False

    with open(gitignore_file, 'r') as f:
        content = f.read()

    if '.env' in content and not '!.env.example' in content:
        print("✅ .env 已在 .gitignore 中")
        return True
    elif '.env' in content and '!.env.example' in content:
        print("✅ .env 已在 .gitignore 中，且允许 .env.example")
        return True
    else:
        print("❌ .env 不在 .gitignore 中！")
        return False

def check_config_module():
    """检查配置模块是否可以正常导入"""
    print("\n⚙️  配置模块检查")
    print("-" * 50)

    try:
        from app.core.config import settings
        print("✅ app.core.config 模块导入成功")

        # 检查新增的配置项
        config_items = [
            "DASHSCOPE_API_KEY",
            "DASHSCOPE_BASE_URL",
            "DASHSCOPE_MODEL",
            "GOOGLE_API_KEY",
            "GEMINI_API_KEY",
            "DEEPSEEK_API_KEY",
        ]

        print("\n配置项检查:")
        for item in config_items:
            if hasattr(settings, item):
                value = getattr(settings, item)
                status = "✅ 已配置" if value else "⚠️  未配置"
                print(f"  {item}: {status}")
            else:
                print(f"  {item}: ❌ 配置项不存在")

        return True
    except Exception as e:
        print(f"❌ 配置模块导入失败: {e}")
        return False

def check_api_client_manager():
    """检查 API 客户端管理器"""
    print("\n🔌 API 客户端管理器检查")
    print("-" * 50)

    try:
        from app.core.api_client import api_client_manager
        print("✅ api_client_manager 导入成功")

        # 检查可用的服务
        services = api_client_manager.get_available_llm_services()
        print("\nLLM 服务可用性:")
        for service, available in services.items():
            status = "✅ 可用" if available else "❌ 不可用"
            print(f"  {service}: {status}")

        # 检查是否至少有一个服务可用
        if any(services.values()):
            print("\n✅ 至少有一个 LLM 服务可用")
            return True
        else:
            print("\n⚠️  没有可用的 LLM 服务，请配置至少一个 API Key")
            return False

    except Exception as e:
        print(f"❌ API 客户端管理器检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_llm_service():
    """检查 LLM 服务"""
    print("\n🤖 LLM 服务检查")
    print("-" * 50)

    try:
        from app.core.llm import llm_service
        print("✅ llm_service 导入成功")

        # 检查可用的客户端
        clients = {
            "OpenAI": llm_service.openai_client,
            "Anthropic": llm_service.anthropic_client,
            "DashScope": llm_service.dashscope_client,
        }

        print("\n客户端状态:")
        for name, client in clients.items():
            status = "✅ 已初始化" if client else "❌ 未初始化"
            print(f"  {name}: {status}")

        if llm_service.default_client:
            print(f"\n✅ 默认客户端已设置")
            return True
        else:
            print(f"\n❌ 默认客户端未设置")
            return False

    except Exception as e:
        print(f"❌ LLM 服务检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_security_script():
    """检查安全扫描脚本是否存在"""
    print("\n🔍 安全工具检查")
    print("-" * 50)

    security_script = project_root / "scripts" / "security_check.py"

    if security_script.exists():
        print("✅ security_check.py 存在")

        # 检查是否可执行
        if os.access(security_script, os.X_OK):
            print("✅ security_check.py 可执行")
        else:
            print("⚠️  security_check.py 不可执行")
            print("   运行: chmod +x scripts/security_check.py")

        return True
    else:
        print("❌ security_check.py 不存在")
        return False

def check_documentation():
    """检查文档是否存在"""
    print("\n📚 文档检查")
    print("-" * 50)

    docs = {
        "API_KEY_MANAGEMENT.md": project_root / "docs" / "API_KEY_MANAGEMENT.md",
        "SECURITY_IMPROVEMENTS.md": project_root / "docs" / "SECURITY_IMPROVEMENTS.md",
    }

    all_exist = True
    for name, path in docs.items():
        if path.exists():
            print(f"✅ {name} 存在")
        else:
            print(f"❌ {name} 不存在")
            all_exist = False

    return all_exist

def main():
    """主函数"""
    print("=" * 50)
    print("🔍 项目环境配置验证")
    print("=" * 50)
    print()

    checks = [
        ("环境文件", check_env_file),
        ("Git 安全", check_gitignore),
        ("配置模块", check_config_module),
        ("API 客户端管理器", check_api_client_manager),
        ("LLM 服务", check_llm_service),
        ("安全工具", check_security_script),
        ("文档", check_documentation),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} 检查时发生错误: {e}")
            results.append((name, False))

    # 输出总结
    print("\n" + "=" * 50)
    print("📊 检查结果汇总")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")

    print()
    print(f"总计: {passed}/{total} 项检查通过")

    if passed == total:
        print("\n🎉 所有检查通过！项目配置正确。")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 项检查未通过，请查看上面的详细信息。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
