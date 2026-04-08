import numpy as np
import pandas as pd

# ====================== 1. 生成数据 ======================
np.random.seed(10)
n = 30
df = pd.DataFrame({
    "姓名": [f"学生{i}" for i in range(1, n+1)],
    "班级": np.random.choice(["一班", "二班", "三班"], n),
    "语文": np.random.randint(40, 100, n),
    "数学": np.random.randint(40, 100, n),
    "英语": np.random.randint(40, 100, n)
})

# ====================== 2. 计算总分、平均分 ======================
df["总分"] = df[["语文","数学","英语"]].sum(axis=1)
df["平均分"] = df[["语文","数学","英语"]].mean(axis=1).round(1)

# ====================== 3. 评级 ======================
df["评级"] = np.where(df["平均分"] >= 80, "优秀",
                      np.where(df["平均分"] >= 60, "良好", "不及格"))

# ====================== 4. 班级分析 ======================
cls_analysis = df.groupby("班级").agg({
    "平均分": [np.mean, np.max, np.min],
    "总分": "sum"
}).round(1)

# ====================== 5. 输出结果 ======================
print("===== 班级成绩分析 =====")
print(cls_analysis)

print("\n===== 不及格学生 =====")
print(df[df["评级"] == "不及格"][["姓名","班级","平均分"]])

# ====================== 6. 导出报告 ======================
df.to_excel("班级成绩分析报告.xlsx", index=False)
print("\n✅ 报告已保存：班级成绩分析报告.xlsx")
print(df)