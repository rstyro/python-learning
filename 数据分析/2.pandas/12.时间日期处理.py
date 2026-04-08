import pandas as pd

df = pd.DataFrame({
    "日期": ["2025-01-05", "2025-02-10", "2025-03-15", "2025-04-20"],
    "销售额": [100, 200, 150, 300]
})

# 转日期类型.
df["日期"] = pd.to_datetime(df["日期"])

# 提取年、月、日、星期
df["年"] = df["日期"].dt.year
df["月"] = df["日期"].dt.month
df["星期"] = df["日期"].dt.day_name()

# 按月份筛选
mask = df["日期"] >= "2025-03-01"
print(df[mask])