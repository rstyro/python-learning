import numpy as np
import matplotlib.pyplot as plt

# 生成0~10之间100个均匀的点
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

plt.plot(x, y1, color='red', linestyle='-', label='sin')
plt.plot(x, y2, color='blue', linestyle='--', label='cos')

plt.legend()  # 图例
plt.show()