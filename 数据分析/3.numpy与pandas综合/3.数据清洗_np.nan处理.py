import numpy as np
import pandas as pd

df = pd.DataFrame({
    "姓名": ["张三","李四",None,"王五"],
    "成绩": [88, np.nan, 76, 59]
})

# 查看空值
print(df.isnull().sum())

# 用 numpy 填充均值
df["成绩"] = df["成绩"].fillna(df["成绩"].mean())
print(df)