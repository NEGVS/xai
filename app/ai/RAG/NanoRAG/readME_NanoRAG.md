 (base) andy_mac@Andy-FandeMacBook-Pro xai % 

show version

pip show nano-graphrag


Name: nano-graphrag
Version: 0.0.8.2
Summary: A simple, easy-to-hack GraphRAG implementation
Home-page: https://github.com/gusye1234/nano-graphrag
Author: JianbaiYe
Author-email: 
License: 
Location: /Users/andy_mac/PycharmProjects/xai/venv/lib/python3.11/site-packages
Requires: dspy-ai, future, graspologic, hnswlib, nano-vectordb, neo4j, networkx, openai, tenacity, tiktoken, xxhash
Required-by: 
(venv) (base) andy_mac@Andy-FandeMacBook-Pro xai % 


如果版本 < 0.3.0，强烈建议升级（方案 1）。
如果已经是最新版但仍不支持 llm_model_list，说明这个功能可能在 fork 或特定分支中，你可以去 GitHub 仓库（https://github.com/gusye1234/nano-graphrag）看 README 或 issues，确认参数名是否变了。


# 先卸载旧版，避免冲突
pip uninstall nano-graphrag -y

# 安装最新稳定版
pip install nano-graphrag --upgrade

# 如果 PyPI 还没更新到最新，可以直接从 GitHub main 分支安装（推荐）
pip install git+https://github.com/gusye1234/nano-graphrag.git@main
