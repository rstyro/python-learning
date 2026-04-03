#!/usr/bin/python3

# ============== 1. 基础try-except ==============
print("===== 1. 基础异常捕获 =====")
try:
    # 可能出错的代码
    num = 10 / 0
    print(num)
except ZeroDivisionError:
    # 捕获除零异常
    print("错误：不能除以零")

# ============== 2. 捕获多个异常 ==============
print("\n===== 2. 捕获多个异常 =====")
try:
    # num = int("python")
    num = 10 / 0
except ZeroDivisionError:
    print("除零错误")
except ValueError:
    print("数值转换错误")

# ============== 3. 捕获所有异常 ==============
print("\n===== 3. 捕获所有异常 =====")
try:
    print(10 / 0)
except Exception as e:
    # 获取异常信息
    print(f"捕获到异常：{e}")

# ============== 4. try-except-else ==============
print("\n===== 4. else分支 =====")
# 无异常时执行else
try:
    num = 10 / 2
except Exception as e:
    print(f"异常：{e}")
else:
    print(f"计算成功，结果：{num}")

# ============== 5. try-except-finally ==============
print("\n===== 5. finally分支 =====")
# 无论是否异常，finally必定执行
try:
    print(10 / 0)
except:
    print("发生异常")
finally:
    print("无论如何都会执行的代码")

# ============== 6. 主动抛出异常 raise ==============
print("\n===== 6. 主动抛异常 =====")
def check_age(age):
    if age < 0:
        # 主动抛出值异常
        raise ValueError("年龄不能为负数")
    return age

try:
    check_age(-5)
except ValueError as e:
    print(f"捕获主动抛的异常：{e}")

# ============== 7. 自定义异常 ==============
print("\n===== 7. 自定义异常 =====")
# 继承Exception创建自定义异常
class AgeError(Exception):
    def __init__(self, msg):
        self.msg = msg

def check_age2(age):
    if age < 0 or age > 150:
        raise AgeError("年龄超出合理范围")

try:
    check_age2(200)
except AgeError as e:
    print(f"自定义异常：{e.msg}")

# ============== 8. 常见内置异常 ==============
print("\n===== 常见内置异常 =====")
# SyntaxError: 语法错误
# NameError: 未定义变量
# IndexError: 列表索引越界
# KeyError: 字典键不存在
# FileNotFoundError: 文件不存在