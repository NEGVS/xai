import numpy as np

# create arr
arr = np.array([1, 2, 3, 4, 5])

# print arr
print(arr)

# count sum arr
sum_arr = np.sum(arr)
print('sum of arr\n', sum_arr)

# create 2 X 2 matrix
matrix = np.array([[1, 2], [3, 4]])
# print
print(matrix)
# matrix transfer
transpose_matrix = np.transpose(matrix)

print(transpose_matrix)
# 千万别把 @ 和 * 混淆！* 是元素级乘法（要求两个矩阵维度完全相同），@ 是矩阵乘法（要求列数 = 行数）
matrix_A = np.array([[1, 2], [3, 4]])
matrix_B = np.array([[5, 6], [7, 8]])
# matrix_C = np.matrix_transpose(matrix_A)
matrix_C = matrix_A @ matrix_B
print(matrix_C)

x = np.linspace(0,10,100)
print(x)