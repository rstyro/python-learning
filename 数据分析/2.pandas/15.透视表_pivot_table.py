import pandas as pd

df = pd.DataFrame({
    "班级": ["一班", "一班", "二班", "二班", "一班"],
    "性别": ["男", "女", "男", "女", "男"],
    "成绩": [88, 92, 79, 95, 85]
})

# 制作透视表：行=班级，列=性别，值=平均成绩
pivot = pd.pivot_table(
    df,
    values="成绩",
    index="班级",
    columns="性别",
    aggfunc="mean"
).round(1)

print(pivot)