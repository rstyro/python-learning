import numpy as np

a = np.array([[1,2],[3,4]])

# 保存
np.save("arr.npy", a)

# 读取
b = np.load("arr.npy")
print(b)

# 保存为txt
np.savetxt("arr.txt", a, fmt="%.2f")