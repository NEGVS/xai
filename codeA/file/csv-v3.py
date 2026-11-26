#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取岗位关联表CSV并生成INSERT SQL语句
修复：list调用strip报错 + 列索引混乱问题
"""
import csv
import re
from datetime import datetime

# 输入文件路径
csv_file = '/Users/andy_mac/Documents/CodeSpace/srzp/ai-engineering-center/docs/todo/岗位关联表_-_关联关系表V2.0.csv'
# 输出文件路径
output_file = '/Users/andy_mac/Documents/CodeSpace/srzp/ai-engineering-center/docs/todo/generated_sql-3.sql'


def extract_nums(text: str) -> list[int]:
    """
    1. 根据、分割字符串
    2. 提取每个片段里的数字，返回int列表
    示例："10服务员、13餐饮收银员、92酒吧服务员" → [10,13,92]
    """
    if not isinstance(text, str):
        return []
    parts = text.split("、")
    res = []
    for p in parts:
        match = re.search(r"\d+", p)
        if match:
            res.append(int(match.group()))
    return res


def num_list_to_str(num_list: list[int]) -> str:
    """数字列表转为逗号分隔字符串，空列表返回空字符串"""
    if not num_list:
        return ""
    return ",".join(str(x) for x in num_list)


def clean_value(value):
    """
    清理字段值，去除多余空格和引号
    兼容：字符串输入；列表不再进这个函数，提前转字符串
    """
    if not value:
        return "''"
    # 只处理字符串
    if not isinstance(value, str):
        value = str(value)
    value = value.strip().strip('"').strip()
    if not value or value == '000' or value == '000,000,000':
        return "''"
    # 转义单引号
    value = value.replace("'", "''")
    return f"'{value}'"


def generate_sql():
    sql_statements = []

    print('start read csv...')
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        # 跳过标题行
        next(reader)

        for row in reader:
            if len(row) < 11:
                print(f"跳过行（字段不足）: {row}")
                continue

            # ========== 修正列索引，按你原始注释重新对齐 ==========
            group_code = row[0].strip()  # 第1列：组ID
            name = row[1].strip()        # 第2列：虚拟大类名
            a2_raw = row[4].strip().strip('"')  # 原A2级匹配
            a3_raw = row[5].strip().strip('"')  # 原A3级匹配
            b_raw = row[7].strip().strip('"')   # 原B级匹配
            c_raw = row[9].strip().strip('"')   # 原C级匹配

            # 提取数字列表，并转为逗号字符串
            a2_match_str = num_list_to_str(extract_nums(a2_raw))
            a3_match_str = num_list_to_str(extract_nums(a3_raw))
            b_match_str = num_list_to_str(extract_nums(b_raw))
            c_match_str = num_list_to_str(extract_nums(c_raw))

            # 跳过空行
            if not group_code or not name:
                continue

            # 清理值
            group_code_sql = clean_value(group_code)
            name_sql = clean_value(name)
            a2_match_sql = clean_value(a2_match_str)
            a3_match_sql = clean_value(a3_match_str)
            b_match_sql = clean_value(b_match_str)
            c_match_sql = clean_value(c_match_str)

            # 生成 SQL
            sql = f"""INSERT INTO srzp_service.virtual_job_category_pro (group_code, name, category_id, a2_match, a3_match, b_match, c_match, created_at, updated_at, deleted_at)
VALUES ({group_code_sql}, {name_sql}, 1, {a2_match_sql}, {a3_match_sql}, {b_match_sql}, {c_match_sql}, NOW(), NOW(), NULL);"""

            sql_statements.append(sql)

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('-- 自动生成的SQL语句\n')
        f.write(f'-- 生成时间: {datetime.now()}\n\n')
        f.write('\n\n'.join(sql_statements))

    print(f"✅ 成功生成 {len(sql_statements)} 条SQL语句")
    print(f"📄 输出文件: {output_file}")

    # 打印前3条预览
    print("\n--- 前3条SQL预览 ---")
    for idx, sql in enumerate(sql_statements[:3], 1):
        print(f"{idx}. {sql}\n")


if __name__ == '__main__':
    generate_sql()
