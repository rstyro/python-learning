# -*- coding: utf-8 -*-

# ====================== 1. 内置命名空间 ======================
# Python 启动就存在，如 print、input、int、str
# 可以通过 __builtins__ 访问
print("内置命名空间示例:", print, int)


# ====================== 2. 全局命名空间 ======================
# 模块顶层定义的变量、函数、类，属于全局命名空间
global_var = "我是全局变量"

def global_func():
    return "我是全局函数"

class GlobalClass:
    pass


# ====================== 3. 局部命名空间 ======================
def demo_func(param):
    # 函数内部变量 -> 局部命名空间
    local_var = "我是局部变量"
    print("局部命名空间变量:", local_var)
    print("函数参数也属于局部:", param)

    # 局部可以访问全局
    print("局部访问全局:", global_var)

# 外部无法访问局部变量
# print(local_var)  # 报错 NameError


# ====================== 4. 嵌套函数 & 闭包命名空间 ======================
def outer():
    outer_var = "外层函数变量"

    def inner():
        nonlocal outer_var  # 引用外层嵌套变量
        inner_var = "内层函数变量"
        print("内层访问嵌套:", outer_var)
        print("内层局部变量:", inner_var)

    inner()
    # print(inner_var)  # 无法访问内层局部


# ====================== 5. 类命名空间 & 对象命名空间 ======================
class Person:
    # 类属性 -> 类命名空间
    species = "人类"

    def __init__(self, name):
        # 实例属性 -> 对象命名空间
        self.name = name

    def say(self):
        print(self.name, "属于", Person.species)


# ====================== 6. global 关键字 修改全局变量 ======================
count = 0

def add_count():
    global count  # 声明使用全局变量
    count += 1


# ====================== 7. 查看命名空间内置方法 ======================
def show_namespace():
    a = 123
    print("\n=== 局部命名空间 vars() ===")
    print(vars())  # 局部命名空间字典

print("\n=== 全局命名空间 globals() ===")
print(globals())

print("\n=== 局部命名空间 locals() ===")
print(locals())


# ====================== 测试调用 ======================
if __name__ == '__main__':
    print("----- 全局命名空间 -----")
    print(global_var)
    print(global_func())

    print("\n----- 局部命名空间 -----")
    demo_func("测试参数")

    print("\n----- 嵌套命名空间 -----")
    outer()

    print("\n----- 类&对象命名空间 -----")
    p = Person("小明")
    print("类命名空间:", Person.species)
    print("对象命名空间:", p.name)

    print("\n----- global 修改全局 -----")
    add_count()
    print("全局count:", count)

    show_namespace()