import numpy as np
import pandas as pd

# 用 NumPy 创建数据
arr = np.random.randint(50, 100, size=(5, 3))

# 转成 Pandas DataFrame
df = pd.DataFrame(arr, columns=["语文", "数学", "英语"], index=["学生1","学生2","学生3","学生4","学生5"])

print(df)
print()

# 新增一列
df['总分']=df.sum(axis=1)
print(df)