import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 全局中文配置
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 1. 生成模拟销售数据 ==========
# 30天日期
dates = pd.date_range('2025-01-01', periods=30, freq='D')
# 随机地区
region = np.random.choice(['华北', '华东', '华南', '西南'], 30)
# 随机销售额
sales = np.random.randint(100, 1000, 30)

# 构建DataFrame
df = pd.DataFrame({
    '日期': dates,
    '地区': region,
    '销售额': sales
})

# ========== 2. 按地区汇总销售额 ==========
region_sum = df.groupby('地区')['销售额'].sum()

# ========== 3. 绘制双图组合报表 ==========
# 1行2列布局
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 左图：地区销售柱状图
region_sum.plot(kind='bar', ax=ax1, color='skyblue')
ax1.set_title('各地区销售额')

# 右图：每日销售趋势
df.groupby('日期')['销售额'].sum().plot(ax=ax2, color='orange')
ax2.set_title('每日销售趋势')

# 自动调整布局
plt.tight_layout()
# 保存报表图片
plt.savefig('销售分析报表.png')
plt.show()

print("✅ 销售报表图片已保存完成！")