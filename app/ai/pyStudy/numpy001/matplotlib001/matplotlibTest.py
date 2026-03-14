import numpy as np
# import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use('Agg')  # 或 'TkAgg'，根据系统支持
# 示例：绘制资金流动图
months = np.arange(1, 37)  # 3年36个月
income = np.full(36, 13500)  # 每月收入1.35万
tuition = np.full(36, 8333)  # 每月学费8333元
remaining = income - tuition

plt.plot(months, income, label='月收入', color='blue')
plt.plot(months, tuition, label='学费支出', color='red')
plt.plot(months, remaining, label='剩余资金', color='green')
plt.xlabel('月份')
plt.ylabel('金额（元）')
plt.title('每月资金流动')
plt.legend()
plt.grid(True)
plt.show()