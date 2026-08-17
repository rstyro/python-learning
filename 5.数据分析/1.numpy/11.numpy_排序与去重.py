import numpy as np

a = np.array([3,1,4,1,5,9,2,6])

print("数组:", a)
# 排序
print("排序:", np.sort(a))

# 排序后的元素在原数组中的索引位置
print("索引:", np.argsort(a))

# 去重
print("去重:", np.unique(a))