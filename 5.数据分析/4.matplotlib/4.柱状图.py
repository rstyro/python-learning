import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

name = ['A','B','C','D']
score = [88,92,70,95]

# 柱状图
plt.bar(name, score, color='orange')

# 水平柱状图
# plt.barh(name, score)
plt.title("柱状图")
plt.show()


