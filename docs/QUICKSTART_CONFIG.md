# API Key 配置快速开始

## 🚀 快速开始（5 分钟）

### 1. 设置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
vim .env
```

**至少配置一个 LLM 服务**：

```bash
# 选项 1: 阿里云千问（推荐，国内速度快）
DASHSCOPE_API_KEY=sk-your-dashscope-key
DASHSCOPE_MODEL=qwen-plus

# 选项 2: OpenAI
OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-4

# 选项 3: Google Gemini
GOOGLE_API_KEY=AIza-your-google-key

# 选项 4: DeepSeek
DEEPSEEK_API_KEY=sk-your-deepseek-key
```

### 2. 验证配置

```bash
# 运行验证脚本
python scripts/verify_setup.py
```

### 3. 使用统一的 API 客户端

```python
from app.core.api_client import api_client_manager

# 获取默认客户端（自动选择可用的服务）
client = api_client_manager.get_default_llm_client()

# 或获取特定服务的客户端
dashscope_client = api_client_manager.get_dashscope_client()
openai_client = api_client_manager.get_openai_client()

# 异步客户端
async_client = api_client_manager.get_dashscope_client(async_mode=True)
```

## 📖 详细文档

- **[API_KEY_MANAGEMENT.md](./API_KEY_MANAGEMENT.md)** - 完整使用指南
- **[SECURITY_IMPROVEMENTS.md](./SECURITY_IMPROVEMENTS.md)** - 整改说明
- **[COMPLETION_REPORT.md](./COMPLETION_REPORT.md)** - 完成报告

## 🔒 安全检查

```bash
# 检查代码中是否有硬编码的密钥
python scripts/security_check.py

# 使用 gitleaks 扫描（需要先安装）
brew install gitleaks
gitleaks detect --source . --verbose
```

## ❓ 常见问题

### Q: 我需要配置所有的 API Key 吗？

A: 不需要。至少配置一个 LLM 服务即可。系统会自动选择可用的服务。

### Q: 如何知道哪些服务可用？

```python
from app.core.api_client import api_client_manager

services = api_client_manager.get_available_llm_services()
print(services)
# {'openai': True, 'dashscope': True, 'google': False, ...}
```

### Q: 如何获取 API Key？

- **阿里云千问**: https://dashscope.console.aliyun.com/apiKey
- **OpenAI**: https://platform.openai.com/api-keys
- **Google Gemini**: https://makersuite.google.com/app/apikey
- **DeepSeek**: https://platform.deepseek.com/api_keys

## ⚠️ 重要提醒

**永远不要：**
- ❌ 硬编码 API Key 到代码中
- ❌ 提交 `.env` 文件到 Git
- ❌ 在 commit message 中包含密钥
- ❌ 将生产环境的密钥用于开发或测试

**必须做到：**
- ✅ 所有敏感信息存储在环境变量中
- ✅ 使用 `.env.example` 作为模板（不含真实密钥）
- ✅ 确保 `.env` 在 `.gitignore` 中
- ✅ 定期运行安全检查

## 📞 支持

如有问题，请：
1. 查看 [API_KEY_MANAGEMENT.md](./API_KEY_MANAGEMENT.md)
2. 运行 `python scripts/verify_setup.py` 诊断问题
3. 创建 Issue 或联系项目维护者
