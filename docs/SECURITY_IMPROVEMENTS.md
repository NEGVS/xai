# API Key 安全整改总结

## 整改日期
2026-06-18

## 整改目标
- 消除项目中所有硬编码的 API Key 和敏感信息
- 建立统一的配置管理系统
- 确保所有敏感信息从环境变量获取
- 提供安全检查工具和最佳实践文档

## 主要改动

### 1. 核心配置系统

#### 1.1 更新配置文件 (`app/core/config.py`)
- ✅ 添加 `DASHSCOPE_API_KEY` - 阿里云千问 API 配置
- ✅ 添加 `DASHSCOPE_BASE_URL` - DashScope 基础 URL
- ✅ 添加 `DASHSCOPE_MODEL` - 默认模型配置
- ✅ 添加 `DASHSCOPE_FALLBACK_MODELS` - 备用模型列表
- ✅ 添加 `GOOGLE_API_KEY` - Google AI API 配置
- ✅ 添加 `GEMINI_API_KEY` - Gemini API 配置
- ✅ 添加 `DEEPSEEK_API_KEY` - DeepSeek API 配置

#### 1.2 更新 LLM 服务 (`app/core/llm.py`)
- ✅ 添加 DashScope 客户端支持
- ✅ 使用 OpenAI 兼容模式连接 DashScope
- ✅ 调整默认客户端优先级：DashScope > Anthropic > OpenAI
- ✅ 添加 `get_client("dashscope")` 方法

#### 1.3 创建统一的 API 客户端管理器 (`app/core/api_client.py`)
- ✅ 实现单例模式，确保配置只加载一次
- ✅ 集中管理所有 LLM 服务的 API 客户端
- ✅ 提供同步和异步客户端
- ✅ 支持服务可用性检查
- ✅ 提供统一的 API Key 获取接口

支持的服务：
- OpenAI (同步 + 异步)
- DashScope/千问 (同步 + 异步)
- DeepSeek (同步 + 异步)
- Anthropic Claude
- Google Gemini
- News API
- Alpha Vantage

### 2. 修复硬编码的 API Key

#### 2.1 Google API 相关文件（8 个文件）
| 文件 | 状态 |
|------|------|
| `app/controller/flask/flask_genAI.py` | ✅ 已修复 |
| `app/ai/openAi/google/gemini_Image_editing.py` | ✅ 已修复 |
| `app/ai/openAi/google/gemini_Image_Test.py` | ✅ 已修复 |
| `app/ai/openAi/google/gemini_Text_Test.py` | ✅ 已修复 |
| `app/ai/openAi/google/streamingOutput.py` | ✅ 已修复 |
| `app/ai/openAi/google/VeoTest.py` | ✅ 已修复 |
| `app/ai/openAi/google/gemini_image_generate.py` | ✅ 已修复 |
| `app/ai/openAi/google/genAI/GenAI.py` | ✅ 已修复 |

修复方式：
```python
# 修复前
client = genai.Client(api_key="AIzaSyCY0pgtmhJbisYENnNgWzd0m_u5vKdiB8U")

# 修复后
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("请设置 GOOGLE_API_KEY 或 GEMINI_API_KEY 环境变量")
client = genai.Client(api_key=api_key)
```

#### 2.2 数据库密码相关文件
| 文件 | 问题 | 状态 |
|------|------|------|
| `app/ai/pyStudy/redis/redisT.py` | Redis 密码硬编码 | ✅ 已修复 |
| `test/srzp.py` | MySQL 密码硬编码 | ✅ 已修复 |

#### 2.3 文档文件
| 文件 | 问题 | 状态 |
|------|------|------|
| `app/ai/openAi/google/readMe.md` | 文档中包含真实 API Key | ✅ 已修复 |

### 3. 环境变量配置

#### 3.1 更新 `.env.example`
添加了以下配置项：

**LLM 服务：**
- `DASHSCOPE_API_KEY` - 阿里云千问
- `DASHSCOPE_BASE_URL` - DashScope API 地址
- `DASHSCOPE_MODEL` - 默认模型
- `GOOGLE_API_KEY` - Google AI
- `GEMINI_API_KEY` - Gemini
- `DEEPSEEK_API_KEY` - DeepSeek

**数据库：**
- `REDIS_HOST` - Redis 主机
- `REDIS_PORT` - Redis 端口
- `REDIS_PASSWORD` - Redis 密码
- `REDIS_DB` - Redis 数据库索引
- `MYSQL_HOST` - MySQL 主机
- `MYSQL_USER` - MySQL 用户
- `MYSQL_PASSWORD` - MySQL 密码
- `MYSQL_DATABASE` - MySQL 数据库名

**数据源：**
- `NEWS_API_KEY` - NewsAPI
- `ALPHA_VANTAGE_API_KEY` - Alpha Vantage

### 4. 安全工具

#### 4.1 安全检查脚本 (`scripts/security_check.py`)
创建了自动化安全扫描工具，可以检测：
- ✅ 硬编码的 API Key
- ✅ 数据库连接字符串中的密码
- ✅ 硬编码的 Token
- ✅ 私钥文件
- ✅ AWS 密钥
- ✅ Google API 密钥

特性：
- 自动跳过占位符（placeholder、dummy、example 等）
- 支持扫描多种文件类型（.py, .js, .ts, .java, .yml, .yaml, .json）
- 排除 venv、node_modules 等目录
- 提供详细的问题报告

使用方法：
```bash
python scripts/security_check.py
```

### 5. 文档

