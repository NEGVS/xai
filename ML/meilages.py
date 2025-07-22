import matplotlib.pyplot as plt
from datetime import datetime

# 设置seaborn风格
# sns.set_style("whitegrid",{"grid.linestyle":"--","grid.alpha":0.5})
# plt.rcParams['font.family'] ='Arial'
# plt.rcParams['font.size']=13

# 数据
dates = ['2025.3.15', '2025.3.20', '2025.4.7', '2025.6.10', '2025.6.16']
mileages = [47170, 47323, 48392, 51722, 52300]

# 将日期字符串转换为 datetime 对象
dates = [datetime.strptime(date, '%Y.%m.%d') for date in dates]

# 创建折线图
plt.figure(figsize=(10, 6))
plt.plot(dates, mileages, marker='o', linestyle='-', color='b', label='Mileage (KM)')

# 设置图表标题和标签
plt.title('Mileage Over Time', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Mileage (KM)', fontsize=12)

# 设置日期格式化
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.AutoDateLocator())

# 添加网格
plt.grid(True, linestyle='--', alpha=0.7)

# 旋转 x 轴标签以避免重叠
plt.xticks(rotation=45)

# 添加图例
plt.legend()

# 调整布局以防止标签被裁剪
plt.tight_layout()

# 显示图表
plt.show()
