
import app.utils.DateUtils as DateUtils

from sklearn.preprocessing import StandardScaler
import hdbscan
import umap
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

# ===================原因是 Matplotlib 默认字体 DejaVu Sans 不支持中文。
plt.rcParams['font.sans-serif'] = ['PingFang SC']  # Mac系统字体
plt.rcParams['axes.unicode_minus'] = False

# 1-general test high dimensional data: 10 dimensional 5 cluster
print('1-general test high dimensional data')
X, _ = make_blobs(n_samples=1000, n_features=10, centers=5, random_state=42)
# 2- data  standardization
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print('2-data  standardization')

# 3-UMAP dimensionality reduction ，10 dimensionality to 2 dimensionality
umap_model = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
X_umap = umap_model.fit_transform(X_scaled)
print('3-UMAP dimensionality reduction')

# 4-HDBSCAN cluster
cluster_er = hdbscan.HDBSCAN(min_cluster_size=50)
labels = cluster_er.fit_predict(X_scaled)
print('4-HDBSCAN cluster')

# 5-可视化降维+聚类结果
print('5-可视化降维+聚类结果')

plt.figure(figsize=(10,8))
# 用不同颜色表示不同聚类，-1表示噪声点
scatter=plt.scatter(X_umap[:,0],X_umap[:,1],c=labels,cmap='Spectral',s=50,alpha=0.8)

# plt.scatter(
#     embedding[:,0],
#     embedding[:,1],
#     c=labels,
#     cmap='Spectral',
#     s=10
# )
plt.colorbar(scatter,label='aaa')
# 聚类标签（-1=噪声）
plt.title('bbb')
# UMAP降维+HDBSCAN聚类结果
plt.xlabel('cc')
# UMAP维度1
plt.ylabel('dd')
# UMAP维度2
plt.show()

print(DateUtils.DateUtils.get_date())