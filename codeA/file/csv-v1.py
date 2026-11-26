#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取岗位关联表CSV并生成INSERT SQL语句
"""

import csv

# 输入文件路径
# /Users/andy_mac/Documents/CodeSpace/srzp/ai-engineering-center/docs/todo/岗位关联表_-_关联关系表V2.0.csv
csv_file = '/Users/andy_mac/Documents/CodeSpace/srzp/ai-engineering-center/docs/todo/岗位关联表_-_关联关系表V2.0_副本.csv'
# 输出文件路径
output_file = '/Users/andy_mac/Documents/CodeSpace/srzp/ai-engineering-center/docs/todo/generated_sql.sql'


def clean_value(value):
    """清理字段值，去除多余空格和引号"""
    if not value:
        return "''"
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

            # print(len(row))
            if len(row) < 6:
                print(f"跳过行（字段不足）: {row}")
                continue

            # 解析各列
            group_code = row[0].strip()  # 第1列：组ID
            name = row[1].strip()  # 第2列：虚拟大类名
            a2_match = row[2].strip().strip('"')  # 第3列：A2级匹配
            a3_match = row[3].strip().strip('"')  # 第4列：A3级匹配
            b_match = row[4].strip().strip('"')  # 第5列：B级匹配
            c_match = row[5].strip().strip('"') if len(row) > 5 else ''  # 第6列：C级匹配

            # 跳过空行
            if not group_code or not name:
                continue

            # 清理值
            group_code_sql = clean_value(group_code)
            name_sql = clean_value(name)
            a2_match_sql = clean_value(a2_match)
            a3_match_sql = clean_value(a3_match)
            b_match_sql = clean_value(b_match)
            c_match_sql = clean_value(c_match)

            # 生成 SQL
            sql = f"""INSERT INTO srzp_service.virtual_job_category_pro (group_code, name, category_id, a2_match, a3_match, b_match, c_match, created_at, updated_at, deleted_at)
                      VALUES ({group_code_sql}, {name_sql}, 1, {a2_match_sql}, {a3_match_sql}, {b_match_sql}, {c_match_sql}, NOW(), NOW(), NULL);
                    """

            sql_statements.append(sql)

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('-- 自动生成的SQL语句\n')
        f.write('-- 生成时间: ' + str(__import__('datetime').datetime.now()) + '\n\n')
        f.write('\n\n'.join(sql_statements))

    print(f"✅ 成功生成 {len(sql_statements)} 条SQL语句")
    print(f"📄 输出文件: {output_file}")

    # 打印前3条预览
    print("\n--- 前3000条SQL预览 ---")
    count=0
    for sql in sql_statements[:3000]:
        count += 1
        # print(count)
        print(sql)
        print()


if __name__ == '__main__':
    generate_sql()
