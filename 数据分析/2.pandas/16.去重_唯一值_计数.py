import pandas as pd

df = pd.DataFrame({
    "姓名": ["张三", "李四", "张三", "王五", "李四"],
    "城市": ["北京", "上海", "北京", "广州", "上海"]
})

# 查看唯一值
print("姓名唯一值：", df["姓名"].unique())

# 计数
print("\n姓名出现次数：")
print(df["姓名"].value_counts())

# 去重
df_drop = df.drop_duplicates(subset=["姓名"])
print("\n去重后：")
print(df_drop)