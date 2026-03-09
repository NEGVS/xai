这里为你整理了 **10个高频实用的 pandas 示例**，覆盖数据读取、清洗、筛选、计算、可视化等核心场景，代码可直接复制运行（建议先安装 `pandas` 和 `matplotlib`：`pip install pandas matplotlib`）。

### 示例1：创建DataFrame（基础）
```python
import pandas as pd
import numpy as np

# 1. 从字典创建（最常用）
data = {
    "姓名": ["张三", "李四", "王五", "赵六"],
    "年龄": [22, 25, 28, 30],
    "城市": ["北京", "上海", "广州", "深圳"],
    "薪资": [8000, 12000, 15000, 20000]
}
df = pd.DataFrame(data)
print("示例1 - 创建DataFrame：")
print(df)
```
**核心说明**：字典的`key`是列名，`value`是列数据（列表/数组），是创建DataFrame最基础的方式。

显示所有行列
# 关键配置：显示所有列、所有行，取消列宽限制
pd.set_option('display.max_columns', None)  # 显示所有列（取消列数限制）
pd.set_option('display.max_rows', None)     # 显示所有行（取消行数限制）
pd.set_option('display.width', None)        # 取消输出宽度限制（避免列换行）
pd.set_option('display.max_colwidth', None) # 取消列内容长度限制


### 示例2：读取/保存数据（文件操作） ok
```python
# 2.1 读取CSV文件（实际工作中最常用）
# df = pd.read_csv("data.csv", encoding="utf-8")  # 本地文件
# 2.2 读取Excel文件（需安装openpyxl：pip install openpyxl）
# df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# 2.3 保存为CSV（演示用，基于示例1的df）
df.to_csv("员工信息.csv", index=False, encoding="utf-8")  # index=False不保存行索引
print("\n示例2 - 保存文件完成，生成「员工信息.csv」")
```
**核心说明**：`read_csv/read_excel`是读取外部数据的核心函数，`to_csv/to_excel`用于保存，`encoding="utf-8"`避免中文乱码。

### 示例3：数据查看与基础信息 ok
```python
print("\n示例3 - 数据基础信息：")
print("前2行数据：")
print(df.head(2))  # 查看前n行（默认5行）
print("\n数据维度（行×列）：", df.shape)  # 输出(4,4)
print("\n数据类型：")
print(df.dtypes)  # 查看每列的数据类型
print("\n数据描述性统计（数值列）：")
print(df.describe())  # 仅对数值列（年龄、薪资）计算均值、标准差等 ok
```
**核心说明**：`head()`快速预览数据，`shape`看数据规模，`dtypes`检查类型（避免后续计算出错），`describe()`快速分析数值列分布。

### 示例4：数据筛选（按条件/列）
```python
print("\n示例4 - 数据筛选：")
# 4.1 筛选单列
print("仅查看「姓名」列：")
print(df["姓名"])

# 4.2 筛选多列
print("\n查看「姓名+薪资」列：")
print(df[["姓名", "薪资"]])

# 4.3 按条件筛选（薪资>10000的行）
print("\n薪资>10000的员工：")
df_high_salary = df[df["薪资"] > 10000]
print(df_high_salary)

# 4.4 多条件筛选（年龄>25 且 城市=深圳）
print("\n年龄>25且城市=深圳的员工：")
df_filter = df[(df["年龄"] > 25) & (df["城市"] == "深圳")]  # &表示且，|表示或
print(df_filter)
```
**核心说明**：方括号+条件是筛选的核心，多条件需用`()`包裹，`&/|`代替`and/or`。

### 示例5：数据清洗（缺失值/重复值）
```python
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
```
**核心说明**：`isnull()`检测缺失值，`fillna()`填充（均值/中位数/固定值），`drop_duplicates()`删除重复行，是数据清洗的核心步骤。

### 示例6：数据排序
```python
print("\n示例6 - 数据排序：")
# 6.1 按「薪资」降序排序
df_sorted = df.sort_values(by="薪资", ascending=False)
print("按薪资降序：")
print(df_sorted)

# 6.2 多列排序（先按年龄升序，再按薪资降序）
df_sorted2 = df.sort_values(by=["年龄", "薪资"], ascending=[True, False])
print("\n按年龄升序、薪资降序：")
print(df_sorted2)
```
**核心说明**：`sort_values()`是排序核心，`by`指定排序列，`ascending=False`表示降序。

