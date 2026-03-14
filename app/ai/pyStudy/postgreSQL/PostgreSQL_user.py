import psycopg2
from psycopg2 import errors
import random
import string

# -------------------------- 1. 配置数据库连接参数 --------------------------
PG_CONFIG = {
    "host": "localhost",  # 替换为你的PG主机
    "port": 5432,  # PG默认端口，无需修改除非自定义
    "dbname": "postgres",  # 替换为你的数据库名
    "user": "andy_mac",  # 替换为你的PG用户名
    "password": ""  # 替换为你的PG密码
}


# -------------------------- 2. 生成10条测试数据 --------------------------
def generate_test_data(num=10):
    """生成指定数量的测试用户数据（适配srzp_user.user表结构）"""
    test_data = []
    # 随机生成姓名和邮箱（避免重复）
    for i in range(num):
        # 随机姓名：前缀+数字（如Andy_1、Lisa_2）
        name = f"{random.choice(['Andy', 'Lisa', 'Mike', 'Zhang', 'Li', 'Wang'])}_{i}"
        # 随机邮箱：姓名+随机字符串+@example.com（保证唯一）
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        email = f"{name.lower()}_{random_str}@example.com"
        # 表结构：id（自增无需传）、name、email、create_at（默认当前时间）、update_at（默认NULL）、deleted_at（默认NULL）
        test_data.append((name, email))
    return test_data


# -------------------------- 3. 连接数据库并插入数据 --------------------------
def insert_data_to_pg():
    conn = None
    cursor = None
    try:
        # 1. 建立数据库连接
        print("建立数据库连接")
        conn = psycopg2.connect(**PG_CONFIG)
        # 设置自动提交（可选，插入操作建议显式commit）
        conn.autocommit = False
        cursor = conn.cursor()

        # 2. 生成10条测试数据
        test_data = generate_test_data(num=10)
        print(f"生成的10条测试数据：{test_data}")
        for a, b in test_data:
            print(a, "-", b)
        # 3. 批量插入数据（executemany效率更高，适配多条插入）
        insert_sql = """
            INSERT INTO srzp_user.user (name, email)
            VALUES (%s, %s);  -- id/create_at自动填充，update_at/deleted_at默认NULL
        """
        # 执行批量插入
        cursor.executemany(insert_sql, test_data)
        # 提交事务
        conn.commit()
        print("✅ 10条数据已成功插入srzp_user.user表！")

    except errors.UniqueViolation:
        # 捕获邮箱重复的唯一约束异常
        if conn:
            conn.rollback()  # 回滚事务
        print("❌ 错误：插入的邮箱重复，违反UNIQUE约束！")
    except errors.OperationalError as e:
        # 捕获连接异常（如密码错误、主机不可达）
        print(f"❌ 数据库连接失败：{str(e)}")
    except Exception as e:
        # 捕获其他异常
        if conn:
            conn.rollback()
        print(f"❌ 插入数据失败：{str(e)}")
    finally:
        # 4. 关闭游标和连接（无论成功/失败都执行）
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("🔌 数据库连接已关闭")


# -------------------------- 4. 执行插入操作 --------------------------
if __name__ == "__main__":
    insert_data_to_pg()
