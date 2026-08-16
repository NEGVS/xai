import csv


def read_csv_unique_keys(file_path: str) -> set:
    """
    读取csv，拼接 user_id_business_user_id_job_id 作为唯一标识存入集合
    空字段、无法转数字的脏数据自动跳过
    """
    key_set = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_id = row.get("user_id", "").strip()
                bus_uid = row.get("business_user_id", "").strip()
                job_uid = row.get("job_id", "").strip()

                # 任意字段为空直接跳过
                if not user_id or not bus_uid or not job_uid:
                    continue

                try:
                    bus_id = int(bus_uid)
                    job_id = int(job_uid)
                except ValueError:
                    # 数字转换失败，丢弃脏数据
                    continue

                combine_key = f"{user_id}_{bus_id}_{job_id}"
                key_set.add(combine_key)
    except FileNotFoundError:
        print(f"错误：文件不存在 -> {file_path}")
    return key_set


if __name__ == "__main__":
    # 文件路径
    file_a = '/Users/andy_mac/PycharmProjects/xai/docs/file/Result_21.csv'
    file_b = '/Users/andy_mac/PycharmProjects/xai/docs/file/srzp_application_srzon_match_greet_record.csv'

    # 读取两份数据集合
    set_a = read_csv_unique_keys(file_a)
    set_b = read_csv_unique_keys(file_b)

    # 集合运算
    intersection = set_a & set_b  # 交集：两者共有
    union = set_a | set_b  # 并集：全部合并去重
    only_a = set_a - set_b  # A有、B没有
    only_b = set_b - set_a  # B有、A没有

    # 统计打印
    print("===== 数据统计 =====")
    print(f"文件A总条数：{len(set_a)}")
    print(f"文件B总条数：{len(set_b)}")
    print(f"交集数量：{len(intersection)}")
    print(f"并集总数量：{len(union)}")
    print(f"A独有(在A不在B)：{len(only_a)}")
    print(f"B独有(在B不在A)：{len(only_b)}")

    # 如需查看A独有明细，取消下面注释
    # print("\n===== A独有明细 =====")
    # for item in only_a:
    #     uid, bid, jid = item.split("_")
    #     print(uid, bid, jid)
    # 打印B独有明细（差集内容）
    print("\n===== B独有差集明细（B有A没有） =====")
    for item in only_b:
        user_id, business_user_id, job_id = item.split("_")
        print(f"user_id:{user_id}, business_user_id:{business_user_id}, job_id:{job_id}")
