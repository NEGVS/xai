# pip install hdbscan umap-learn scikit-learn pandas matplotlib001 seaborn plotly -U

import numpy as np
# 在聚类任务中，vectors 几乎总是以 NumPy 数组的形式传入（shape 通常是 (n_samples, n_features)），所以需要 NumPy
import hdbscan


# 导入 HDBSCAN 库（层次密度聚类算法）。

def cluster(vectors):
    """
        对向量进行 HDBSCAN 聚类，返回每个样本的簇标签（列表形式）

        参数:
            vectors: np.ndarray, shape=(n_samples, n_features)

        返回:
            list[int]: 每个样本的簇标签，-1 表示噪声点
        """

    if not isinstance(vectors, np.ndarray):
        vectors = np.array(vectors)

    if vectors.ndim != 2:
        raise ValueError("输入 vectors 必须是二维数组 (n_samples, n_features)")

    clusterer = hdbscan.HDBSCAN(

        min_cluster_size=5,
        metric='euclidean',
        min_samples = None,
        cluster_selection_epsilon=0.0,
        cluster_selection_method='eom'  # 'eom' 或 'leaf'

        # 默认等于 min_cluster_size
        #     precomputed 创建 HDBSCAN 聚类器实例。
        #
        # 主要参数解释：
        #
        # 参数值含义实际影响min_cluster_size5构成一个有效簇（cluster）最少需要的样本点数量设得越小，越容易出现小簇；设得越大，簇越少，小群体会被当成噪声metric'euclidean'距离度量方式，这里使用欧几里得距离（L2 范数）最常见的选择，适用于大多数连续向量空间（word2vec、BERT、sentence-transformers 等）precomputed被注释掉如果传入的是距离矩阵（而非原始向量），则需要设为 True当前代码没有使用，说明输入是原始向量，不是预计算的距离矩阵
        # 其他常用但这里没写的参数（供参考）：
        #
        # min_samples：默认 = min_cluster_size，用于定义核心点，越大越保守（噪声越多）
        # cluster_selection_epsilon：控制簇合并的尺度，0 表示完全自动
        # alpha：距离缩放参数（默认 1.0）
        # leaf_size：加速索引的参数（大数据时有用）
    )

    labels = clusterer.fit_predict(vectors)
    return labels.tolist()
