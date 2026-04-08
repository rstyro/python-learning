import numpy as np
import pandas as pd

df = pd.DataFrame({
    "班级": ["一班","一班","二班","二班"],
    "成绩": [88,76,92,67]
})

# 分组后用 np 函数
res = df.groupby("班级")["成绩"].agg([np.mean, np.max, np.min])
print(res)