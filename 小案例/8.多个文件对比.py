import pandas as pd

# 读取文件
path = "file\\"

# 文件列表
df1 = pd.read_excel(path+"buket_list.xlsx",header=None)
df2 = pd.read_excel(path+"测试环境导出数据.xlsx")
df3 = pd.read_excel(path+"预发布环境导出数据.xlsx")

# 获取第一列所有数据（转成集合，方便对比）
data1 = set()
for value in df1.iloc[:, 0]:
    s = str(value).strip()  # 转字符串+去空格
    if s.startswith("bk-"):  # 只保留 bk- 开头
        data1.add(s)

# 获取 id列的数据，拼接bk-
data2 = set("bk-" + str(id) for id in df2["id"])
data3 = set("bk-" + str(id) for id in df3["id"])

# 1. data1 独有（两个环境都没有）
only_df1 = data1 - (data2 | data3)

# 2. data1 和 data2 共有
df1_and_df2 = data1 & data2

# 3. data1 和 data3 共有
df1_and_df3 = data1 & data3

# 4. 三个表都共有
all_three = data1 & data2 & data3

# ==============================
# 4. 输出所有结果
# ==============================
print("="*70)
print("🔹 1. 仅在 buket_list 存在，测试+预发布都没有")
print("="*70)
for item in sorted(only_df1):
    print(item)
print(f"总数：{len(only_df1)}")

print("\n" + "="*70)
print("🔹 2. buket_list 和 测试环境 共有")
print("="*70)
for item in sorted(df1_and_df2):
    print(item)
print(f"总数：{len(df1_and_df2)}")

print("\n" + "="*70)
print("🔹 3. buket_list 和 预发布环境 共有")
print("="*70)
for item in sorted(df1_and_df3):
    print(item)
print(f"总数：{len(df1_and_df3)}")

print("\n" + "="*70)
print("🔹 4. 三个表（EOS+测试+预发布）都共有")
print("="*70)
for item in sorted(all_three):
    print(item)
print(f"总数：{len(all_three)}")


# 构建map
def build_bucket_map(df,env):
    bucket_map = {}
    for _, row in df.iterrows():
        bid = "bk-" + str(row["id"]).strip()
        status = str(row["status"]).strip()
        name = str(row["name"]).strip() if pd.notna(row["name"]) else ""
        bucket_map[bid] = {"status": status, "name": name,"env":env}
    return bucket_map

map2 = build_bucket_map(df2,'测试环境')
map3 = build_bucket_map(df3,'预发环境')

# 合并所有桶信息（优先取预发布，没有再取测试）
bucket_info = {}
for bid, info in map2.items():
    bucket_info[bid] = info
for bid, info in map3.items():
    bucket_info[bid] = info

all_project_buckets = set(bucket_info.keys())

status_list = []
name_list = []
env_list = []

for value in df1.iloc[:, 0]:
    bucket = str(value).strip()
    name = ""  # 默认空
    env = ""  # 默认空

    if bucket.startswith("bk-"):
        # 取项目名
        if bucket in bucket_info:
            name = bucket_info[bucket]["name"]
            env = bucket_info[bucket]["env"]

        # 取状态
        if bucket in all_project_buckets:
            if bucket_info[bucket]["status"] == "2":
                status_list.append("已删除")
            else:
                status_list.append("正常")
        else:
            status_list.append("不存在项目空间")
    else:
        status_list.append("非目标数据")

    name_list.append(name)
    env_list.append(env)

# ======================
# 3. Sheet1：桶名 + 项目名 + 状态
# ======================

result_df = pd.DataFrame({
    "桶名": df1.iloc[:, 0],
    "状态": status_list,
    "项目名": name_list,
    "环境": env_list
})
# ======================
# 4. Sheet2：不存在项目空间 + 已删除
# ======================
not_exist_df = result_df[
    (result_df["状态"] == "不存在项目空间") |
    (result_df["状态"] == "已删除")
    ][["桶名", "项目名", "状态","环境"]].copy()


# ==============================
# 3. 另存为新 Excel
# ==============================
output_path = path+"buket_list_更新.xlsx"

with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    result_df.to_excel(writer, sheet_name="完整数据", index=False)
    not_exist_df.to_excel(writer, sheet_name="可删除的", index=False)

print(f"✅ 文件已生成：{output_path}")
print("📊 列说明：原数据 + 新增【状态】列")