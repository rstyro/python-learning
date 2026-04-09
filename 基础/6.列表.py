#!/usr/bin/python3

# 1. 列表的创建方式
# 空列表
empty_list = []
# 存储不同数据类型
mix_list = [1, 3.14, 'python', True, [1,2,3]]
# 使用list()函数创建
str_list = list('hello')
num_list = list(range(1, 6))

print("1. 列表创建")
print(f"混合列表: {mix_list}")
print(f"字符串转列表: {str_list}")
print(f"数字列表: {num_list}\n")

# 2. 列表索引与切片
test_list = [10, 20, 30, 40, 50]
print("2. 列表索引与切片")
# 正索引
print(f"第一个元素: {test_list[0]}")
# 负索引
print(f"最后一个元素: {test_list[-1]}")
# 切片
print(f"索引1-3: {test_list[1:4]}")
print(f"步长为2: {test_list[::2]}")
print(f"反转列表: {test_list[::-1]}")
print(f"整个列表的副本: {test_list[:]}\n")

# 3. 列表元素修改
print("3. 修改列表元素")
test_list[2] = 300
print(f"修改后: {test_list}")
# 切片修改
test_list[1:3] = [200, 300]
print(f"切片修改后: {test_list}\n")

# 4. 列表添加元素
add_list = [1,2,3]
print("4. 列表添加元素")
# append()追加单个元素
add_list.append(4)
print(f"append后: {add_list}")
# extend()追加多个元素
add_list.extend([5,6])
print(f"extend后: {add_list}")
# insert()指定位置插入
add_list.insert(0, 0)
print(f"insert插入后: {add_list}\n")

# 5. 列表删除元素
del_list = [1,2,3,4,5,3]
print("5. 列表删除元素")
# del删除指定索引
del del_list[0]
print(f"del删除后: {del_list}")
# pop()删除指定索引元素，默认最后一个
del_list.pop()
print(f"pop后: {del_list}")
# remove()删除第一个匹配元素
del_list.remove(3)
print(f"remove后: {del_list}")
# clear()清空列表
del_list.clear()
print(f"clear清空后: {del_list}\n")

# 6. 列表常用内置函数与方法
sort_list = [5,2,8,1,9]
print("6. 列表常用操作")
# len()获取长度
print(f"列表长度: {len(sort_list)}")
# max()/min()最大最小值
print(f"最大值: {max(sort_list)}, 最小值: {min(sort_list)}")
# count()统计元素个数
print(f"元素2出现次数: {sort_list.count(2)}")
# index()查找元素索引
print(f"元素8的索引: {sort_list.index(8)}")
# sort()原地升序排序
sort_list.sort()
print(f"sort升序: {sort_list}")
# sort(reverse=True)降序
sort_list.sort(reverse=True)
print(f"sort降序: {sort_list}")
# reverse()反转列表
sort_list.reverse()
print(f"reverse反转: {sort_list}\n")

# 7. 列表复制
copy_list = [1,2,3]
# 浅拷贝
new_list1 = copy_list.copy()
new_list2 = copy_list[:]
new_list1.append(4)
print("7. 列表复制")
print(f"原列表: {copy_list}")
print(f"拷贝后修改的列表: {new_list1}\n")

# 8. 列表遍历
print("8. 列表遍历")
for i in [1,2,3]:
    print(f"遍历元素: {i}")
# 带索引遍历,Python内置的 enumerate 函数可以把一个 list 变成索引-元素对
for idx, val in enumerate(['a','b','c']):
    print(f"索引{idx}: {val}")
print()

# 9. 列表嵌套（二维列表）
print("9. 嵌套列表")
nested_list = [[1,2],[3,4],[5,6]]
print(f"二维列表: {nested_list}")
print(f"获取元素4: {nested_list[1][1]}\n")

# 10. 列表推导式
print("10. 列表推导式")
# 生成1-5平方
square_list = [x**2 for x in range(1,6)]
print(f"平方列表: {square_list}")
# 带条件筛选
even_list = [x for x in range(10) if x % 2 == 0]
print(f"偶数列表: {even_list}")

# 11. 成员运算
print("\n11. 成员运算")
print(2 in [1,2,3])
print(5 not in [1,2,3])

# 12. 列表拼接与重复
print("\n12. 拼接与重复")
print([1,2] + [3,4])
print([1,2] * 3)