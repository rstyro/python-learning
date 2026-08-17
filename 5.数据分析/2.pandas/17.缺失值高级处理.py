import pandas as pd
import numpy as np

df = pd.DataFrame({
    "姓名": ["张三", None, "王五", "赵六"],
    "成绩": [88, np.nan, 79, None],
    "城市": ["北京", "上海", None, "深圳"]
})

# 删除任意空值行
df_drop_any = df.dropna(how="any")

# 删除全部为空的行
df_drop_all = df.dropna(how="all")

# 不同列填充不同值
df["成绩"] = df["成绩"].fillna(df["成绩"].mean())
df["城市"] = df["城市"].fillna("未知")

print(df)