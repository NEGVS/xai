# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from app.utils import DateUtils
from app.ai.pyStudy import FileUtils
import hdbscan
import umap
import matplotlib.pyplot as plt

# ==================== 1. 解决中文乱码（Mac PyCharm）================
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'PingFang SC', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ==================== 2. 模拟真实业务数据（加强区分度）================
np.random.seed(42)
n = 8000
print('1-模拟真实业务数据')
data = pd.DataFrame({
    'recency': np.random.exponential(30, n).astype(int),
    'frequency': np.random.poisson(5, n),
    'monetary': np.random.lognormal(6, 1.2, n).astype(int),
    'login_days': np.random.poisson(12, n),
    'browse_items': np.random.poisson(45, n),
    'add_cart_rate': np.random.beta(2, 5, n),
    'coupon_usage': np.random.beta(3, 8, n),
    'return_rate': np.random.beta(1, 10, n),
    'stay_minutes': np.random.gamma(15, 2, n),
    'search_diversity': np.random.uniform(0.1, 0.9, n)
})

# 制造更明显的 7 个业务群体（真实项目常用）
print('1-制造更明显的 7 个业务群体（真实项目常用）')
data.loc[0:900, ['monetary', 'frequency', 'login_days']] *= 7  # 高价值忠实
data.loc[901:1700, 'recency'] = 95  # 即将流失
data.loc[1701:2400, ['coupon_usage', 'return_rate']] = 0.93  # 薅羊毛党
data.loc[2401:3100, 'browse_items'] *= 4;
data.loc[2401:3100, 'frequency'] = 1  # 只看不买
data.loc[3101:3800, 'stay_minutes'] = 5  # 低活跃
data.loc[3801:4500, 'search_diversity'] = 0.95  # 搜索狂魔

print('原始数据预览：')
print(data.head())

# ==================== 3. 标准化 + UMAP ====================
print('3. 标准化 + UMAP ====================')

scaler = StandardScaler()
X_scaled = scaler.fit_transform(data)

reducer = umap.UMAP(n_neighbors=30, min_dist=0.0, n_components=2, random_state=42)
X_umap = reducer.fit_transform(X_scaled)

# ==================== 4. HDBSCAN（参数优化后稳定 6~8 个簇）================
print('4. HDBSCAN（参数优化后稳定 6~8 个簇）================')
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=65,  # 调小一点，簇数量更合理
    min_samples=15,
    cluster_selection_epsilon=0.5,
    prediction_data=True
)

labels = clusterer.fit_predict(X_umap)
data['cluster'] = labels

n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
print(f"\n 聚类完成！共 {n_clusters} 个有效簇，噪声点占比 {list(labels).count(-1) / n:.1%}")

# ==================== 5. 可视化 + 保存图片================
print('5. 可视化 + 保存图片================')

plt.figure(figsize=(12, 8))
scatter = plt.scatter(X_umap[:, 0], X_umap[:, 1], c=labels, cmap='tab20', s=8, alpha=0.8)
plt.colorbar(scatter, label='Cluster ID')
plt.title('HDBSCAN 用户画像分群结果（UMAP 2D 投影）')
plt.xlabel('UMAP1')
plt.ylabel('UMAP2')
plt.grid(True, alpha=0.8)
plt.show()
# 生成时间戳
timestamp = DateUtils.get_timestamp()
FileUtils.create_folder('', 'img')
plt.savefig('./img/hdbscan_user_clusters' + str(timestamp) + '.png', dpi=300, bbox_inches='tight')
print("图片已保存：hdbscan_user_clusters" + str(timestamp) + ".png")

plt.close()

# ==================== 6. 各簇特征均值 + 自动保存（兼容无 openpyxl）================
print("\n各簇特征均值：")
cluster_summary = data.groupby('cluster').mean().round(2)
print(cluster_summary)

# 自动兼容保存
try:
    FileUtils.create_folder('', 'excel')
    excel_path = './excel/hdbscan_cluster_summary' + str(timestamp) + '.xlsx'
    cluster_summary.to_excel(excel_path)
    print("已保存为 Excel：", excel_path)
except ImportError:
    FileUtils.create_folder('', 'csv')
    csv_path = './csv/hdbscan_cluster_summary' + str(timestamp) + '.csv'
    cluster_summary.to_csv(csv_path, encoding='utf-8-sig')
    print("未安装 openpyxl，已自动保存为 CSV：", csv_path, "（推荐装 openpyxl）")
except Exception as e:
    print(f"保存失败：{e}")
