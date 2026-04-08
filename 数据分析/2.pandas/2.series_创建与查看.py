import pandas as pd

# Series = 一列数据
s = pd.Series([90, 85, 92, 78, 100])

print("===== Series 内容 =====")
print(s)

print("\n===== 取值 =====")
print("第0个值：", s[0])
print("最大值：", s.max())
print("平均值：", s.mean())