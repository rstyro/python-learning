import numpy as np

# 对应元素相乘
a = np.array([[1,2],[3,4]])
b = np.array([[1,0],[0,1]])

print("对应相乘:\n", a * b)

# 矩阵点积（真正的矩阵乘法）,对应元素相乘后再相加
print("矩阵点积:\n", np.dot(a,b))