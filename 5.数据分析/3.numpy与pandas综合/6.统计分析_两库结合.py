import numpy as np
import pandas as pd

df = pd.DataFrame({
    "一班": np.random.randint(50,100,10),
    "二班": np.random.randint(50,100,10)
})

print(df,"\n")
# numpy 做统计
print("平均分:", np.mean(df["一班"]))
print("最高分:", np.max(df))
print("标准差:", np.std(df))