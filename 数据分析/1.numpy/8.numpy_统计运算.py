import numpy as np

a = np.array([[1,2,3],[4,5,6],[7,8,9]])

print("总和:", a.sum())
print("平均值:", a.mean())
print("最大值:", a.max())
print("最小值:", a.min())
print("标准差:", a.std())
print("方差:", a.var())

# 按行/列计算
print("按行求和:", a.sum(axis=1))
print("按列求平均:", a.mean(axis=0))