#### 5.1 API Key 管理指南 (`docs/API_KEY_MANAGEMENT.md`)
创建了完整的最佳实践文档，包含：
- ✅ 核心安全原则
- ✅ 配置系统使用指南
- ✅ 支持的 LLM 服务列表
- ✅ 代码示例（正确 vs 错误）
- ✅ 安全检查工具使用
- ✅ Pre-commit Hook 设置
- ✅ 故障排查指南
- ✅ 紧急情况处理流程

#### 5.2 整改总结 (`docs/SECURITY_IMPROVEMENTS.md`)
本文档，记录了所有改动。

## 配置使用示例

### 使用统一的 API Client Manager（推荐）

```python
from app.core.api_client import api_client_manager

# 获取 DashScope 客户端
client = api_client_manager.get_dashscope_client()

# 获取异步客户端
async_client = api_client_manager.get_dashscope_client(async_mode=True)

# 获取默认客户端（自动选择可用的服务）
default_client = api_client_manager.get_default_llm_client()

# 检查服务是否可用
if api_client_manager.has_service("dashscope"):
    print("DashScope 可用")

# 获取 API Key
google_key = api_client_manager.get_api_key("google")
```

### 使用 LLM Service（LangChain 集成）

```python
from app.core.llm import llm_service

# 获取指定的客户端
dashscope_client = llm_service.get_client("dashscope")
anthropic_client = llm_service.get_client("anthropic")

# 使用默认客户端
response = await llm_service.analyze_sentiment("这是一个很好的产品")
```

### 直接使用 Settings

```python
from app.core.config import settings

# 获取配置
api_key = settings.DASHSCOPE_API_KEY
base_url = settings.DASHSCOPE_BASE_URL
model = settings.DASHSCOPE_MODEL
```

## 环境变量设置

### 开发环境

1. 复制模板文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入真实的 API Key：


3. 加载环境变量（如果使用命令行）：
```bash
source .env
# 或
export $(cat .env | xargs)
```

### 生产环境

使用环境变量或密钥管理服务：
```bash
# 直接设置环境变量
export DASHSCOPE_API_KEY="your-production-key"

# 或使用 AWS Secrets Manager、Azure Key Vault 等
```

## 安全检查清单

### 提交代码前

- [ ] 运行安全检查脚本：`python scripts/security_check.py`
- [ ] 确认没有硬编码的密钥
- [ ] 确认 `.env` 文件没有被提交
- [ ] 确认 `.gitignore` 包含 `.env`
- [ ] 检查 commit message 中没有密钥

### 代码审查时

- [ ] 检查是否使用 `os.getenv()` 或统一的配置服务
- [ ] 检查是否有硬编码的连接字符串
- [ ] 检查测试文件中是否使用了真实的密钥
- [ ] 检查文档中是否包含真实的密钥

### 定期检查

- [ ] 每月运行一次 `gitleaks detect`
- [ ] 审查所有有权访问密钥的人员
- [ ] 轮换长期使用的密钥
- [ ] 检查密钥使用日志，识别异常活动

## 统计数据

### 修复的文件数量
- **硬编码 API Key**: 8 个文件
- **硬编码密码**: 2 个文件
- **文档更新**: 1 个文件
- **总计**: 11 个文件

### 新增的文件
- `app/core/api_client.py` - 统一的 API 客户端管理器
- `scripts/security_check.py` - 安全检查脚本
- `docs/API_KEY_MANAGEMENT.md` - API Key 管理指南
- `docs/SECURITY_IMPROVEMENTS.md` - 本文档

### 更新的文件
- `app/core/config.py` - 添加新的配置项
- `app/core/llm.py` - 添加 DashScope 支持
- `.env.example` - 更新配置模板

## 后续建议

### 短期（1 周内）
1. ✅ 团队成员更新本地 `.env` 配置
2. ✅ 设置 pre-commit hook
3. ✅ 运行一次完整的安全扫描

### 中期（1 个月内）
1. 🔄 集成 gitleaks 到 CI/CD 流程
2. 🔄 实施密钥轮换策略
3. 🔄 为生产环境配置密钥管理服务（AWS Secrets Manager/Azure Key Vault）

### 长期
1. 📝 建立密钥访问审计日志
2. 📝 实施最小权限原则
3. 📝 定期进行安全培训

## 测试验证

### 验证环境变量加载

```python
# 测试脚本
from app.core.config import settings
from app.core.api_client import api_client_manager

print("配置验证:")
print(f"- DASHSCOPE_API_KEY: {'已配置' if settings.DASHSCOPE_API_KEY else '未配置'}")
print(f"- OPENAI_API_KEY: {'已配置' if settings.OPENAI_API_KEY else '未配置'}")
print(f"- GOOGLE_API_KEY: {'已配置' if settings.GOOGLE_API_KEY else '未配置'}")

print("\n可用服务:")
services = api_client_manager.get_available_llm_services()
for service, available in services.items():
    status = "✅" if available else "❌"
    print(f"{status} {service}")
```

### 验证 API 调用

```python
# 测试 DashScope 连接
from app.core.api_client import api_client_manager

client = api_client_manager.get_dashscope_client()
if client:
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": "测试连接"}]
    )
    print("✅ DashScope 连接成功")
    print(f"响应: {response.choices[0].message.content}")
else:
    print("❌ DashScope 不可用")
```

## 相关资源

- [CLAUDE.md](../CLAUDE.md) - 项目设计文档
- [API_KEY_MANAGEMENT.md](./API_KEY_MANAGEMENT.md) - 详细的使用指南
- [.env.example](../.env.example) - 环境变量模板
- [security_check.py](../scripts/security_check.py) - 安全检查工具

## 联系方式

如有问题或建议，请联系项目维护者或创建 Issue。

---

**整改完成日期**: 2026-06-18  
**文档版本**: 1.0  
**下次审查日期**: 2026-07-18
