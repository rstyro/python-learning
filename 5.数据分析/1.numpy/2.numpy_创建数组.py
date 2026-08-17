import numpy as np

# 从列表创建数组
a1 = np.array([1, 2, 3, 4, 5])
print("一维数组:", a1)

# 二维数组（矩阵）
a2 = np.array([[1,2],[3,4],[5,6]])
print("二维数组:\n", a2)

# 快速创建
print("全0数组:", np.zeros(5))
print("全1数组:", np.ones((2,3)))
print("1~10:", np.arange(1,11))
print("0~1均分5份:", np.linspace(0,1,5))