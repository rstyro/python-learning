import pandas as pd

df = pd.DataFrame({
    "姓名": ["  zhangSan  ", "LI SI", "WangWu", "zhaoliu"],
    "邮箱": ["zhangsan@163.com", "lisi@gmail.com", None, "zhaoliu@qq.com"]
})

# 去空格 + 转小写
df["姓名"] = df["姓名"].str.strip().str.lower()

# 提取邮箱域名
df["域名"] = df["邮箱"].str.split("@").str[-1]

# 判断是否包含 gmail
df["是gmail"] = df["邮箱"].str.contains("gmail", na=False)

print(df)