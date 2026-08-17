import numpy as np

a = np.array([[1,2],[3,4]])

# 行列式
print("行列式:", np.linalg.det(a))

# 逆矩阵
print("逆矩阵:\n", np.linalg.inv(a))