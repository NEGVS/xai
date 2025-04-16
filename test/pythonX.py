import time
import os
import sys
from pathlib import Path

# 1-字符串拼接------------
print('1-字符串拼接--------')
timestamp = str(int(time.time()))

path = 'abc' + timestamp
print(path)
# 错误做法（慢）
s = ""
for i in range(1000):
    s += str(i)
print(s)
# 正确做法（快）
parts = []
for i in range(1000):
    parts.append(str(i))
s = "".join(parts)
print(s)

# 因为字符串不可变，每次 += 会创建新对象。改用列表暂存后 join()：--少量拼接：优先用 f-string 或 +
# 大量拼接：用 join() + 列表推导
# 2- 目录-------------------
print('2- 目录-------------------')
current_dir = os.getcwd()
print(current_dir)
# 方法1：使用 __file__（推荐）
script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)
path_final = Path(script_dir) / "ss" / "as.png"
path_final2 = Path("script_dir") / "ss" / "as.png"
print(path_final)
print(path_final2)
current_dir = os.getcwd()

# 示例：加入时间戳
timestamp = int(time.time())
filename = f"abc_{timestamp}_kkk.png"

path_final = Path(current_dir) / filename

print(path_final)

# import os

"""
    获取文件路径的目录，检查目录是否存在，如果不存在则创建。

    Args:
        file_path (str): 文件的完整路径

    Returns:
        str: 目录路径
    """

def ensure_directory(file_path):
    try:
        # 获取目录路径
        directory = os.path.dirname(file_path)

        # 检查目录是否为空
        if not directory:
            raise ValueError("Invalid file path: No directory found")

        # 检查目录是否存在
        if not os.path.exists(directory):
            print(f"Directory {directory} does not exist, creating...")
            # 创建目录（包括父目录）
            os.makedirs(directory, exist_ok=True)
            print(f"Directory {directory} created successfully")
        else:
            print(f"Directory {directory} already exists")

        return directory

    except Exception as e:
        print(f"Error processing directory: {e}")
        raise


def main():
    # 示例文件路径（替换为你的路径）
    file_path = "/Users/andy_mac/PycharmProjects/xai/google/image/gemini-image_1744789391.png"

    try:
        # 调用函数确保目录存在
        directory = ensure_directory(file_path)
        print(f"Working directory: {directory}")

    except Exception as e:
        print(f"Failed to ensure directory: {e}")


if __name__ == "__main__":
    main()
