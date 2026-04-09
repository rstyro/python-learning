# -*- coding: utf-8 -*-
"""
Python 生成器函数
"""


# ====================== 1. 最简单生成器 ======================
# 特点：yield 会暂停函数，下次调用从暂停处继续
def simple_generator():
    yield 1
    yield 2
    yield 3


# ====================== 2. 带参数生成器 ======================
def count_generator(n):
    for i in range(1, n + 1):
        yield i


# ====================== 3. 无限生成器 ======================
def infinite_counter():
    num = 0
    while True:
        yield num
        num += 1


# ====================== 4. send 传值给生成器 ======================
def receiver():
    print("生成器已启动")
    while True:
        value = yield
        print(f"收到外部值：{value}")


# ====================== 5. yield from 嵌套生成器 ======================
def sub_generator():
    yield 10
    yield 20


def main_generator():
    yield 1
    # 把子生成器的值全部迭代出来
    yield from sub_generator()
    yield 2


# ====================== 6. 生成器表达式 ======================
# (表达式 for 变量 in 可迭代对象)
# 对比：列表是[]，生成器是()
def generator_expression():
    # 列表推导式
    list_comp = [x * 2 for x in range(5)]
    # 生成器表达式
    gen_comp = (x * 2 for x in range(5))
    return list_comp, list(gen_comp)


# ====================== 7. 超大文件逐行读取（实战） ======================
# 一次只读一行，GB级文件不占内存
def read_large_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        yield "文件不存在，此为演示示例"


# ====================== 8. 斐波那契生成器（面试高频） ======================
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        # 返回当前项
        yield a
        # 计算下一项
        a, b = b, a + b


# ====================== 9. 生成器管道（数据流处理） ======================
# 多个生成器串联，内存零压力
def numbers():
    for i in range(10):
        yield i


def even(nums):
    for n in nums:
        if n % 2 == 0:
            yield n


def square(nums):
    for n in nums:
        yield n ** 2


# ====================== 主运行入口 ======================
if __name__ == '__main__':
    print("===== 1. 基础生成器 next() =====")
    gen1 = simple_generator()
    print(next(gen1))
    print(next(gen1))
    print(next(gen1))

    print("\n===== 2. for 遍历生成器 =====")
    for num in count_generator(5):
        print(num, end=' ')
    print()

    print("\n===== 3. 无限生成器（取前5个） =====")
    gen2 = infinite_counter()
    for _ in range(5):
        print(next(gen2), end=' ')
    print()

    print("\n===== 4. send 向生成器传值 =====")
    gen3 = receiver()
    next(gen3)
    gen3.send("Hello Generator")
    gen3.send("Python 教程")

    print("\n===== 5. yield from 嵌套生成器 =====")
    for num in main_generator():
        print(num, end=' ')
    print()

    print("\n===== 6. 生成器表达式 =====")
    list_res, gen_res = generator_expression()
    print("列表:", list_res)
    print("生成器转列表:", gen_res)

    print("\n===== 7. 大文件读取演示 =====")
    for line in read_large_file("demo.txt"):
        print(line)

    print("\n===== 8. 斐波那契数列前10项 =====")
    print(list(fibonacci(10)))

    print("\n===== 9. 生成器管道（数字→偶数→平方） =====")
    pipeline = square(even(numbers()))
    print(list(pipeline))