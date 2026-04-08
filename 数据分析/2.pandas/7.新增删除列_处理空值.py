import pandas as pd

data = {
    "姓名": ["张三", "李四", None, "赵六", "钱七"],
    "成绩": [90, None, 92, 78, 100]
}
df = pd.DataFrame(data)

print("===== 原始数据（有空值） =====")
print(df)

# 查看空值
print("\n===== 每列空值数量 =====")
print(df.isnull().sum())

# 填充空值
df["成绩"] = df["成绩"].fillna(0)
print("\n===== 填充后成绩 =====")
print(df)

# 新增列
df["是否及格"] = df["成绩"] >= 60
print("\n===== 新增是否及格列 =====")
print(df)

# 删除列
df = df.drop("姓名", axis=1)
print("\n===== 删除姓名列后 =====")
print(df)