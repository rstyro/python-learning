import numpy as np

# 0~1 随机数
print(np.random.rand(5))

# 标准正态分布
print(np.random.randn(5))

# 整数随机
print(np.random.randint(0,10,size=(2,3)))

# 固定随机种子（结果不变）
np.random.seed(10)
print(np.random.rand(2))