import os
from datetime import datetime

# 获取环境变量值
print(os.environ["DASHSCOPE_API_KEY"])
print(os.environ["OPENAI_BASE_URL"])

print(os.getenv("DASHSCOPE_API_KEY"))
# 输出当前时间
print(os.getenv("OPENAI_API_KEY"))

print(os.environ["OPENAI_API_KEY_A"])

current_time = datetime.now()
# 格式化：年-月-日 时:分:秒
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
print(f"当前系统时间: {formatted_time}")
