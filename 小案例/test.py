# 函数文档字符串（docstring）的查看：
def add(x, y):
    """返回 x 和 y 的和"""
    return x + y
print(add.__doc__)     # 或 help(add)

# 闭包（closure）：内部函数引用外部函数的变量
def outer(x):
    def inner(y):
        return x + y
    return inner
add5 = outer(5)
print(add5(3))