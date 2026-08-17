import numpy as np

a = np.array([1,2,3])
b = a       # 视图
c = a.copy()# 真正复制

a[0] = 99
print("a:", a)
print("b:", b)  # 变了
print("c:", c)  # 不变