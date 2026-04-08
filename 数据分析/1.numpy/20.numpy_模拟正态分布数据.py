import numpy as np

"""
np.random.normal 用于从正态分布（高斯分布）中随机抽样。它的三个主要参数含义如下：
    loc：分布的均值（μ）。决定分布的中心位置，示例中 loc=50 表示数据集中在 50 附近。
    scale：分布的标准差（σ）。衡量数据的离散程度，scale=10 意味着大约 68% 的数据落在 [40, 60]（μ±σ）区间内。
    size：输出的样本数量。可以是整数（如 1000）或形状元组，这里 size=1000 生成 1000 个随机数。
"""
# 模拟1000个正态分布数据
data = np.random.normal(loc=50, scale=10, size=1000)

# 分析
print("平均值:", data.mean())
print("标准差:", data.std())
print("最大值:", data.max())
print("最小值:", data.min())

# 统计大于60的数量
cnt = (data > 60).sum()
print("大于60的数量:", cnt)
