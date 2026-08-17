import pandas as pd

# 1. 构造数据
df = pd.DataFrame({
    "姓名": [f"学生{i}" for i in range(1, 21)],
    "班级": ["一班"]*10 + ["二班"]*10,
    "成绩": [82, 76, 95, 63, 88, 59, 91, 77, 84, 70,
             90, 85, 72, 66, 55, 93, 81, 79, 69, 87]
})

# 2. 基础信息
print("===== 数据概览 =====")
print(df.shape)
print(df.describe())

# 3. 不及格人数
print("\n===== 不及格人数 =====")
print(df[df["成绩"] < 60].shape[0])

# 4. 各班统计
print("\n===== 各班成绩统计 =====")
print(df.groupby("班级")["成绩"].agg(["mean", "max", "min"]))

# 5. 保存结果
df.to_excel("成绩分析结果.xlsx", index=False)
print("\n已保存到 成绩分析结果.xlsx")

print("\n打印表格:")
print(df)