# 安装
# pip install matplotlib

import numpy as np
import matplotlib.pyplot as plt

# 最简单折线图
x = np.array([1,2,3,4,5])
y = x**2

print(x,y)
plt.plot(x, y)
plt.show()
