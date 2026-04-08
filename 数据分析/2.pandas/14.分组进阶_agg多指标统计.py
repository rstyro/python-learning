import pandas as pd

df = pd.DataFrame({
    "班级": ["一班", "一班", "二班", "二班", "二班"],
    "姓名": ["张三", "李四", "王五", "赵六", "钱七"],
    "成绩": [88, 92, 79, 95, 85]
})

# 一次性统计多个指标
result = df.groupby("班级")["成绩"].agg([
    "count", "mean", "max", "min", "sum"
]).round(2)

print(result)