import pandas as pd

data = {
    "姓名": ["张三", "李四", "王五", "赵六", "钱七"],
    "年龄": [18, 19, 18, 20, 19],
    "成绩": [90, 85, 92, 78, 100]
}
df = pd.DataFrame(data)

print("===== 基本信息（列名、类型、空值） =====")
df.info()

print("\n===== 统计信息（均值、最大、最小等） =====")
print(df.describe())

print("\n===== 所有列名 =====")
print(df.columns.tolist())