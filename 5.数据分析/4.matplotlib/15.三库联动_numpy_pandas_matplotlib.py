import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

# 构造DataFrame
df = pd.DataFrame({
    '类别': ['数码', '服饰', '食品', '图书'],
    '利润': np.random.randint(100, 500, 4)
})

# 绘制柱状图，自定义颜色
plt.bar(df['类别'], df['利润'], color=['r', 'g', 'b', 'orange'])
plt.title("各品类利润")

plt.show()