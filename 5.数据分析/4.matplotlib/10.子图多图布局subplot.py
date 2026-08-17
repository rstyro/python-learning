import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

# 2行2列布局，第1个子图
plt.subplot(2, 2, 1)
plt.plot(x, np.sin(x))

# 第2个子图
plt.subplot(2, 2, 2)
plt.plot(x, np.cos(x))

# 第3个子图
plt.subplot(2, 2, 3)
plt.bar([1, 2], [3, 4])

plt.show()