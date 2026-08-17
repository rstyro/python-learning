import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 或 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

plt.plot([1, 2, 3], [4, 5, 1])
plt.title("测试图")

# 保存图片，dpi=150，bbox_inches='tight'去掉白边
plt.savefig("test.png", dpi=150, bbox_inches='tight')
print("图片已保存")

plt.show()