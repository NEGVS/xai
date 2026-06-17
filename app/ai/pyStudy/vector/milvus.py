from pymilvus import MilvusClient

# 连接 Milvus
print("连接 Milvus")
client = MilvusClient(
    uri="http://localhost:19530",  # 你的地址
    token=""  # 没有密码就留空：root:Milvus
)

# 1. 查看有哪些集合（表）
collections = client.list_collections()
print("=== 所有集合 ===")
print(collections)
# ['test_vector_collection', 'andy_vectors', 'andy_vectorsV2']
# 2-
print("=== 获取集合schema ===")
for coll in collections:
    # ======================
    # 关键修复：先加载集合！
    # ======================
    client.load_collection(collection_name=coll)

    print(coll)
    schema = client.describe_collection(collection_name=coll)
    print(schema)

# 3-
print("=== 获取集合 数据条数 ===")
for coll in collections:

    print(coll)
    count = client.query(
        collection_name=coll,
        output_fields=["count(*)"]
    )
    print("数据条数：", count)


# 2. 遍历每个集合，查看前 10 条数据
for coll in collections:
    print(f"\n=== 集合：{coll} 数据预览（前10条）===")

    if coll == 'test_vector_collection':
        continue
    # 查询数据（不指定条件 = 查全部）
    res = client.query(
        collection_name=coll,
        filter="",
        limit=10
    )

    # 打印
    for item in res:
        print(item)
