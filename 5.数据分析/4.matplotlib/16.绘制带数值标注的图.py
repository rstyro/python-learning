import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

x = np.arange(1, 6)
y = [20, 50, 30, 80, 60]

plt.plot(x, y, marker='o')

# 循环给每个点加数值标注
for i, j in zip(x, y):
    plt.text(i, j + 2, str(j))  # j+2是为了让文字往上偏移一点

plt.title("带数值标注的折线图")
plt.show()