#!/usr/bin/python3

# 1. 基础if语句
print("=====1. 基础if语句=====")
score = 85
if score >= 60:
    print("成绩及格")

# 2. if-else语句
print("\n=====2. if-else语句=====")
score = 55
if score >= 60:
    print("成绩及格")
else:
    print("成绩不及格")

# 3. if-elif-else 多条件判断
print("\n=====3. 多条件elif=====")
score = 92
if score >= 90:
    print("等级：优秀")
elif score >= 80:
    print("等级：良好")
elif score >= 60:
    print("等级：及格")
else:
    print("等级：不及格")

# 4. 条件嵌套
print("\n=====4. 条件嵌套=====")
age = 20
has_id = True
if age >= 18:
    print("已成年")
    if has_id:
        print("可以进入网吧")
    else:
        print("需要携带身份证")
else:
    print("未成年人禁止入内")

# 5. 三目运算符（简洁条件表达式）
print("\n=====5. 三目运算符=====")
num = 10
result = "偶数" if num % 2 == 0 else "奇数"
print(f"数字{num}是{result}")

# 6. 多条件逻辑运算 and/or/not
print("\n=====6. 逻辑运算符=====")
# and 同时满足
username = "admin"
password = "123456"
if username == "admin" and password == "123456":
    print("登录成功")
else:
    print("账号或密码错误")

# or 满足其一
weekday = 6
if weekday == 6 or weekday == 7:
    print("周末休息")
else:
    print("工作日上班")

# not 取反
is_raining = False
if not is_raining:
    print("可以出门游玩")

# 7. 判断成员关系 in/not in
print("\n=====7. 成员判断条件=====")
fruits = ["apple", "banana", "orange"]
if "apple" in fruits:
    print("苹果在列表中")

# 8. 空值判断
print("\n=====8. 空值判断=====")
# 0、空字符串、空列表、空字典、None 都会被视为False
text = ""
if not text:
    print("字符串为空")

lst = []
if not lst:
    print("列表为空")