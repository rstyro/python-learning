#!/usr/bin/python3

# 1. 元组的创建方式
print("=====1. 元组创建=====")
# 空元组
empty_tuple = ()
# 多元素元组
num_tuple = (1, 2, 3, 4, 5)
# 省略小括号创建
str_tuple = "a", "b", "c"
# 单元素元组（必须加逗号，否则是普通数据）
single_tuple = (10,)
# 混合数据类型
mix_tuple = (1, 3.14, "python", True)
# tuple()函数创建
range_tuple = tuple(range(1, 6))
str_to_tuple = tuple("hello")

print(f"空元组: {empty_tuple}")
print(f"单元素元组: {single_tuple}")
print(f"数字元组: {num_tuple}")
print(f"字符串转元组: {str_to_tuple}")
print(f"range元组: {range_tuple}")

# 2. 元组索引与切片
print("\n=====2. 索引与切片=====")
test_tuple = (10, 20, 30, 40, 50)
# 正索引
print(f"第一个元素: {test_tuple[0]}")
# 负索引
print(f"最后一个元素: {test_tuple[-1]}")
# 切片
print(f"索引1-3: {test_tuple[1:4]}")
print(f"步长为2: {test_tuple[::2]}")
print(f"反转元组: {test_tuple[::-1]}")

# 3. 元组不可变特性（重点）
print("\n=====3. 元组不可变性=====")
# test_tuple[0] = 100  # 取消注释会报错，元组元素不能修改
# 嵌套元组，内部可变对象可修改
nest_tuple = (1, 2, [3, 4])
nest_tuple[2][0] = 300
print(f"修改嵌套列表后的元组: {nest_tuple}")

# 4. 元组拼接与重复
print("\n=====4. 拼接与重复=====")
tuple1 = (1, 2)
tuple2 = (3, 4)
# 拼接
print(f"元组拼接: {tuple1 + tuple2}")
# 重复
print(f"元组重复: {tuple1 * 3}")

# 5. 元组常用内置函数
print("\n=====5. 内置函数=====")
num = (5, 1, 8, 3, 9)
# 长度
print(f"长度: {len(num)}")
# 最大最小值
print(f"最大值: {max(num)}, 最小值: {min(num)}")
# 求和
print(f"求和: {sum(num)}")

# 6. 元组内置方法
print("\n=====6. 元组方法=====")
test = (1, 2, 2, 3, 2)
# 统计元素出现次数
print(f"元素2出现次数: {test.count(2)}")
# 查找元素第一个索引
print(f"元素3的索引: {test.index(3)}")

# 7. 成员运算
print("\n=====7. 成员运算=====")
print(2 in test)
print(6 not in test)

# 8. 元组遍历
print("\n=====8. 元组遍历=====")
for item in ("apple", "banana", "orange"):
    print(f"元素: {item}")
# 带索引遍历
for idx, val in enumerate(("a", "b", "c")):
    print(f"索引{idx}: {val}")

# 9. 元组解包
print("\n=====9. 元组解包=====")
a, b, c = (10, 20, 30)
print(f"a={a}, b={b}, c={c}")
# 通配符解包
x, *y, z = (1, 2, 3, 4, 5)
print(f"x={x}, y={y}, z={z}")

# 10. 删除元组
print("\n=====10. 删除元组=====")
del_tuple = (1, 2, 3)
del del_tuple
# print(del_tuple)  # 取消注释报错，元组已被删除