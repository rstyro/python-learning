import numpy as np

a = np.array([1,2,3,4,5,6,7,8,9])

# 大于5的元素
print(a[a > 5])

# 偶数
print(a[a % 2 == 0])

# 多条件
print(a[(a>3) & (a<8)])