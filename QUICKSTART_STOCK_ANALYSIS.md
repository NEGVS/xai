# 🚀 快速启动指南

## 5分钟快速上手

### 第1步：安装依赖（2分钟）

```bash
cd /Users/andy_mac/PycharmProjects/xai
pip install -r requirements.txt
```

### 第2步：配置API密钥（1分钟）

```bash
# 复制环境变量模板
cp .env.template .env

# 编辑.env文件，至少配置一个LLM API密钥：
# OPENAI_API_KEY=sk-...
# 或
# ANTHROPIC_API_KEY=sk-ant-...
```

**推荐使用Claude**（性价比更高）：
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

### 第3步：启动服务（10秒）

```bash
./start.sh
```

服务启动后会看到：
```
🚀 启动 Stock Analysis Multi-Agent System...
🌐 启动FastAPI服务...
📝 API文档: http://localhost:8000/docs
🏥 健康检查: http://localhost:8000/api/v1/agents/health
```

### 第4步：测试（1分钟）

#### 方式1：浏览器测试
打开 http://localhost:8000/docs

点击 `POST /api/v1/analysis/stock`，输入：
```json
{
  "symbol": "AAPL",
  "analysis_type": "full",
  "time_range": "1M"
}
```

点击 Execute，等待30-45秒即可看到完整分析报告！

#### 方式2：命令行测试
```bash
curl -X POST "http://localhost:8000/api/v1/analysis/stock" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}'
```

#### 方式3：Python测试脚本
```bash
python test_analysis.py
```

---

## 📊 测试其他股票

```bash
# Apple
curl -X POST "http://localhost:8000/api/v1/analysis/stock" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}'

# Tesla
curl -X POST "http://localhost:8000/api/v1/analysis/stock" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "TSLA"}'

# Microsoft
curl -X POST "http://localhost:8000/api/v1/analysis/stock" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "MSFT"}'

# NVIDIA
curl -X POST "http://localhost:8000/api/v1/analysis/stock" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "NVDA"}'
```

---

## 🔍 常见问题

### Q1: 提示"至少需要配置一个LLM API Key"
**解决**：编辑 `.env` 文件，添加 `OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY`

### Q2: 无法获取股票数据
**解决**：
- 检查网络连接
- 确认使用美股代码（如AAPL而非苹果）
- yfinance偶尔会有延迟，稍后重试

### Q3: 依赖安装失败
**解决**：
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Q4: 想使用NewsAPI获取真实新闻
**可选**：在 `.env` 中添加
```bash
NEWS_API_KEY=your_newsapi_key
```
不配置也能正常运行（使用模拟新闻数据）

---

## 📚 更多文档

- **API使用文档**: README_API.md
- **项目总结**: PROJECT_SUMMARY.md
- **设计文档**: CLAUDE.md

---

## 🎯 下一步

1. ✅ 测试不同的股票代码
2. ✅ 查看完整的分析报告
3. ✅ 探索API文档（http://localhost:8000/docs）
4. ✅ 根据需求定制Agent逻辑
5. ✅ 添加前端界面（Vue3）

---

**开始探索吧！** 🚀
