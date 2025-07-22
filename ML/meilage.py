import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 设置 Seaborn 风格
sns.set_style("whitegrid", {"grid.linestyle": "--", "grid.alpha": 0.5})
# plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 12

# 数据
dates = ['2025.3.15', '2025.3.20', '2025.4.7', '2025.6.10', '2025.6.16']
mileages = [47170, 47323, 48392, 51722, 52300]

# 将日期字符串转换为 datetime 对象
dates = [datetime.strptime(date, '%Y.%m.%d') for date in dates]

# 计算增长速率（公里/天）
growth_rates = []
rate_dates = []
for i in range(1, len(mileages)):
    delta_mileage = mileages[i] - mileages[i - 1]
    delta_days = (dates[i] - dates[i - 1]).days
    growth_rate = delta_mileage / delta_days if delta_days > 0 else 0
    growth_rates.append(growth_rate)
    rate_dates.append(dates[i])  # 使用后一个日期作为速率的代表点
    # print(f"From {dates[i-1].strftime('%Y-%m-%d')} to {dates[i].strftime('%Y-%m-%d')}: {growth_rate:.2f} KM/day")

# 创建图表
fig, ax1 = plt.subplots(figsize=(10, 6), facecolor='#f5f5f5')
ax1.set_facecolor('#fafafa')

# 绘制折线图（公里数）
line, = ax1.plot(dates, mileages, marker='o', linestyle='-', linewidth=2, markersize=8,
                 color='#1f77b4', markeredgecolor='white', markeredgewidth=1.5, label='Mileage (KM)')
ax1.fill_between(dates, mileages, color='#1f77b4', alpha=0.1)

# 添加公里数数据标签
for i, (date, mileage) in enumerate(zip(dates, mileages)):
    ax1.text(date, mileage + 300, f'{mileage}', ha='center', va='bottom', fontsize=10,
             color='#333333', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

# 设置主坐标轴（公里数）
ax1.set_title('Mileage and Growth Rate Over Time', fontsize=16, fontweight='bold', pad=15, color='#333333')
ax1.set_xlabel('Date', fontsize=12, color='#333333')
ax1.set_ylabel('Mileage (KM)', fontsize=12, color='#1f77b4')
ax1.tick_params(axis='y', labelcolor='#1f77b4')
ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
ax1.xaxis.set_major_locator(plt.matplotlib.dates.AutoDateLocator())
plt.xticks(rotation=45, ha='right')

# 创建次坐标轴（增长速率）
ax2 = ax1.twinx()
ax2.bar(rate_dates, growth_rates, width=2, alpha=0.4, color='#ff7f0e', label='Growth Rate (KM/day)')
ax2.set_ylabel('Growth Rate (KM/day)', fontsize=12, color='#ff7f0e')
ax2.tick_params(axis='y', labelcolor='#ff7f0e')

# 添加图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, frameon=True, edgecolor='#cccccc', facecolor='white', fontsize=10)

# 优化边框
for spine in ax1.spines.values():
    spine.set_edgecolor('#cccccc')
    spine.set_linewidth(0.8)
for spine in ax2.spines.values():
    spine.set_edgecolor('#cccccc')
    spine.set_linewidth(0.8)

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()