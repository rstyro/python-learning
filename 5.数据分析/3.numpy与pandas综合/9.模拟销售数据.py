import numpy as np
import pandas as pd

# 日期
dates = pd.date_range("2025-01-01", periods=100, freq="D")

# 用numpy生成随机数据
region = np.random.choice(["华北","华东","华南","西南"], 100)
sales = np.random.randint(100, 2000, 100)
cost = sales * np.random.uniform(0.4, 0.7, 100)  # 成本

df = pd.DataFrame({
    "日期": dates,
    "地区": region,
    "销售额": sales,
    "成本": cost
})

df["利润"] = df["销售额"] - df["成本"]
print(df.head())