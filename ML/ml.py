import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy
print(sys.executable)  # 查看当前 Python 解释器路径
print(pd.__version__)
data = pd.read_csv("/Users/andy_mac/PycharmProjects/xai/static/csv/ml.csv")
print(data)
x = data["YeaysExperience"]
y = data["Salary"]
print(x)
print(y)

plt.scatter(x, y)
plt.show()
