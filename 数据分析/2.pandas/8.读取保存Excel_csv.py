import pandas as pd

# 先造数据
data = {
    "姓名": ["张三", "李四", "王五"],
    "成绩": [90, 85, 92]
}
df = pd.DataFrame(data)

# 保存为 Excel（需要安装：pip install openpyxl）
df.to_excel("学生表.xlsx", index=False)
print("已保存：学生表.xlsx")

# 保存为 CSV
df.to_csv("学生表.csv", index=False, encoding="utf-8-sig")
print("已保存：学生表.csv")

# 读取文件
df_read = pd.read_excel("学生表.xlsx")
print("\n===== 读取回来的数据 =====")
print(df_read)