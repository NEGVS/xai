# pip install hdbscan umap-learn scikit-learn pandas matplotlib seaborn plotly -U

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import hdbscan
import umap
import matplotlib.pyplot as plt
import seaborn as sns

# ==================== 1. 模拟真实业务数据（8000 用户）================
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

# 真实业务里会加上一些极端用户（高价值/流失/薅羊毛）
data.loc[0:300, 'monetary'] *= 8      # 高价值用户
data.loc[301:600, 'recency'] = 120    # 即将流失
data.loc[601:900, 'coupon_usage'] = 0.95  # 薅羊毛党

print("原始数据预览：")
print(data.head())

# ==================== 2. 标准化 + UMAP 降维（推荐！）================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(data)

# UMAP 降到 2D（便于可视化，真实生产可直接用 10 维聚类）
reducer = umap.UMAP(n_neighbors=30, min_dist=0.0, n_components=2, random_state=42)
X_umap = reducer.fit_transform(X_scaled)

# ==================== 3. HDBSCAN 聚类（几乎零参数）================
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=120,      # 最小一个群 120 人（根据业务调整）
    min_samples=30,            # 核心点要求，越小越敏感
    cluster_selection_epsilon=0.5,  # 可微调
    prediction_data=True
)

labels = clusterer.fit_predict(X_umap)

data['cluster'] = labels
print(f"\n聚类结果：共 {len(set(labels)) - (1 if -1 in labels else 0)} 个有效簇，噪声点占比 {list(labels).count(-1)/n:.1%}")

# ==================== 4. 可视化（生产必看）================
plt.figure(figsize=(12, 8))
scatter = plt.scatter(X_umap[:, 0], X_umap[:, 1], c=labels, cmap='tab20', s=8, alpha=0.8)
plt.colorbar(scatter, label='Cluster')
plt.title('HDBSCAN 用户画像分群结果（UMAP 2D 投影）')
plt.xlabel('UMAP1'); plt.ylabel('UMAP2')
plt.show()

# 各簇特征均值（业务解读核心！）
print("\n各簇特征均值（业务打标签依据）：")
print(data.groupby('cluster').mean().round(2))