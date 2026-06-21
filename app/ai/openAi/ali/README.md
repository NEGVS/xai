# 阿里云千问问答机器人 - 使用说明

## 📦 文件说明

### Python 文件
- `aliChat.py` - 普通输出问答机器人（一次性显示完整答案）
- `aliChatStream.py` - 流式输出问答机器人（逐字显示答案）

### 启动脚本（推荐使用）
- `run_aliChat.sh` - 启动普通版本
- `run_aliChatStream.sh` - 启动流式版本

## 🚀 使用方法

### 方法1：使用启动脚本（推荐，已解决中文输入问题）

```bash
# 普通输出版本
./run_aliChat.sh

# 流式输出版本
./run_aliChatStream.sh
```

### 方法2：直接运行 Python 文件

如果遇到中文输入问题，先设置环境变量：

```bash
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 然后运行
python app/ai/openAi/ali/aliChat.py
# 或
python app/ai/openAi/ali/aliChatStream.py
```

## 🔧 环境要求

### 必需的环境变量
```bash
export DASHSCOPE_API_KEY="your_api_key_here"
```

### 检查是否已配置
```bash
echo $DASHSCOPE_API_KEY
```

## 💡 使用示例

### 启动后的交互
```
请输入问题: 什么是人工智能？
AI回答:
人工智能（Artificial Intelligence，简称 AI）...
```

### 退出程序
输入 `exit` 或按 `Ctrl+C`

## 🐛 常见问题

### 1. 无法输入中文
**原因**: 终端环境变量未设置

**解决方案**:
- 使用启动脚本（`run_aliChat.sh` 或 `run_aliChatStream.sh`）
- 或手动运行: `source ~/.zshrc` 后再启动

### 2. API Key 错误
**错误信息**: `请设置 DASHSCOPE_API_KEY 环境变量`

**解决方案**:
```bash
export DASHSCOPE_API_KEY="your_api_key_here"
```

### 3. 模块未找到
**错误信息**: `ModuleNotFoundError: No module named 'openai'`

**解决方案**:
```bash
pip install openai
```

## 📊 两个版本的区别

| 特性 | aliChat.py | aliChatStream.py |
|------|-----------|------------------|
| 输出方式 | 一次性显示 | 逐字显示 |
| 响应速度 | 等待完成后显示 | 立即开始显示 |
| 用户体验 | 简洁直接 | 类似ChatGPT |
| 适用场景 | 快速问答 | 长回答、更好的交互 |

## 🎯 程序化调用示例

如果要在代码中使用：

```python
import asyncio
from app.ai.openAi.ali.aliChat import AliChat

async def main():
    bot = AliChat()
    await bot.ask("你的问题")

asyncio.run(main())
```

## 📝 注意事项

1. **API Key 安全**: 不要将 API Key 提交到 Git
2. **终端选择**: 推荐使用 iTerm2 或 macOS Terminal
3. **网络连接**: 需要能访问阿里云 API
4. **Token 消耗**: 每次对话会消耗 token，注意成本

## 🔗 相关链接

- 阿里云 DashScope: https://dashscope.aliyuncs.com/
- 千问模型文档: https://help.aliyun.com/zh/dashscope/
