# pip install hdbscan umap-learn scikit-learn pandas matplotlib001 seaborn plotly -U

import pandas as pd
import numpy as np
from sklearn.datasets import make_moons
import matplotlib.pyplot as plt
import hdbscan
# ===================== 关键配置：解决中文乱码 =====================
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 设置默认字体为黑体（Windows）
# 如果是Mac系统，替换为：['Arial Unicode MS'] ，
# 设置默认字体为黑体（Windows）['SimHei']
# 如果是Linux系统，替换为：['WenQuanYi Micro Hei']
# 如果是Linux系统，替换为：['WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题
# 双月亮+噪声
X, _ = make_moons(n_samples=500, noise=0.5, random_state=42)
# hdbscan 聚类，几乎零参数

clusterer = hdbscan.HDBSCAN(
    min_cluster_size=15,  # 最小簇大小 最重要的参数
    min_samples=5,  # 核心点定义，越大越保守
    cluster_selection_epsilon=0.0,  # 0=完全层次自主选择
    prediction_data=True
)
labels = clusterer.fit_predict(X)
# 可视化
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', s=10)
plt.title('HDBSCAN聚类结果（自动识别噪声）')
plt.show()
print('簇数量：', len(set(labels)) - (1 if -1 in labels else 0))
print('噪声点数量：', list(labels).count(-1))
