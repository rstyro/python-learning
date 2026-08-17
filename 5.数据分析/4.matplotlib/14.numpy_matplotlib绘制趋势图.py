import numpy as np
import matplotlib.pyplot as plt

# 中文配置
plt.rcParams['font.sans-serif'] = ['SimHei']

# 1~12代表12个月
x = np.arange(1, 13)
# 随机月度销量
sales = np.random.randint(100, 500, 12)

# 绘制带圆点标记的折线，线宽2
plt.plot(x, sales, marker='o', linewidth=2)
plt.title("月度销售趋势")
plt.xlabel("月份")
plt.ylabel("销售额")
plt.grid(True)

plt.show()