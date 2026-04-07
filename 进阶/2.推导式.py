#!/usr/bin/python3

# ============== 1. 列表推导式 [] ==============
print("===== 1. 列表推导式 =====")
# 基础格式：[表达式 for 变量 in 可迭代对象]
# 生成1-5的数字列表
list1 = [i for i in range(1, 6)]
print("基础列表:", list1)

# 生成1-5的平方列表
list2 = [i ** 2 for i in range(1, 6)]
print("平方列表:", list2)

# 带条件筛选：筛选偶数
list3 = [i for i in range(1, 11) if i % 2 == 0]
print("偶数列表:", list3)

# 多循环：二维组合
list4 = [f"{i}-{j}" for i in range(1, 3) for j in range(1, 3)]
print("多循环列表:", list4)

# ============== 2. 字典推导式 {} ==============
print("\n===== 2. 字典推导式 =====")
# 基础：键为数字，值为平方
dict1 = {i: i ** 2 for i in range(1, 6)}
print("基础字典:", dict1)

# 列表转字典
keys = ["name", "age", "gender"]
values = ["小红", 18, "女"]
dict2 = {k: v for k, v in zip(keys, values)}
print("列表转字典:", dict2)

# 条件筛选字典
dict3 = {i: i**2 for i in range(1, 6) if i % 2 != 0}
print("筛选后字典:", dict3)

# ============== 3. 集合推导式 {} ==============
print("\n===== 3. 集合推导式 =====")
# 自动去重+推导
set1 = {i % 3 for i in range(10)}
print("集合推导（自动去重）:", set1)

# 字符串去重
str_set = {char for char in "hello world"}
print("字符串去重集合:", str_set)

# ============== 4. 生成器推导式 () ==============
print("\n===== 4. 生成器推导式 =====")
# 使用()，返回生成器对象，节省内存
gen = (i for i in range(1, 5))
print("生成器对象:", gen)
# 遍历生成器
print("遍历生成器:", end=" ")
for num in gen:
    print(num, end=" ")

# ============== 5. 嵌套推导式 ==============
print("\n\n===== 5. 嵌套推导式 =====")
# 二维列表推导式
# range(start, stop, step)：range(1, 8, 3) 生成从1开始，步长为3，直到8（不包括8）的数字。所以：j 取值 1, 4, 7
matrix = [[i for i in range(j, j + 3)] for j in range(1, 8, 3)]
print("二维列表:", matrix)

# ============== 6. 结合if-else推导式 ==============
print("\n===== 6. 带if-else的推导式 =====")
# 偶数保留，奇数变为0
num_list = [i if i % 2 == 0 else 0 for i in range(1, 11)]
print("if-else推导:", num_list)