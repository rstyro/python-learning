#!/usr/bin/python3

print("=====1、函数作为参数传递======")
# 1. 函数作为参数传递
def say_hello():
    print("Hello")

def execute_func(func):
    print("开始执行函数")
    func()
    print("执行完毕")

# 函数可以作为参数传递
execute_func(say_hello)


print("\n=====2、定义装饰器（外层接收函数，内层包装功能）======")
# 定义装饰器（外层接收函数，内层包装功能）
def my_decorator(func):
    # 包装函数
    def wrapper():
        print("===== 功能增强前 =====")
        # 调用原函数
        func()
        print("===== 功能增强后 =====")
    return wrapper

# 定义普通函数
def test():
    print("我是原函数功能")

# 手动装饰
test = my_decorator(test)
# 调用
test()


print("\n=====3、定义装饰器:语法糖 @ 符号======")
# 语法糖 @ 符号（常用写法）
def my_decorator2(func):
    def wrapper():
        print("===== 功能增强前 =====")
        func()
        print("===== 功能增强后 =====")
    return wrapper

# @装饰器名 = 自动完成包装
@my_decorator2
def test2():
    print("@我是原函数功能")

test2()
print("\n")



print("\n=====4、定义装饰器:适配任意参数======")
def my_decorator3(func):
    def wrapper(*args, **kwargs):
        print("执行前操作")
        result = func(*args, **kwargs)
        print("执行后操作")
        return result
    return wrapper

@my_decorator3
def func1(name):
    print(f"你好{name}")

@my_decorator3
def func2(a, b, c):
    return a + b + c

func1("小明")
print(func2(1,2,3))

print("\n=====5、带参数的装饰器======")
# 外层再包一层接收参数
def decorator_with_param(msg):
    print("接收到的参数：",msg)
    def my_decorator_with_param(func):
        def wrapper():
            print(msg)
            func()
        return wrapper
    return my_decorator_with_param

@decorator_with_param("这是装饰器参数")
def test_with_param():
    print("原函数")

test_with_param()

print("\n=====6、多个装饰器叠加======")
def decorator1(func):
    def wrapper():
        print("装饰器1 前置")
        func()
        print("装饰器1 后置")
    return wrapper

def decorator2(func):
    def wrapper():
        print("装饰器2 前置")
        func()
        print("装饰器2 后置")
    return wrapper

# 执行顺序：从上到下装饰，从下到上执行
@decorator1
@decorator2
def test_multiple():
    print("原函数")

test_multiple()