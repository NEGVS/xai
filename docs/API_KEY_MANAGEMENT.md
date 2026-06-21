# API Key 管理指南

## 概述

本文档说明如何在项目中安全地管理 API Key 和其他敏感信息。

## 核心原则

### ✅ 必须做到

1. **所有敏感信息必须存储在环境变量中**
   - API Keys
   - 密码
   - 数据库连接字符串
   - Token 和密钥

2. **使用统一的配置管理**
   - 通过 `app/core/config.py` 集中管理所有配置
   - 通过 `app/core/api_client.py` 统一管理 API 客户端
   - 避免在多处重复获取环境变量

3. **版本控制最佳实践**
   - ✅ 提交 `.env.example` (包含占位符)
   - ❌ 永不提交 `.env` (包含真实密钥)
   - ✅ 确保 `.env` 在 `.gitignore` 中

4. **Pre-commit Hook**
   - 运行 `scripts/security_check.py` 检测硬编码的密钥
   - 在提交前自动扫描潜在的安全问题

5. **使用 Git Secrets 工具**
   - 安装 gitleaks: `brew install gitleaks`
   - 运行扫描: `gitleaks detect --source . --verbose`



2. **不要提交 .env 文件**


4. **不要提交 RAG dump 或包含密钥的数据文件**

5. **不要将生产环境的密钥复制到 demo 或测试环境**

## 配置系统

### 1. 环境变量配置

项目使用 `.env` 文件管理环境变量：

```bash
# 复制模板文件
cp .env.example .env

# 编辑 .env 文件，填入真实的 API Key
vim .env
```

### 2. 支持的 LLM 服务

#### OpenAI

#### Anthropic Claude

#### 阿里云 DashScope (千问)

#### Google Gemini
```

#### DeepSeek

### 3. 使用统一的配置服务

#### 方法 1：通过 Settings (推荐)


```

#### 方法 2：通过 API Client Manager (推荐用于客户端)

```python
from app.core.api_client import api_client_manager

# 获取 OpenAI 客户端
client = api_client_manager.get_openai_client()

# 获取 DashScope 客户端 (异步)
async_client = api_client_manager.get_dashscope_client(async_mode=True)

# 获取默认 LLM 客户端
default_client = api_client_manager.get_default_llm_client()

# 获取特定服务的 API Key
google_key = api_client_manager.get_api_key("google")

# 检查服务是否可用
if api_client_manager.has_service("dashscope"):
    print("DashScope 服务可用")
```

#### 方法 3：通过 LLM Service (用于 LangChain)

```python
from app.core.llm import llm_service

# 获取指定的 LLM 客户端
client = llm_service.get_client("dashscope")  # 或 "openai", "anthropic"

# 使用默认客户端
default_client = llm_service.default_client

# 调用 LLM 服务
result = await llm_service.analyze_sentiment("这是一个很好的产品")
```

## 最佳实践示例

### 示例 1：初始化 LLM 客户端

```python
"""
正确的方式：使用统一的配置管理
"""
from app.core.api_client import api_client_manager

class MyAgent:
    def __init__(self):
        # 使用统一的客户端管理器
        self.client = api_client_manager.get_dashscope_client(async_mode=True)
        
        if not self.client:
            raise ValueError("DashScope 客户端不可用，请检查 DASHSCOPE_API_KEY 配置")
    
    async def generate(self, prompt: str):
        response = await self.client.chat.completions.create(
            model="qwen-plus",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
```

### 示例 2：多个 LLM 服务的 Fallback

```python
from app.core.api_client import api_client_manager

class RobustLLMService:
    def __init__(self):
        self.clients = []
        
        # 按优先级添加可用的客户端
        if api_client_manager.has_service("dashscope"):
            self.clients.append(("dashscope", api_client_manager.get_dashscope_client()))
        
        if api_client_manager.has_service("openai"):
            self.clients.append(("openai", api_client_manager.get_openai_client()))
        
        if not self.clients:
            raise ValueError("没有可用的 LLM 服务")
    
    def generate(self, prompt: str):
        last_error = None
        
        for service_name, client in self.clients:
            try:
                response = client.chat.completions.create(
                    model="qwen-plus" if service_name == "dashscope" else "gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"{service_name} 失败: {e}")
                last_error = e
                continue
        
        raise last_error or Exception("所有 LLM 服务均不可用")
```

### 示例 3：Google Gemini 客户端

```python
import os
from google import genai

def create_gemini_client():
    """创建 Gemini 客户端的正确方式"""
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("请设置 GOOGLE_API_KEY 或 GEMINI_API_KEY 环境变量")
    
    return genai.Client(api_key=api_key)

# 使用
client = create_gemini_client()
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello, world!"
)
```

## 安全检查

### 运行安全扫描

