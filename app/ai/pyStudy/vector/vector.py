import chromadb
import sys
import numpy
import warnings
import logging
chroma_client = chromadb.Client()

logging.basicConfig(level=logging.DEBUG)
print(numpy.__version__)
print(sys.modules['numpy'].__file__)  # 检查 NumPy 的加载路径
warnings.filterwarnings('ignore', message='The NumPy module was reloaded')
# print(sys.modules.get('numpy'))  # 检查 NumPy 是否已加载

print("NumPy loaded:", numpy.__version__, numpy.__file__)