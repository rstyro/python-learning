import numpy as np
import pandas as pd

df = pd.DataFrame({
    "姓名": ["学生1","学生2","学生3","学生4"],
    "成绩": [77,55,92,49]
})

# numpy 布尔判断
mask = np.array(df["成绩"] >= 60)
print("布尔掩码:", mask)

# 筛选及格
print(df[mask])