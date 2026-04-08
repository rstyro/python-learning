import pandas as pd

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五"],
    "成绩": [58, 75, 92]
})

# 自定义评级函数
def get_level(score):
    if score >= 90:
        return "优秀"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"

# 应用到整列
df["等级"] = df["成绩"].apply(get_level)

# 按行 apply;  axis=1函数会应用到每一行、axis=0（默认值）：函数会应用到每一列
df["评语"] = df.apply(lambda row: f"{row['姓名']}：{row['等级']}", axis=1)

print(df)