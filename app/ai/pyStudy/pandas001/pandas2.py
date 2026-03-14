# =========
import pandas as pd
import numpy as np

from app.ai.pyStudy.file.fileUtils import FileUtils
import matplotlib.pyplot as plt

# 关键配置：显示所有列、所有行，取消列宽限制
pd.set_option('display.max_columns', None)  # 显示所有列（取消列数限制）
pd.set_option('display.max_rows', None)  # 显示所有行（取消行数限制）
pd.set_option('display.width', None)  # 取消输出宽度限制（避免列换行）
pd.set_option('display.max_colwidth', None)  # 取消列内容长度限制

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 解决中文显示问题
plt.rcParams["axes.unicode_minus"] = False
# ==========

# 1. 从字典创建（最常用）
data = {
    "name": ['san', 'si', 'five', 'six'],
    'age': [22, 25, 12, 23],
    "城市": ["北京", "上海", "广州", "深圳"],
    "薪资": [8000, 12000, 15000, 20000]
}

df = pd.DataFrame(data)

FileUtils.create_folder('', 'csv')
df.to_csv('./csv/kkk2.csv', index=False, header=False, encoding='utf-8')
print(df)
print('====获取其中一列========df["name"]')
print(df["name"])
# 4.3 按条件筛选（薪资>10000的行）
print("\n薪资>12000的员工：")
df_high_salary = df[df["薪资"] > 12000]
print(df_high_salary)
# 4.4 多条件筛选（年龄>25 且 城市=深圳）
print("\n年龄>20且城市=深圳的员工：")
df_filter = df[(df["age"] >= 20) & (df["城市"] == "深圳")]  # &表示且，|表示或
print(df_filter)
print('============df.head')
print(df.head())
print('============df.describe')
print(df.describe())
print('=================================df_clean')
# 5：数据清洗（缺失值 / 重复值）
# 先构造带缺失值/重复值的DataFrame
df_clean = df.copy()
df_clean.loc[3, "薪资"] = np.nan  # 给赵六的薪资设为缺失值
df_clean = pd.concat([df_clean, df_clean.iloc[0:1]], ignore_index=True)  # 新增重复行（张三）
print("\n示例5 - 数据清洗：")
print("原始带问题的数据：")
print(df_clean)

# 5.1 检测缺失值
print("\n缺失值检测（True表示缺失）：")
print(df_clean.isnull())
# 5.2 填充缺失值（数值列用均值填充）
df_clean["薪资"] = df_clean["薪资"].fillna(df_clean["薪资"].mean())
# 5.3 删除重复行
df_clean = df_clean.drop_duplicates()

print("\n清洗后的数据：")
print(df_clean)
print("\n示例6 - 数据排序：")
# 6.1 按「薪资」降序排序
df_sorted = df.sort_values(by="薪资", ascending=False)
print("按薪资降序：")
print(df_sorted)

# 6.2 多列排序（先按年龄升序，再按薪资降序）
df_sorted2 = df.sort_values(by=["age", "薪资"], ascending=[True, False])
print("\n按年龄升序、薪资降序：")
print(df_sorted2)
# 先构造带「部门」列的DataFrame
df_group = df.copy()
df_group["部门"] = ["技术", "销售", "销售", "技术"]

print("\n示例7 - 分组聚合：")
# 按「部门」分组，计算薪资的均值和总和
group_result = df_group.groupby("部门")["薪资"].agg(["mean", "sum"])
group_result.columns = ["部门平均薪资", "部门总薪资"]  # 重命名列
print("各部门薪资统计：")
print(group_result)

print("\n示例10 - 数据可视化（生成图表）：")
plt.figure(figsize=(8, 4))
# bar/line/hist
df.plot(kind='line', x='age', y='薪资', marker='o', color=
'red')
plt.title('age vs salary')
plt.xlabel('age')
plt.ylabel('salary')
plt.tight_layout()
plt.show()
# =================||||||||||||||=======
# 2.1 读取CSV文件（实际工作中最常用）
df2 = pd.read_csv("kkk.csv", encoding="utf-8")  # 本地文件
print('df2----1--start')

print(df2)
print('df2----end')
# 2.2 读取Excel文件（需安装openpyxl：pip install openpyxl）
df3 = pd.read_excel(
    "/Users/andy_mac/PycharmProjects/xai/app/ai/DeepL/hdbScan/excel/hdbscan_cluster_summary1773045185.xlsx",
    sheet_name="Sheet1")
print('df3----1--start')
print(df3)
print('df3----end')
