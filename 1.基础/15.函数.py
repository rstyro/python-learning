#!/usr/bin/python3

# ============== 1. 基础函数定义与调用 ==============
print("===== 1. 基础函数 =====")
# 定义函数
def say_hello():
    print("Hello Python!")
    print("这是自定义函数")

# 调用函数
say_hello()

# ============== 2. 带参数的函数 ==============
print("\n===== 2. 带参数函数 =====")
def add_num(a, b):
    print(f"{a} + {b} = {a + b}")

# 位置传参
add_num(10, 20)

# ============== 3. 带返回值的函数 ==============
print("\n===== 3. 带返回值函数 =====")
def multiply(a, b):
    return a * b

result = multiply(5, 6)
print(f"计算结果: {result}")

# 多返回值
def get_info():
    name = "小明"
    age = 18
    return name, age

n, a = get_info()
print(f"姓名: {n}, 年龄: {a}")

# ============== 4. 关键字参数 ==============
print("\n===== 4. 关键字参数 =====")
def person_info(name, age, gender):
    print(f"姓名:{name}, 年龄:{age}, 性别:{gender}")

# 打乱顺序传参
person_info(age=20, name="小红", gender="女")

# ============== 5. 默认参数 ==============
print("\n===== 5. 默认参数 =====")
def student(name, grade="一年级"):
    print(f"学生:{name}, 年级:{grade}")

# 不传使用默认值
student("小李")
# 传参覆盖默认值
student("小张", "二年级")

# ============== 6. 可变位置参数 *args ==============
print("\n===== 6. 可变参数*args =====")
def sum_all(*args):
    total = 0
    for i in args:
        total += i
    return total

print(f"求和: {sum_all(1,2,3,4,5)}")

# ============== 7. 可变关键字参数 **kwargs ==============
print("\n===== 7. 关键字参数**kwargs =====")
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="小王", score=99, subject="数学")

# ============== 8. 函数嵌套 ==============
print("\n===== 8. 函数嵌套 =====")
def outer():
    print("外层函数")
    def inner():
        print("内层函数")
    inner()

outer()

# ============== 9. 匿名函数 lambda ==============
print("\n===== 9. lambda匿名函数 =====")
# 简单函数使用lambda
func = lambda x, y: x * y
print(f"lambda计算: {func(3, 4)}")

# ============== 10. 变量作用域 ==============
print("\n===== 10. 变量作用域 =====")
# 全局变量
num = 100

def test_scope():
    # 局部变量
    num = 200
    print(f"函数内num: {num}")

test_scope()
print(f"函数外num: {num}")

# global声明全局变量
def change_global():
    global num
    num = 300

change_global()
print(f"修改后全局num: {num}")

# ============== 11. 递归函数 ==============
print("\n===== 11. 递归函数 =====")
# 阶乘递归
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)

print(f"5的阶乘: {factorial(5)}")