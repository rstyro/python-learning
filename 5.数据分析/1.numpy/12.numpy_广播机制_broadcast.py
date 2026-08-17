import numpy as np

a = np.array([[1,2,3],[4,5,6]])
b = np.array([10,20,30])

# 自动对齐广播
print(a + b)

print(a * 100)