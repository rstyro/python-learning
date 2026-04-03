#!/usr/bin/python3

# 1. 字典的创建
print("=====1. 字典创建=====")
# 空字典
empty_dict = {}
# 标准键值对字典
person = {"name": "张三", "age": 20, "gender": "男"}
# 使用dict()函数创建
student = dict(name="李四", age=19, score=90)
# 嵌套字典
nest_dict = {"class": 1, "student": {"name": "王五", "score": 95}}

print(f"空字典: {empty_dict}")
print(f"个人信息: {person}")
print(f"嵌套字典: {nest_dict}")

# 2. 访问字典元素
print("\n=====2. 访问元素=====")
# 通过key访问
print(f"姓名: {person['name']}")
# get()访问，key不存在返回None，不报错
print(f"年龄: {person.get('age')}")
print(f"不存在的key: {person.get('height', '无数据')}")
# 访问嵌套字典
print(f"嵌套分数: {nest_dict['student']['score']}")

# 3. 修改字典元素
print("\n=====3. 修改元素=====")
person["age"] = 21
print(f"修改年龄后: {person}")
# 新增键值对
person["height"] = 180
print(f"新增身高后: {person}")

# 4. 删除字典元素
print("\n=====4. 删除操作=====")
del_dict = {"a": 1, "b": 2, "c": 3}
# del删除指定key
del del_dict["a"]
print(f"del删除后: {del_dict}")
# pop()删除并返回值
pop_val = del_dict.pop("b")
print(f"pop删除的值: {pop_val}, 剩余: {del_dict}")
# popitem()删除最后一对键值（Python3.7+）
del_dict.popitem()
print(f"popitem后: {del_dict}")
# clear()清空字典
del_dict.clear()
print(f"clear清空后: {del_dict}")

# 5. 获取所有键、值、键值对
print("\n=====5. 获取键值集合=====")
info = {"name": "小明", "age": 18, "score": 88}
# 所有key
print(f"所有键: {info.keys()}")
# 所有value
print(f"所有值: {info.values()}")
# 所有键值对
print(f"所有键值对: {info.items()}")

# 6. 字典遍历
print("\n=====6. 字典遍历=====")
# 遍历key
print("遍历key:")
for key in info:
    print(f"{key}: {info[key]}")
# 遍历键值对
print("\n遍历键值对:")
for k, v in info.items():
    print(f"{k} = {v}")

# 7. 字典常用方法
print("\n=====7. 常用方法=====")
test_dict = {"id": 1, "name": "test"}
# update()合并字典
test_dict.update({"age": 20})
print(f"update合并后: {test_dict}")
# copy()浅拷贝
copy_dict = test_dict.copy()
# fromkeys()创建字典
new_dict = dict.fromkeys(["a", "b"], 0)
print(f"fromkeys创建: {new_dict}")

# 8. 成员判断（判断key）
print("\n=====8. 成员运算=====")
print("name" in info)
print("height" not in info)

# 9. 内置函数
print("\n=====9. 内置函数=====")
print(f"字典长度: {len(info)}")
print(f"所有key转列表: {list(info)}")

# 10. 字典推导式
print("\n=====10. 字典推导式=====")
# 键为数字，值为平方
square_dict = {x: x**2 for x in range(1, 6)}
print(f"平方字典: {square_dict}")
# 条件筛选
filter_dict = {k: v for k, v in info.items() if v != 18}
print(f"筛选后字典: {filter_dict}")