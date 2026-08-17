import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 或 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

df = pd.DataFrame({
    '城市': ['北京', '上海', '广州'],
    '销量': [200, 300, 150]
})

# 柱状图
df.plot(kind='bar', x='城市', y='销量')
# 饼图
df.plot(kind='pie', y='销量', labels=df['城市'])

plt.show()