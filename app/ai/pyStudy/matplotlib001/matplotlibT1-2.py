import matplotlib.pyplot as plt
import numpy as np

x = [1, 2, 3, 4]
y = [10, 200, 25, 30]
y2 = [13, 20, 15, 50]

plt.plot(x, y,label="Series A")
plt.plot(x, y2,label="Series B")

plt.title("Multiple Line Chart")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")

plt.legend()
# 举个直观例子：如果你的折线图里同时画了「销量」和「利润」两条线，plt.legend() 会在图表上标注哪条线是销量、哪条是利润，避免混淆。
# 先给绘图函数（如 plot()）加 label 参数，再调用 plt.legend() 即可自动生成图例

plt.show()
