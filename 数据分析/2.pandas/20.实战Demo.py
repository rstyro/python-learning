# ==============================================
# Pandas 实战项目：超市销售数据分析
# 难度：进阶 | 适用：初学者练手、面试项目、工作实战
# ==============================================

import pandas as pd
import numpy as np

# ===================== 1. 生成模拟数据（真实项目可替换为 Excel）=====================
print("===== 1. 生成/加载销售数据 =====")

# 生成模拟销售数据（你以后可以换成 pd.read_excel("真实数据.xlsx")）
np.random.seed(2025)
data = {
    "订单日期": pd.date_range(start="2025-01-01", periods=500, freq="D"),
    "地区": np.random.choice(["华北", "华东", "华南", "西南", "西北"], 500),
    "城市": np.random.choice(["北京", "上海", "广州", "深圳", "成都", "西安"], 500),
    "商品类别": np.random.choice(["电子产品", "服装", "食品", "图书", "家电"], 500),
    "商品名称": np.random.choice(["手机", "T恤", "薯片", "Python书", "冰箱"], 500),
    "销量": np.random.randint(1, 10, 500),
    "单价": np.random.choice([1999, 99, 15, 59, 2999], 500),
    "成本": np.random.choice([1200, 50, 8, 30, 1800], 500)
}

df = pd.DataFrame(data)

# 查看前5行
print("数据前5行：")
print(df.head())
print(f"数据形状：{df.shape}")

# ===================== 2. 数据清洗（最关键！）=====================
print("\n===== 2. 数据清洗 =====")

# 2.1 查看缺失值
print("缺失值数量：")
print(df.isnull().sum())

# 2.2 计算销售额、利润（新增列）
df["销售额"] = df["销量"] * df["单价"]
df["利润"] = df["销量"] * (df["单价"] - df["成本"])

# 2.3 利润不能为负（异常值处理）
df.loc[df["利润"] < 0, "利润"] = 0

print("新增销售额、利润后：")
print(df[["商品名称", "销量", "销售额", "利润"]].head())

# ===================== 3. 基础数据分析 ====================
print("\n===== 3. 基础统计分析 =====")

# 总销售额、总利润
print(f"总销售额：{df['销售额'].sum():,} 元")
print(f"总利润：{df['利润'].sum():,} 元")

# 平均订单金额
print(f"平均每单销售额：{df['销售额'].mean():.2f} 元")

# ===================== 4. 地区销售分析 ====================
print("\n===== 4. 地区销售排名 =====")
area_sale = df.groupby("地区")["销售额"].sum().sort_values(ascending=False)
print(area_sale)

# ===================== 5. 商品类别分析 ====================
print("\n===== 5. 各类别销售额 & 利润 =====")
cate_analysis = df.groupby("商品类别").agg({
    "销售额": "sum",
    "利润": "sum",
    "销量": "sum"
}).sort_values("销售额", ascending=False)

print(cate_analysis)

# ===================== 6. 月度销售趋势 ====================
print("\n===== 6. 月度销售趋势 =====")
df["月份"] = df["订单日期"].dt.to_period("M")  # 提取年月
month_sale = df.groupby("月份")["销售额"].sum()
print(month_sale.head(10))

# ===================== 7. 爆款商品分析 ====================
print("\n===== 7. 销量最高的商品 =====")
product_top = df.groupby("商品名称")["销量"].sum().sort_values(ascending=False)
print(product_top)

# ===================== 8. 导出所有分析结果到 Excel ====================
print("\n===== 8. 导出分析报告 =====")

with pd.ExcelWriter("超市销售分析报告.xlsx") as writer:
    df.to_excel(writer, sheet_name="原始数据", index=False)
    area_sale.to_excel(writer, sheet_name="地区销售")
    cate_analysis.to_excel(writer, sheet_name="类别分析")
    month_sale.to_excel(writer, sheet_name="月度趋势")
    product_top.to_excel(writer, sheet_name="爆款商品")

print("✅ 分析完成！文件已保存：超市销售分析报告.xlsx")

# ===================== 9. 最终结论 ====================
print("\n===== 项目分析结论 =====")
print("1. 销售额最高的地区：", area_sale.index[0])
print("2. 最赚钱的商品类别：", cate_analysis.index[0])
print("3. 销量最高的商品：", product_top.index[0])