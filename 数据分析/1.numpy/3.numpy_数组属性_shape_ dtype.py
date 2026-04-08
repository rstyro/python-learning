import numpy as np

a = np.array([[1,2,3],[4,5,6]])

print("数组形状:", a.shape)
print("维度数:", a.ndim)
print("元素总数:", a.size)
print("数据类型:", a.dtype)

# 修改形状
b = a.reshape(3,2)
print("修改形状后:\n", b)