import numpy as np

a = np.array([1,2,np.nan,4,np.inf])

print("是否NaN:", np.isnan(a))
print("是否无穷:", np.isinf(a))

# 替换NaN
a[np.isnan(a)] = 0
print("替换后:", a)