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
