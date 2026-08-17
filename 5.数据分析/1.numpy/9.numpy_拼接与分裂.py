import numpy as np

a = np.array([[1,2],[3,4]])
b = np.array([[5,6],[7,8]])

# 垂直拼接
print("垂直拼接:\n", np.vstack([a,b]))

# 水平拼接
print("水平拼接:\n", np.hstack([a,b]))

# 分裂
c = np.array([1,2,3,4,5,6])
print("分裂成3份:", np.split(c,3))