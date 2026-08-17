import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 或 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 生成1000个正态分布数据（均值50，标准差10）
data = np.random.normal(50, 10, 1000)

# 绘制直方图，分20组
plt.hist(data, bins=20)
plt.title("数据分布")
plt.show()