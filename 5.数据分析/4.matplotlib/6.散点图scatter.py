import numpy as np
import matplotlib.pyplot as plt

# 随机生成50个0~1之间的点
x = np.random.rand(50)
y = np.random.rand(50)

# 绘制散点图，绿色，点大小30
plt.scatter(x, y, color='green', s=30)
plt.show()