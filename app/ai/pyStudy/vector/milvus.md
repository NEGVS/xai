1-使用python链接milvus数据库
pip install pymilvus

collection not loaded → 集合没有加载到内存，所以无法查询数据。
Milvus 的规则：集合必须 load 加载后，才能查询、搜索，否则直接报错 101。