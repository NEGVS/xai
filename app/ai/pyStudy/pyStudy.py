import os

from openai import OpenAI

print(os.getenv("OPENAI_API_KEY"))
print(os.getenv("DEEPSEEK_API_KEY"))
print(os.environ["DEEPSEEK_API_KEY"])
print(os.environ)
# define a arr
arr = {}
for st in os.environ:
    if st.endswith("KEY"):
        arr[st] = os.environ[st]
    print(st)
print("-------")
print(arr)
print(arr.keys())
print(arr.values())
for ak in arr:
    print(ak)
str = "assdd"
a = set(str)
count = {}  # 字典
count_s = ["2", "d", "o"]  # 数组
numbers = [1, 5, 8, 9, 33, 2]  # 数组
count_s_empty = []  # 数组
count_k = ("hjkk")  # 元组
for i in a:
    print(i)
    count[i] = str.count(i)
print(count)
print(count.keys())
print(count.values())

# for a, b in arr:
#     print(a)
#     print(b)
# client = OpenAI(api_key=os.environ['DEEPSEEK_API_KEY'],base_url="https://api.deepseek.com")
# 如果是空输出，空，否则输出元素
# 写法1
if not count_s_empty:
    print("count_s_empty 空")
else:
    print("count_s_empty 非空")
    print(count_s_empty)
# 写法1
if not count_s:
    print("count_s 空")
else:
    print("count_s 非空 ")
    print(count_s)
# **逐个输出元素**：
if not count_s:
    print("空")
else:
    print("count_s 非空 逐个输出元素")
    for item in count_s:
        print(item)
    # 倒序遍历
    print("count_s 非空 逐个输出元素，倒序遍历")
    for item in reversed(count_s):
        print(item)
    print("count_s 非空 逐个输出元素，倒序遍历 method 2")

    for item in count_s[::-1]:
        print(item)
# 测试字典
data = {"b": 2, "a": 1, "c": 3}

# 1. 按 key 正序遍历
for k, v in sorted(data.items(), key=lambda x: x[0]):
    print(k, v)

# 2. 按 value 正序遍历
for k, v in sorted(data.items(), key=lambda x: x[1]):
    print(k, v)

arr = [
    {"name": "z", "num": 9},
    {"name": "a", "num": 1},
    {"name": "m", "num": 5},
]
# 根据 num 字段正序
for item in sorted(arr, key=lambda d: d["num"]):
    print(item)

arr = [
    {"name": "z", "num": 9},
    {"name": "a", "num": 1},
    {"name": "m", "num": 5},
]
if not arr:
    print("空")
else:
    for item in sorted(arr, key=lambda d: d["num"]):
        print(item)

# 核心：`sorted` 的 `key` 返回**元组**，元组会按顺序依次比较，实现多字段排序。
## 示例：列表里面是字典，多字段正序
data = [
    {"dept": "A", "age": 22, "score": 80},
    {"dept": "B", "age": 20, "score": 90},
    {"dept": "A", "age": 22, "score": 75},
    {"dept": "A", "age": 20, "score": 88},
]

# 优先级：先 dept 正序 → age 正序 → score 正序
res = sorted(data, key=lambda x: (x["dept"], x["age"], x["score"]))
for row in res:
    print(row)


res = sorted(numbers)
print(res)
# 倒序 sorted(numbers, reverse=True)

print(sorted(numbers, reverse=True))