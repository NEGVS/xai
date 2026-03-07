# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import hdbscan
import umap
import matplotlib.pyplot as plt
import seaborn as sns

# ==================== 修复1：解决中文乱码（Mac 必加）================
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'PingFang SC', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ==================== 1. 模拟真实业务数据（加强区分度）================
np.random.seed(42)
n = 8000

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

# 制造更明显的业务群体（真实场景常见）
data.loc[0:800, ['monetary', 'frequency', 'login_days']] *= 6      # 高价值忠实用户
data.loc[801:1600, 'recency'] = 90                                 # 即将流失
data.loc[1601:2200, ['coupon_usage', 'return_rate']] = 0.92        # 薅羊毛党
data.loc[2201:2800, 'browse_items'] *= 3; data.loc[2201:2800, 'frequency'] = 1  # 只看不买

print("原始数据预览：")
print(data.head())

# ==================== 2. 标准化 + UMAP 降维 ====================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(data)

reducer = umap.UMAP(
    n_neighbors=30,
    min_dist=0.0,
    n_components=2,
    random_state=42
)
X_umap = reducer.fit_transform(X_scaled)

# ==================== 3. HDBSCAN 聚类（参数已优化）================
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=80,       # 降低后簇数量更合理（6~8个）
    min_samples=20,
    cluster_selection_epsilon=0.6,
    prediction_data=True
)

labels = clusterer.fit_predict(X_umap)

data['cluster'] = labels
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
noise_ratio = list(labels).count(-1) / n

print(f"\n🎉 聚类完成！共 {n_clusters} 个有效簇，噪声点占比 {noise_ratio:.1%}")

# ==================== 4. 可视化（保存为图片，避免 PyCharm 崩溃）================
plt.figure(figsize=(12, 8))
scatter = plt.scatter(X_umap[:, 0], X_umap[:, 1], c=labels, cmap='tab20', s=8, alpha=0.8)
plt.colorbar(scatter, label='Cluster ID')
plt.title('HDBSCAN 用户画像分群结果（UMAP 2D 投影）')
plt.xlabel('UMAP1')
plt.ylabel('UMAP2')
plt.grid(True, alpha=0.3)

# 保存图片（关键修复！）
plt.savefig('hdbscan_user_clusters.png', dpi=300, bbox_inches='tight')
print("📸 图片已保存为：hdbscan_user_clusters.png （可在项目文件夹查看）")

plt.close()  # 关闭画布，避免内存占用

# ==================== 5. 各簇特征均值（业务打标签核心）================
print("\n📊 各簇特征均值（直接复制给业务方打标签）：")
cluster_summary = data.groupby('cluster').mean().round(2)
print(cluster_summary)

# 可选：保存到 Excel 方便业务查看
cluster_summary.to_excel('hdbscan_cluster_summary2.xlsx')
print("📁 各簇详细特征已保存为：hdbscan_cluster_summary2.xlsx")