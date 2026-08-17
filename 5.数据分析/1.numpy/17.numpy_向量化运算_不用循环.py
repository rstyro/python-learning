import numpy as np

# 对每个元素做复杂运算
def f(x):
    return x**2 + 2*x + 1

a = np.array([1,2,3,4])
print(f(a))