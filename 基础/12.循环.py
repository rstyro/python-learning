#!/usr/bin/python3

# ============== 1. while循环 ==============
print("===== 1. 基础while循环 =====")
i = 1
# 条件满足则循环
while i <= 5:
    print(f"循环次数: {i}")
    i += 1

# while else：循环正常结束后执行
print("\n===== while else =====")
i = 1
while i <= 3:
    print(i)
    i += 1
else:
    print("while循环正常执行完毕")

# ============== 2. for循环 + range() ==============
print("\n===== 2. for循环与range =====")
# range(stop)：0到stop-1
for i in range(5):
    print(f"range(5): {i}")

# range(start, stop)
print("\nrange(2, 6):")
for i in range(2, 6):
    print(i)

# range(start, stop, step) 步长
print("\nrange(1, 10, 2):")
for i in range(1, 10, 2):
    print(i)

# ============== 3. for遍历可迭代对象 ==============
print("\n===== 3. 遍历序列 =====")
# 遍历列表
lst = ["苹果", "香蕉", "橙子"]
for fruit in lst:
    print(f"水果: {fruit}")

# 遍历字符串
for char in "Python":
    print(f"字符: {char}")

# 遍历字典
dic = {"name": "小明", "age": 18}
for k, v in dic.items():
    print(f"{k}: {v}")

# ============== 4. break 终止整个循环 ==============
print("\n===== 4. break 跳出循环 =====")
for i in range(1, 10):
    if i == 5:
        print("满足条件，终止循环")
        break
    print(i)

# ============== 5. continue 跳过当前循环 ==============
print("\n===== 5. continue 跳过本次 =====")
for i in range(1, 6):
    if i == 3:
        print("跳过数字3")
        continue
    print(i)

# ============== 6. 循环嵌套 ==============
print("\n===== 6. 循环嵌套 九九乘法表 =====")
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}*{i}={i*j}", end="\t")
    print()

# ============== 7. for else 用法 ==============
print("\n===== 7. for else =====")
for i in range(3):
    print(i)
else:
    print("for循环正常结束，执行else")

# 被break打断则不执行else
print("\nbreak打断for循环，else不执行:")
for i in range(3):
    if i == 2:
        break
    print(i)
else:
    print("这段不会执行")

# ============== 8. 无限循环 ==============
print("\n===== 8. 无限循环（按Ctrl+C终止） =====")
# while True:
#     print("无限循环")