### 示例7：数据分组与聚合（groupby）
```python
# 先构造带「部门」列的DataFrame
df_group = df.copy()
df_group["部门"] = ["技术", "销售", "销售", "技术"]

print("\n示例7 - 分组聚合：")
# 按「部门」分组，计算薪资的均值和总和
group_result = df_group.groupby("部门")["薪资"].agg(["mean", "sum"])
group_result.columns = ["部门平均薪资", "部门总薪资"]  # 重命名列
print("各部门薪资统计：")
print(group_result)
```
**核心说明**：`groupby()`是数据分析核心，先分组、再对指定列做聚合（`agg`支持均值、求和、计数等）。

### 示例8：新增/修改列
```python
print("\n示例8 - 新增/修改列：")
# 8.1 新增列（薪资税后，假设税率10%）
df["税后薪资"] = df["薪资"] * 0.9
# 8.2 修改列（年龄+1，模拟次年年龄）
df["年龄"] = df["年龄"] + 1
# 8.3 条件新增列（薪资等级：高/中/低）
df["薪资等级"] = pd.cut(
    df["薪资"],
    bins=[0, 10000, 15000, float("inf")],
    labels=["低", "中", "高"]
)
print("新增/修改列后的数据：")
print(df)
```
**核心说明**：直接赋值即可新增/修改列，`pd.cut()`可按区间给数值列打标签（如薪资等级）。

### 示例9：数据合并（merge/concat）
```python
# 构造第二个DataFrame（员工绩效）
df_perf = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六"],
    "绩效评分": [85, 90, 78, 95]
})

print("\n示例9 - 数据合并：")
# 9.1 按「姓名」合并（类似SQL的JOIN）
df_merge = pd.merge(df, df_perf, on="姓名", how="inner")  # inner表示内连接
print("合并员工信息+绩效：")
print(df_merge)

# 9.2 行拼接（新增员工）
new_employee = pd.DataFrame({
    "姓名": ["钱七"],
    "年龄": [24],
    "城市": ["杭州"],
    "薪资": [9000],
    "税后薪资": [8100],
    "薪资等级": ["低"]
})
df_concat = pd.concat([df, new_employee], ignore_index=True)
print("\n新增员工后的数据：")
print(df_concat)
```
**核心说明**：`merge()`用于按关键字合并（多表关联），`concat()`用于行/列拼接。

### 示例10：数据可视化（快速绘图）
```python
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 解决中文显示问题
plt.rcParams["axes.unicode_minus"] = False

print("\n示例10 - 数据可视化（生成图表）：")
# 10.1 柱状图：员工薪资对比
plt.figure(figsize=(8, 4))
df.plot(kind="bar", x="姓名", y="薪资", color="skyblue")
plt.title("员工薪资对比")
plt.xlabel("姓名")
plt.ylabel("薪资（元）")
plt.xticks(rotation=0)  # x轴标签不旋转
plt.tight_layout()  # 调整布局
plt.show()

# 10.2 折线图：年龄vs薪资
plt.figure(figsize=(8, 4))
df.plot(kind="line", x="年龄", y="薪资", marker="o", color="red")
plt.title("年龄 vs 薪资")
plt.xlabel("年龄")
plt.ylabel("薪资（元）")
plt.tight_layout()
plt.show()
```
**核心说明**：pandas内置绘图功能（基于matplotlib），`kind`指定图表类型（bar/line/hist等），先设置字体避免中文乱码。

---

### 总结
1. pandas核心是**DataFrame**（表格型数据结构），基础操作围绕「创建→读取→查看→筛选→清洗→计算→可视化」展开；
2. 高频函数：`read_csv()`/`head()`/`loc[]`/`groupby()`/`merge()`/`sort_values()`，覆盖80%日常场景；
3. 数据清洗（缺失值/重复值）和分组聚合（groupby）是数据分析的核心步骤，需重点掌握。

如果需要针对某类场景（如时间序列处理、透视表）的示例，可以告诉我，我再补充。
