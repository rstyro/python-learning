# 基本赋值
age = 18
b = 3.14
name = "Python"
is_ok = True

# 多变量赋值
# 两个整型对象 1 和 2 的分配给变量 x 和 y，字符串对象 "three" 分配给变量 z。
x, y, z = 1, 2, "three"
# 多变量赋相同值
m = n = 0

print("age=",age)
print("x, y, z=",x, y, z)
print("m,n=",m,n)

# 修改变量值
age = 19
print("age修改后=",age)


# 查看数据类型
print(type(age))        # <class 'int'>
print(type(b))        # <class 'float'>
print(type(name))     # <class 'str'>
print(type(is_ok)) # <class 'bool'>