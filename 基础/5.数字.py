#!/usr/bin/python3
# Python 数字类型 + 内置数字函数 + 复数详细讲解

# ============== 1. 数字基本类型 ==============
print("===== 1. 数字基本类型 =====")
# 整型 int
a = 10
# 浮点型 float
b = 3.14
# 复数 complex
c = 2 + 3j

print(f"整数: {a}, 类型: {type(a)}")
print(f"浮点数: {b}, 类型: {type(b)}")
print(f"复数: {c}, 类型: {type(c)}")

# ============== 2. 数字类型转换 ==============
print("\n===== 2. 数字类型转换 =====")
print(f"int(3.9)    = {int(3.9)}")      # 直接截断小数
print(f"float(5)    = {float(5)}")
print(f"complex(6)  = {complex(6)}")    # 虚部为0
print(f"complex(1,2)= {complex(1,2)}") # 1+2j

# ============== 3. 内置数字函数（无第三方模块）==============
print("\n===== 3. 内置数字函数 =====")
x = -8
y = 4.6
z = 4.4

# abs() 绝对值
print("abs(-8)         =", abs(x))

# round() 四舍五入
print("round(4.6)      =", round(y))
print("round(4.4)      =", round(z))

# max() 最大值
print("max(3, 9, 1)    =", max(3, 9, 1))

# min() 最小值
print("min(3, 9, 1)    =", min(3, 9, 1))

# pow(x,y) x的y次方
print("pow(2, 3)       =", pow(2, 3))

# divmod(x,y) 返回 (商, 余数)
print("divmod(10, 3)   =", divmod(10, 3))

# 用于复数的内置函数 abs() 求模长
com = 3 + 4j
print("abs(3+4j) 模长  =", abs(com))

# ============== 4. 复数 complex 详细讲解 ==============
print("\n===== 4. 复数详细操作 =====")
# 创建复数方式
c1 = 5 + 2j
c2 = complex(3, 1)

# 1. 获取实部 real
print("复数 c1 实部:", c1.real)

# 2. 获取虚部 imag
print("复数 c1 虚部:", c1.imag)

# 3. 共轭复数 conjugate()
print("c1共轭复数:", c1.conjugate())

# 4. 复数四则运算
print("c1 + c2 =", c1 + c2)
print("c1 - c2 =", c1 - c2)
print("c1 * c2 =", c1 * c2)
print("c1 / c2 =", c1 / c2)

# ============== 5. 进制转换内置函数 ==============
print("\n===== 5. 进制转换 =====")
num = 12
print("二进制 bin(12):", bin(num))
print("八进制 oct(12):", oct(num))
print("十六进制 hex(12):", hex(num))

# ============== 6. 布尔与数字关系 ==============
print("\n===== 6. 布尔值视为数字 =====")
print("int(True)  =", int(True))
print("int(False) =", int(False))