import numpy as np
import matplotlib.pyplot as plt

# 生成3组正态分布数据
data = [np.random.normal(50,10,100) for _ in range(3)]

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 或 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False

plt.boxplot(data, tick_labels=['一班','二班','三班'])
plt.show()