import matplotlib.pyplot as plt

labels = ['电子产品','服装','食品','图书']
values = [350, 200, 150, 100]
colors = ['#FFA500', '#00FF00', 'red', '#FF00FF']
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']

# 绘制饼图，autopct显示百分比
plt.pie(values, labels=labels, autopct='%.1f%%', colors=colors)
plt.title("品类销售占比")
plt.show()