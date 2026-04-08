import numpy as np

a = np.array([[1,2,3],[4,5,6],[7,8,9]])

print("第0行:", a[0])
print("第0行第1列:", a[0,1])
print("所有行第2列:", a[:,2])
print("前2行前2列:\n", a[:2,:2])