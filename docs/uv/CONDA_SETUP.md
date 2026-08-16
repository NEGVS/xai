# Conda 环境设置指南

## 环境信息
- **环境名称**: xai
- **Python 版本**: 3.11.15
- **位置**: `/opt/anaconda3/envs/xai`
# 我的使用
1- 环境管理：Conda 管 Python 版本 + 全局环境隔离，UV 管项目依赖、极速安装

2- UV 使用方法
   1- 使用 Conda 切换到对应的环境。
   2- uv init，初始化。 
   3- 新增导入时，使用 uv add openai
   4- 终端设置好后，pycharm中要重新选择一下编译器。

你把.venv删掉了，所以找不到激活文件，现在重新用 uv 生成就行

## 已经在 conda xai 环境里，直接执行
uv venv
生成后激活

source .venv/bin/activate
安装依赖
uv add openai
## 完整正确流程（conda+uv 固定用法）
进入 conda 环境
conda activate xai
项目内创建 uv 虚拟环境（只建一次）
uv venv
激活 uv 环境
source .venv/bin/activate
装包用 uv add，运行用 uv run


# 异常 1
---
(venv) (base) andy_mac@Andy-FandeMacBook-Pro-547 xai % conda env list
# conda environments:
#
base                  *  /opt/anaconda3
aiAgent                  /opt/anaconda3/envs/aiAgent
xai                      /opt/anaconda3/envs/xai

(venv) (base) andy_mac@Andy-FandeMacBook-Pro-547 xai % python --version
Python 3.11.12
(venv) (base) andy_mac@Andy-FandeMacBook-Pro-547 xai %

### 问题说明
你现在**同时嵌套了 conda(base) + 原生venv虚拟环境**，环境乱套了，提示符 `(venv) (base)` 就是典型冲突。

### 现状
1. `conda env list` 有3个环境：
   - base（当前conda默认）
   - aiAgent
   - xai
2. 你现在在`xai`目录，**既进了conda base，又手动开了venv**
3. `python --version` 3.11.1 是外层版本，不是目标虚拟环境版本

---

## 1. 退出双层环境
```bash
# 先退出原生venv
deactivate
# 再退出conda base
conda deactivate
```
提示符变回 `andy_mac@xxx` 干净状态

## 2. 只用Conda管理环境（推荐，抛弃venv）
```bash
# 进入 xai 这个conda环境
conda activate xai

# 查看当前python版本
python --version

# 查看当前所在环境
conda info --envs
```

## 3. 彻底清理多余venv（可选）
```bash
# 删除项目里自建的venv文件夹
rm -rf venv
```

## 4. 日常正确使用流程
```bash
# 打开终端直接进目标环境
conda activate xai

# 退出
conda deactivate
```

## 5. 取消conda默认自动激活base（根治总带base）
```bash
conda config --set auto_activate_base false
```
重启终端就不会一打开就带 `(base)`
------------
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
