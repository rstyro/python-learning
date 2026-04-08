import numpy as np
import pandas as pd

# 生成学生数据
names = [f"学生{i}" for i in range(1, 21)]
scores = np.random.randint(0, 100, size=(20, 3))

df = pd.DataFrame(scores, columns=["语文","数学","英语"], index=names)
print(df.head())