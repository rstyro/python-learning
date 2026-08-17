import pandas as pd

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六"],
    "成绩": [88, 92, 79, 95],
    "城市": ["北京", "上海", "广州", "深圳"]
}, index=['a', 'b', 'c', 'd'])

# loc：按 标签 取值
print("=== loc 取行标签 b 的行 ===")
print(df.loc['b'])

print("\n=== loc 取多行多列 ===")
print(df.loc[['a', 'c'], ['姓名', '成绩']])

# iloc：按 数字位置 取值
print("\n=== iloc 取第0行第1列 ===")
print(df.iloc[0, 1])

print("\n=== iloc 切片 ===")
print(df.iloc[1:3, 0:2])