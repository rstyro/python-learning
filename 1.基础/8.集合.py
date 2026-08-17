#!/usr/bin/python3

# 1. 集合的创建
print("=====1. 集合创建=====")
# 空集合（必须用set()，{}是空字典）
empty_set = set()
# 普通集合，自动去重
num_set = {1, 2, 2, 3, 3, 4}
# 混合类型集合
mix_set = {1, "python", 3.14, True}
# 可迭代对象转集合
list_to_set = set([1, 2, 2, 3])
str_to_set = set("hello")
# 空集合不能用{}
print(f"空集合: {empty_set}")
print(f"自动去重后: {num_set}")
print(f"列表转集合: {list_to_set}")
print(f"字符串转集合: {str_to_set}")

# 2. 集合无序、无索引特性
print("\n=====2. 集合无序无索引=====")
# print(num_set[0]) 报错，集合不支持索引取值

# 3. 添加元素
print("\n=====3. 添加元素=====")
s = {1, 2, 3}
# add()添加单个元素
s.add(4)
s.add(4)  # 重复添加无效
print(f"add添加后: {s}")
# update()添加多个元素
s.update([5, 6])
print(f"update添加后: {s}")

# 4. 删除元素
print("\n=====4. 删除元素=====")
del_s = {1, 2, 3, 4, 5}
# remove()删除指定元素，不存在报错
del_s.remove(3)
print(f"remove删除后: {del_s}")
# discard()删除指定元素，不存在不报错
del_s.discard(10)
# pop()随机删除元素（集合无序）
del_s.pop()
print(f"pop随机删除后: {del_s}")
# clear()清空集合
del_s.clear()
print(f"clear清空后: {del_s}")

# 5. 集合关系运算（核心功能）
print("\n=====5. 集合关系运算=====")
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
# 交集：共同元素
print(f"交集: {a & b}")
print(f"交集intersection: {a.intersection(b)}")
# 并集：所有元素去重
print(f"并集: {a | b}")
print(f"并集union: {a.union(b)}")
# 差集：a有b没有
print(f"差集a-b: {a - b}")
print(f"差集difference: {a.difference(b)}")
# 对称差集：不同时存在的元素
print(f"对称差集: {a ^ b}")

# 6. 集合判断运算
print("\n=====6. 集合判断=====")
x = {1, 2}
y = {1, 2, 3, 4}
# 是否为子集
print(f"x是y的子集: {x.issubset(y)}")
# 是否为超集
print(f"y是x的超集: {y.issuperset(x)}")
# 是否无交集
print(f"x和{5}无交集: {x.isdisjoint({5})}")

# 7. 常用内置函数
print("\n=====7. 内置函数=====")
test_set = {5, 1, 9, 3}
print(f"长度: {len(test_set)}")
print(f"最大值: {max(test_set)}")
print(f"最小值: {min(test_set)}")
print(f"求和: {sum(test_set)}")

# 8. 成员运算
print("\n=====8. 成员运算=====")
print(3 in test_set)
print(10 not in test_set)

# 9. 集合遍历
print("\n=====9. 集合遍历=====")
for i in {"apple", "banana", "pear"}:
    print(f"集合元素: {i}")

# 10. 不可变集合frozenset
print("\n=====10. 不可变集合=====")
f_set = frozenset([1, 2, 3])
# f_set.add(4) 报错，不可修改
print(f"不可变集合: {f_set}")