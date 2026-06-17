# Conda 环境设置指南

## 环境信息
- **环境名称**: xai
- **Python 版本**: 3.11.15
- **位置**: `/opt/anaconda3/envs/xai`

## 如何使用

### 1. 激活环境
```bash
conda activate xai
```

### 2. 退出当前 venv 环境（如果已激活）
```bash
deactivate  # 退出 venv
```

### 3. 验证环境
```bash
# 检查 Python 版本
python --version

# 查看已安装的包
conda list

# 或使用 pip
pip list
```

### 4. 运行项目
```bash
# 激活环境后运行主程序
python main.py
```

## 已安装的主要依赖

### Web 框架
- FastAPI
- Flask
- Uvicorn

### AI/LLM
- OpenAI
- LangChain (langchain, langchain-openai, langchain-community)
- Google Generative AI

### 向量存储
- ChromaDB
- Milvus (pymilvus)

### RAG
- nano-graphrag

### 机器学习
- scikit-learn
- NumPy
- Pandas

### 其他工具
- Pillow (图像处理)
- MoviePy (视频处理)
- Selenium (浏览器自动化)
- psycopg2-binary (PostgreSQL)
- Supabase

## 环境管理

### 更新依赖
```bash
conda activate xai
pip install -r requirements.txt --upgrade
```

### 添加新包
```bashconda info --envs
conda activate xai
pip install package_name

# 更新 requirements.txt
pip freeze > requirements.txt
```

### 导出环境配置
```bash
# 导出为 environment.yml（推荐）
conda env export --no-builds > environment.yml

# 或导出为 requirements.txt
pip freeze > requirements.txt
```

### 删除环境
```bash
conda deactivate
conda remove -n xai --all
```

## 注意事项

1. **不要混用 venv 和 conda**：选择 conda 后，建议删除或不再使用 venv
2. **IDE 配置**：在 PyCharm 中设置 Python 解释器为 `/opt/anaconda3/envs/xai/bin/python`
3. **依赖管理**：使用 `pip` 或 `conda install` 安装新包后，记得更新 requirements.txt

## 常见问题

### Q: 如何在 PyCharm 中使用这个环境？
A: 
1. 打开 PyCharm Settings
2. Project > Python Interpreter
3. 点击齿轮图标 > Add
4. 选择 Conda Environment > Existing environment
5. 选择 `/opt/anaconda3/envs/xai/bin/python`

### Q: 如何切换回 base 环境？
A: 
```bash
conda deactivate
```

### Q: 环境在哪里？
A: 
```bash
conda env list
```

## 快速启动命令

```bash
# 一键启动项目
conda activate aiAgent
conda activate xai && python main.py

# 或者创建别名（添加到 ~/.zshrc）
alias xai-activate="conda activate xai"
alias xai-run="conda activate xai && python main.py"
```
