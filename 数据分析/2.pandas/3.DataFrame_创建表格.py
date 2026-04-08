import pandas as pd

# 字典创建 DataFrame（最常用）
data = {
    "姓名": ["张三", "李四", "王五", "赵六", "钱七"],
    "年龄": [18, 19, 18, 20, 19],
    "成绩": [90, 85, 92, 78, 100],
    "城市": ["北京", "上海", "北京", "深圳", "上海"]
}

df = pd.DataFrame(data)

print("===== 完整表格 =====")
print(df)

print("\n===== 前3行 =====")
print(df.head(3))

print("\n===== 行列数量 =====")
print(df.shape)
print(type(df.shape))