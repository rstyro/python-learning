# 接收文本输入
username = input("请输入你的用户名：")
print("你好，", username)

# 接收数字，需转换类型
# int() 将字符串转为整数
age = int(input("请输入你的年龄："))
print("明年你", age + 1, "岁")

# float() 转为浮点数
score = float(input("请输入考试分数："))
print("分数：",score)


print("===== 常见坑点 =====")
# 错误代码：不转换类型直接计算
# num = input("输入数字：")
# print(num + 10)  # 报错，str和int不能相加
# 正确做法
num = int(input("输入数字："))
print(f"数字+10：{num + 10}")