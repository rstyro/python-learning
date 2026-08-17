import numpy as np
import pandas as pd

df = pd.DataFrame({"成绩": np.random.randint(0,100,10)})

# 及格/不及格
df["等级"] = np.where(df["成绩"] >= 60, "及格", "不及格")
print(df)