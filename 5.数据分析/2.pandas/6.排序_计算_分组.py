import pandas as pd

data = {
    "姓名": ["张三", "李四", "王五", "赵六", "钱七"],
    "成绩": [90, 85, 92, 78, 100],
    "城市": ["北京", "上海", "北京", "深圳", "上海"]
}
df = pd.DataFrame(data)

# 排序
print("===== 按成绩从高到低 =====")
print(df.sort_values("成绩", ascending=False))

# 统计
print("\n===== 总分、平均分、最高分 =====")
print("总分：", df["成绩"].sum())
print("平均分：", df["成绩"].mean())
print("最高分：", df["成绩"].max())

# 分组统计
print("\n===== 每个城市的平均分 =====")
print(df.groupby("城市")["成绩"].mean())