```bash
# 运行项目内置的安全检查脚本
python scripts/security_check.py

# 使用 gitleaks 扫描
gitleaks detect --source . --verbose

# 使用 git-secrets (如果安装)
git secrets --scan
```

### Pre-commit Hook 设置

创建 `.git/hooks/pre-commit`:

```bash
#!/bin/sh

echo "🔍 运行安全检查..."

# 运行安全扫描
python scripts/security_check.py

if [ $? -ne 0 ]; then
    echo "❌ 安全检查失败！请修复问题后再提交。"
    exit 1
fi

echo "✅ 安全检查通过"
exit 0
```

设置可执行权限：

```bash
chmod +x .git/hooks/pre-commit
```

## 环境变量清单

### LLM 服务

| 环境变量 | 说明 | 必需 | 示例           |
|---------|------|------|--------------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | 否 | `sksj-...`   |
| `ANTHROPIC_API_KEY` | Anthropic Claude API 密钥 | 否 | `sk-ant-...` |
| `DASHSCOPE_API_KEY` | 阿里云千问 API 密钥 | 否 | `sk-...`     |
| `GOOGLE_API_KEY` | Google AI API 密钥 | 否 | `AIza...`    |
| `GEMINI_API_KEY` | Gemini API 密钥 | 否 | `AIza...`    |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | 否 | `sk-...`     |

### 数据源服务

| 环境变量 | 说明 | 必需 | 示例 |
|---------|------|------|------|
| `NEWS_API_KEY` | NewsAPI 密钥 | 否 | `xxx...` |
| `ALPHA_VANTAGE_API_KEY` | Alpha Vantage API 密钥 | 否 | `xxx...` |

### 数据库

| 环境变量 | 说明 | 必需 | 示例 |
|---------|------|------|------|
| `DATABASE_URL` | PostgreSQL 连接字符串 | 是 | `postgresql://user:pass@localhost:5432/db` |
| `REDIS_URL` | Redis 连接字符串 | 否 | `redis://localhost:6379` |
| `REDIS_PASSWORD` | Redis 密码 | 否 | `xxx...` |
| `MYSQL_HOST` | MySQL 主机 | 否 | `localhost` |
| `MYSQL_USER` | MySQL 用户 | 否 | `root` |
| `MYSQL_PASSWORD` | MySQL 密码 | 否 | `xxx...` |
| `MYSQL_DATABASE` | MySQL 数据库名 | 否 | `xai` |

## 故障排查

### 问题 1：找不到 API Key

**错误信息**：
```
ValueError: 请设置 DASHSCOPE_API_KEY 环境变量
```

**解决方案**：
```bash
# 检查环境变量是否设置
echo $DASHSCOPE_API_KEY

# 如果为空，设置环境变量
export DASHSCOPE_API_KEY="your-api-key"

# 或者在 .env 文件中添加
echo 'DASHSCOPE_API_KEY=your-api-key' >> .env
```

### 问题 2：.env 文件未加载

**解决方案**：
确保在应用启动时加载了 `.env` 文件：

```python
from dotenv import load_dotenv

# 在应用启动时加载
load_dotenv()
```

或使用 pydantic-settings（推荐）：

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        case_sensitive = True
```

### 问题 3：多处重复获取环境变量

**问题**：
```python
# ❌ 在多个文件中重复获取
api_key = os.getenv("DASHSCOPE_API_KEY")
```

**解决方案**：
使用统一的配置管理：

```python
# ✅ 使用 API Client Manager
from app.core.api_client import api_client_manager

client = api_client_manager.get_dashscope_client()
```

## 参考资源

- [12-Factor App: Config](https://12factor.net/config)
- [OWASP: Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

## 紧急情况处理

### 如果不小心提交了 API Key

1. **立即轮换密钥**
   - 前往 API 提供商的控制台
   - 删除或禁用泄露的密钥
   - 生成新的密钥

2. **从 Git 历史中删除**
   ```bash
   # 使用 git filter-branch (危险操作，请备份)
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch path/to/file" \
     --prune-empty --tag-name-filter cat -- --all
   
   # 或使用 BFG Repo-Cleaner (推荐)
   bfg --replace-text passwords.txt
   ```

3. **强制推送**
   ```bash
   git push origin --force --all
   git push origin --force --tags
   ```

4. **通知团队成员**
   - 让所有协作者重新克隆仓库
   - 更新 CI/CD 环境变量

## 总结

- ✅ 使用环境变量存储所有敏感信息
- ✅ 使用统一的配置管理系统
- ✅ 定期运行安全扫描
- ✅ 设置 pre-commit hook
- ❌ 永不硬编码 API Key
- ❌ 永不提交 .env 文件
- ❌ 永不在 commit log 中包含密钥
