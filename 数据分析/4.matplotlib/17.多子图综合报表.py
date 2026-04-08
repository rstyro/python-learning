import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

# 创建画布，设置总大小
fig = plt.figure(figsize=(10, 6))

# 2行2列第1个图
ax1 = fig.add_subplot(2, 2, 1)
ax1.plot(np.random.rand(10))

# 第2个图
ax2 = fig.add_subplot(2, 2, 2)
ax2.bar(['A', 'B'], [3, 5])

# 第3个图
ax3 = fig.add_subplot(2, 2, 3)
ax3.pie([1, 2, 3])

# 第4个图
ax4 = fig.add_subplot(2, 2, 4)
ax4.scatter(np.random.rand(10), np.random.rand(10))

# 自动调整子图间距
plt.tight_layout()
plt.show()