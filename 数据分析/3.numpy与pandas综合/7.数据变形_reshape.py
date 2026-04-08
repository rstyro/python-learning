import numpy as np
import pandas as pd

# 一维数组 → 二维 → DataFrame
arr = np.arange(1, 21).reshape(5,4)
df = pd.DataFrame(arr, columns=["A","B","C","D"])
print(df)