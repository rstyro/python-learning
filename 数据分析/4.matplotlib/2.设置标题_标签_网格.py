import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 或 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

x = np.arange(1, 11)
y = 2*x + 5

plt.plot(x, y)

plt.title("简单折线图")
plt.xlabel("X轴")
plt.ylabel("Y轴")
plt.grid(True)  # 网格

plt.show()