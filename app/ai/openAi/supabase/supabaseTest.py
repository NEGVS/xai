import os
import time

from supabase import create_client, Client
from datetime import datetime
import uuid
import random
import threading


# # supabase: Client = create_client(url, key)
def get_supabase_client() -> Client:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)


def insert_order(supabase: Client, user_id: int, amount: float):
    """插入一条订单数据"""
    order_no = f"ORD-{uuid.uuid4().hex[:10].upper()}"
    order = {
        "order_no": order_no,
        "user_id": user_id,
        "amount": amount,
        "status": "PENDING",
        "version": 1,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }

    response = supabase.table("orders").insert(order).execute()
    if response.data:
        print(f"✅ -----------插入成功: {response.data[0]}")
        return response.data[0]
    else:
        print("⚠️ 插入失败:", response)
        return None


# data,count =supabase.table('orders').select('*').execute()
def query_orders(supabase: Client, limit: int = 5):
    # query orders
    response = supabase.table('orders').select('*').order('created_at', desc=True).limit(limit).execute()
    print(f"query {len(response.data)} 条订单：")
    for row in response.data:
        print(row)
    response_page = supabase.table("orders").select("*").range(0, 1).execute()  # 查询前20条
    print(response_page)
    response_status = supabase.table("orders").select("*").eq("status", "PENDING").execute()
    print(response_status)

    return response.data


# 2 delete
def delete_order(supabase: Client, order_no: str):
    """删除订单"""
    response = supabase.table("orders").delete().eq("order_no", order_no).execute()
    if response.data:
        print(f"✅ 删除成功: {response.data[0]}")
    else:
        print(f"⚠️ 删除失败: 未找到订单 {order_no}")


# 3 update
def update_order_status(supabase: Client, order_no: str, new_status: str, delay=0):
    """更新订单状态（带乐观锁 version 检查）"""
    # 延迟模拟并发重叠
    if delay > 0:
        time.sleep(delay)
    # 查询当前版本
    res = supabase.table("orders").select("version").eq("order_no", order_no).single().execute()
    if not res.data:
        print(f"⚠️ 未找到订单: {order_no}")
        return None

    current_version = res.data["version"]
    new_version = current_version + 1

    # 更新时校验 version
    response = (
        supabase.table("orders")
        .update({
            "status": new_status,
            "version": new_version,
            "updated_at": datetime.now().isoformat()
        })
        .eq("order_no", order_no)
        .eq("version", current_version)  # 乐观锁检查
        .execute()
    )

    if response.data:
        print(f"✅ 状态更新成功: {response.data[0]}")
        return response.data[0]
    else:
        print("⚠️ 更新失败，可能是 version 不匹配（并发冲突）")
        return None


# ======================== 并发模拟 ==========================
def simulate_concurrent_updates(supabase: Client):
    #     1,insert a new order
    order = insert_order(supabase, random.randint(1000, 2000), round(random.uniform(10.0, 999.99), 2))
    order_no = order["order_no"]
    print(f"\n🎯 开始并发模拟: order_no={order_no}\n")
    # 2,create two thread
    t1 = threading.Thread(target=update_order_status, args=(supabase, order_no, "ANDY", 0))
    t2 = threading.Thread(target=update_order_status, args=(supabase, order_no, "DEMI", 0.01))
    # 3,start thread
    t1.start()
    t2.start()
    # 4,waiting for end
    t1.join()
    t2.join()

    #5,final result
    final = supabase.table('orders').select('status,version').eq('order_no',order_no).single().execute()
    print(f"\n🏁 最终状态: {final.data}")

if __name__ == '__main__':
    supabase = get_supabase_client()
    #     insert orders
    insert_order(supabase, 1, 1)
    for index in range(10):
        user_id = random.randint(1000, 2000)
        amount = round(random.uniform(10.0, 999.99), 2)
        insert_order(supabase, user_id, amount)
    # --- 随机生成逻辑 ---
    # user_id = user_id or random.randint(1000, 2000)
    # amount = amount or round(random.uniform(10.0, 999.99), 2)
    #     query

    query_orders(supabase, 55)

    # 1️⃣ 插入新订单
    print('\n----------插入新订单')

    order = insert_order(supabase, 1001, 199.99)
    # 3️⃣ 更新订单状态（带乐观锁）
    print('\n----------order')
    print(order)
    print(order["order_no"])
    if order:
        update_order_status(supabase, order["order_no"], "PAID")
    print('\n=======---simulate_concurrent_updates')

    simulate_concurrent_updates(supabase)
    # 4️⃣ 删除测试订单（可选）
    # delete_order(supabase, order["order_no"])
