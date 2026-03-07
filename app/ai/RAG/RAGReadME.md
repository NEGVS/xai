from langchain_openai import ChatOpenAI,OpenAIEmbeddings,爆红
模块未安装：

如果你没有安装 langchain_openai 包，Python 会抛出 ModuleNotFoundError: No module named 'langchain_openai'。
即使 langchain_openai 已安装，但如果版本不兼容或环境配置有问题，也可能导致导入失败。
# 安装 langchain_openai 包
pip install langchain-openai
如果已安装，检查版本是否最新
pip install --upgrade langchain-openai


确认你使用的 Python 环境已安装 langchain_openai。可以用以下命令检查：
bashpip show langchain-openai

# 安装 langchain_community 和 chromadb
pip install langchain-community chromadb
检测是否安装
pip show langchain-community
pip show chromadb
查看当前版本
pip list | grep langchain
pip list | grep chromadb


[//]: # (-------)
如果使用虚拟环境，确保激活了正确的环境：
bashsource venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
