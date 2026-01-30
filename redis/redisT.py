import redis

# 阿里云Redis配置（替换为你的实际信息）
REDIS_HOST = "r-uf63qqg3rwom4cz59u.redis.rds.aliyuncs.com"
REDIS_PORT = 6379
REDIS_PASSWORD = "dehB5GWF6j7jrMDa"  # 必须填，阿里云Redis默认有密码
REDIS_DB = 8  # 你的库是8，不用改

# 连接Redis
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_DB,
    decode_responses=True,  # 自动解码为字符串，避免二进制乱码
    socket_connect_timeout=10  # 连接超时时间
)

# 用scan分批扫描删除（非阻塞，适合所有数据量）
cursor = 0
delete_count = 0
while True:
    # 扫描sms开头的key，每次扫描200个
    cursor, keys = r.scan(cursor=cursor, match="sms_ip*", count=200)
    print(cursor, keys)
    if keys:
        # 批量删除扫描到的key
        # r.delete(*keys)
        # delete_count += len(keys)

        print(f"已删除{len(keys)}个key，累计删除{delete_count}个")
    # 游标为0时，扫描完成，退出循环
    if cursor == 0:
        break

print(f"删除完成！累计删除sms_ip_开头的key共{delete_count}个")