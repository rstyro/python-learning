import pandas as pd

df1 = pd.DataFrame({"姓名": ["张三", "李四"], "成绩": [88, 92]})
df2 = pd.DataFrame({"姓名": ["王五", "赵六"], "成绩": [79, 95]})

# 上下拼接
df_all = pd.concat([df1, df2], ignore_index=True)
print("=== 1、concat上下拼接 ===")
print(df_all)


# merge 左右关联
print("\n=== 2、merge 左右关联 ===")
df_user = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "姓名": ["张三", "李四", "王五", "赵六"]
})

df_score = pd.DataFrame({
    "id": [1, 2, 3, 5],
    "成绩": [88, 92, 79, 60]
})

# 内连接（只保留两边都有的）
df_inner = pd.merge(df_user, df_score, on="id", how="inner")
print("=== inner join ===")
print(df_inner)

# 左连接（保留左边全部）
df_left = pd.merge(df_user, df_score, on="id", how="left")
print("\n=== left join ===")
print(df_left)