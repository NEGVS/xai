import sys
import platform
# import torch

print(platform.python_version())  # 打印主要版本号，如 "3.9.7"
print(sys.version)
print(sys.version_info)


# Python 版本（如 '3.9.7'）
python_version = platform.python_version()
print("Python 版本:", python_version)

# Python 实现（如 'CPython', 'PyPy'）
python_implementation = platform.python_implementation()
print("Python 实现:", python_implementation)

# Python 编译器信息（如 'GCC 11.4.0'）
python_compiler = platform.python_compiler()
print("Python 编译器:", python_compiler)
print(sys.executable)  # 查看当前 Python 解释器路径
# Python 安装路径
python_path = sys.executable
print("Python 路径:", python_path)

# 操作系统名称（如 'Windows', 'Linux', 'Darwin'（Mac））
os_name = platform.system()
print("操作系统:", os_name)

# 操作系统版本（如 '10'（Windows 10）, '22.04'（Ubuntu 22.04））
os_version = platform.release()
print("系统版本:", os_version)

# 完整的操作系统信息（如 'Windows-10-10.0.19045-SP0'）
os_info = platform.platform()
print("完整系统信息:", os_info)

# 计算机名称（主机名）
hostname = platform.node()
print("计算机名称:", hostname)

# 处理器架构（如 'AMD64', 'x86_64', 'arm64'）
machine = platform.machine()
print("处理器架构:", machine)

# CPU 信息（仅 Linux/Mac 有效）
processor = platform.processor()
print("CPU 信息:", processor)


# 检查是否有可用 GPU
# print(torch.cuda.is_available())  # True or False