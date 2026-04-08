import pandas as pd

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "李四"],
    "成绩": [88, -5, 79, 92],
    "城市": ["北京", "上海", "广州", "上海"]
})

# 替换单个值
df["成绩"] = df["成绩"].replace(-5, 0)

# 批量替换
df["城市"] = df["城市"].replace({"北京": "BeiJing", "上海": "ShangHai"})

# 按条件修改
df.loc[df["成绩"] < 60, "成绩"] = 60

print(df)