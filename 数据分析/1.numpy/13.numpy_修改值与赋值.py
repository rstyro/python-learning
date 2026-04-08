import numpy as np

a = np.array([[1,2],[3,4]])

a[0,1] = 99
print(a)

a[a < 3] = 0
print(a)