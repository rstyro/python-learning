# Python-Learning
- Python 入门学习笔记 & 代码 Demo，适合零基础快速上手


## 一、基本语法

### 1、HelloWorld

```python
#!/usr/bin/python3

print("Hello, World!")

# 中文
print("你好，世界!!")
```

### 2、文件编码
- Python3 源码文件**默认使用 UTF-8 编码**
- 所有字符串默认为 Unicode 字符串，**直接支持中文**



```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-
```



### 3、标识符

标识符是给变量、函数、类等起的名字，必须遵守以下规则：

- 首字符必须是 **字母（a-z/A-Z）** 或 **下划线 `_`**
- 其他部分可包含：字母、数字、下划线
- **大小写敏感**：`count` ≠ `Count`
- 不能使用 Python 关键字
- 支持 Unicode：可用**中文、特殊符号（如 π）** 作为标识符
- 长度无限制，建议简洁易懂（≤20 字符）



#### 合法标识符：

```bash
age = 25                # 普通变量
user_name = "Alice"     # 下划线命名（推荐）
_total = 100            # 内部变量
MAX_SIZE = 1024         # 常量（全大写）
calculate_area()        # 函数名
StudentInfo             # 类名（大驼峰）
__private_var           # 私有变量（双下划线）
姓名 = "张三"            # 中文变量（合法）
π = 3.14159             # 特殊符号（合法）
```

#### 非法标识符：

```bash
2nd_place = "silver"    # 错误：数字开头
user-name = "Bob"       # 错误：不能用连字符
class = "Math"          # 错误：使用关键字
$price = 9.99           # 错误：特殊符号不允许
```

### 4、Python 保留关键字

保留关键字是 Python 内置的语法单词，禁止自定义使用。

Python 的标准库提供了一个 keyword 模块，可以输出当前版本的所有关键字：

```bash
>>> import keyword
>>> keyword.kwlist
['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
>>> 
```

- **逻辑值**
  - `True` 布尔真值
  - `False` 布尔假值
  - `None` 空值/无值
- **逻辑运算**
  - `and` 逻辑与
  - `or` 逻辑或
  - `not` 逻辑非
  - `in` 成员判断（是否在…中）
  - `is` 身份判断（是否是同一个对象）
- **条件控制**
  - `if` 如果
  - `elif` 否则如果
  - `else` 否则
- **循环控制**
  - `for` for 循环
  - `while` while 循环
  - `break` 跳出当前循环
  - `continue` 跳过本次循环，继续下一次
  - `pass` 空语句，占位用（不执行任何操作）
- **异常处理**
  - `try` 尝试执行代码
  - `except` 捕获异常
  - `finally` 无论是否异常都执行
  - `raise` 主动抛出异常
- **函数定义**
  - `def` 定义函数
  - `return` 函数返回值
  - `lambda` 匿名函数
  - `yield` 生成器函数返回（暂停并返回值）
- **类与对象**
  - `class` 定义类
  - `del` 删除对象/变量
- **模块导入**
  - `import` 导入模块
  - `from` 从模块导入
  - `as` 别名
- **作用域**
  - `global` 声明使用全局变量
  - `nonlocal` 声明使用外层非全局变量
- **异步编程**
  - `async` 定义异步函数
  - `await` 等待异步任务完成
- **其他**
  - `assert` 断言（调试用，条件不满足则报错）
  - `with` 简化资源操作（自动关闭文件/锁等）

### 5、注释
Python中单行注释以 # 开头，多行注释可以用多个 # 号，还有 ''' 和 """：

```python
#!/usr/bin/python3
 
# 第一个注释
# 第二个注释
 
'''
第三注释
第四注释
'''
 
"""
第五注释
第六注释
"""
print ("Hello, Python!")
```

### 6、行与缩进
- Python **不用大括号 `{}`**，使用**缩进**表示代码块
- 同一个代码块必须**缩进一致**（推荐 4 个空格）
- 如果缩进数的空格数不一致，会直接报错:`IndentationError`。

```python
if True:
    print ("Answer")
    print ("True")
else:
    print ("Answer")
  print ("False")    # 缩进不一致，会导致运行错误
```

- 以上程序由于缩进不一致，执行后会出现类似以下错误：
```python
IndentationError: unindent does not match any outer indentation level
```

### 7、多行语句
Python 通常是一行写完一条语句，但如果语句很长，我们可以使用反斜杠 \ 来实现多行语句，例如：

```python
item_one = 1
item_two = 2
item_three = 3
total = item_one + \
        item_two + \
        item_three
print(total) # 输出为 6
```

在 [], {}, 或 () 中的多行语句，不需要使用反斜杠 \，例如：

```python
total = ['item_one', 'item_two', 'item_three',
        'item_four', 'item_five']

```

### 8、数字(Number)类型
python中数字有四种类型：整数、布尔型、浮点数和复数。

- **int** (整数), 如 1, 只有一种整数类型 int，表示为长整型，没有 python2 中的 Long。
- **bool**  布尔值（`True` / `False`）。
- **float** (浮点数), 如 1.23、3E-2
- **complex** (复数) - 复数由实部和虚部组成，形式为 a + bj，其中 a 是实部，b 是虚部，j 表示虚数单位。如 1 + 2j、 1.1 + 2.2j



### 9、字符串(String)

字符串是 Python 最常用的数据类型。

**核心规则：**

- 单引号 `' '` 和双引号 `" "` **完全等价**
- 使用三引号(`'''` 或 `"""`)可以指定一个多行字符串。
- 转义字符：`\n`（换行）、`\t`（制表符）
- 反斜杠可以用来转义，使用 **r** 可以让反斜杠不发生转义。 如 **r"this is a line with \n"** 则 **\n** 会显示，并不是换行。
- 按字面意义级联字符串，如 **"this " "is " "string"** 会被自动转换为 **this is string**。
- 字符串可以用 **+** 运算符连接在一起，用 ***** 运算符重复。
- Python 中的字符串有两种索引方式，从左往右以 **0** 开始，从右往左以 **-1** 开始。
- Python 中的字符串**不可修改**
- Python 没有单独的字符类型，一个字符就是长度为 1 的字符串。
- 字符串切片 **str[start:end]**，其中 start（包含）是切片开始的索引，end（不包含）是切片结束的索引。
- 字符串的切片可以加上步长参数 step，语法格式如下：`str[start:end:step]`



```python
#!/usr/bin/python3
 
str='123456789'
 
print(str)                 # 输出字符串
print(str[0:-1])           # 输出第一个到倒数第二个的所有字符
print(str[0])              # 输出字符串第一个字符
print(str[2:5])            # 输出从第三个开始到第六个的字符（不包含）
print(str[2:])             # 输出从第三个开始后的所有字符
print(str[1:5:2])          # 输出从第二个开始到第五个且每隔一个的字符（步长为2）
print(str * 2)             # 输出字符串两次
print(str + '你好')         # 连接字符串
 
print('------------------------------')
 
print('hello\nworld')      # 使用反斜杠(\)+n转义特殊字符
print(r'hello\nworld')     # 在字符串前面添加一个 r，表示原始字符串，不会发生转义
```

### 10、print 输出

**print** 默认输出是换行的，如果要实现不换行需要在变量末尾加上 **end=""**：



```python
#!/usr/bin/python3
 
x="a"
y="b"
# 换行输出
print( x )
print( y )
 
print('---------')
# 不换行输出
print( x, end=" " )
print( y, end=" " )
print()
```



### 11、模块导入

用于引入 Python 内置或第三方库。

**常用导入方式**

```python
# 导入整个模块
import module

# 导入指定函数
from module import func

# 导入多个函数
from module import f1, f2

# 导入全部函数（不推荐大型项目使用）
from module import *
```



**示例**:

```python
import sys
print(sys.path)  # 打印Python路径
```



### 12、变量与赋值

变量本质是存储数据的容器，Python 无需提前声明变量类型，赋值的同时就完成了变量定义

```python
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

# 修改变量值
age = 19
print(age)


# 查看数据类型
print(type(age))        # <class 'int'>
print(type(b))        # <class 'float'>
print(type(name))     # <class 'str'>
print(type(is_ok)) # <class 'bool'>
```

### 13、标准数据类型

Python3 中常见的数据类型有：

- Number（数字）
- String（字符串）
- bool（布尔类型）
- List（列表）
- Tuple（元组）
- Set（集合）
- Dictionary（字典）

Python3 的六个标准数据类型中：

- **不可变数据（3 个）：**Number（数字）、String（字符串）、Tuple（元组）；
- **可变数据（3 个）：**List（列表）、Dictionary（字典）、Set（集合）。

此外还有一些高级的数据类型，如: 字节数组类型(bytes)。



### 14、列表（List）
列表是 Python 中最常用的可变序列，可存储不同类型的数据，用方括号 `[]` 定义。

#### 核心特性：
- 有序且可重复
- 支持增删改查
- 可嵌套（列表里包含列表）
- 索引和切片规则与字符串一致（索引从 0 开始，支持负索引、步长）

#### 常用操作：
```python
#!/usr/bin/python3

# 定义列表
nums = [1, 2, 3, 4, 5]
mix = [1, "Python", True, 3.14, [6, 7]]  # 混合类型+嵌套列表

# 访问元素
print(nums[0])       # 输出 1（正索引）
print(mix[-2])       # 输出 3.14（负索引）
print(mix[4][1])     # 输出 7（嵌套列表访问）

# 切片
print(nums[1:4])     # 输出 [2, 3, 4]
print(nums[::2])     # 输出 [1, 3, 5]（步长2）

# 修改元素
nums[2] = 30
print(nums)          # 输出 [1, 2, 30, 4, 5]

# 增加元素
nums.append(6)       # 末尾添加单个元素
print(nums)          # 输出 [1, 2, 30, 4, 5, 6]
nums.extend([7, 8])  # 末尾添加多个元素
print(nums)          # 输出 [1, 2, 30, 4, 5, 6, 7, 8]
nums.insert(1, 1.5)  # 指定位置插入元素
print(nums)          # 输出 [1, 1.5, 2, 30, 4, 5, 6, 7, 8]

# 删除元素
nums.remove(30)      # 删除指定值的元素
print(nums)          # 输出 [1, 1.5, 2, 4, 5, 6, 7, 8]
del nums[0]          # 删除指定索引的元素
print(nums)          # 输出 [1.5, 2, 4, 5, 6, 7, 8]
pop_num = nums.pop() # 弹出末尾元素（可指定索引）
print(pop_num)       # 输出 8
print(nums)          # 输出 [1.5, 2, 4, 5, 6, 7]

# 其他常用操作
print(len(nums))     # 输出列表长度 6
print(max(nums))     # 输出最大值 7
print(min(nums))     # 输出最小值 1.5
print(nums.count(2)) # 统计元素出现次数 1
nums.sort()          # 排序（默认升序）
print(nums)          # 输出 [1.5, 2, 4, 5, 6, 7]
nums.reverse()       # 反转列表
print(nums)          # 输出 [7, 6, 5, 4, 2, 1.5]
```

### 15、元组（Tuple）
元组是不可变序列，用圆括号 `()` 定义（空元组用 `()`，单个元素的元组需加逗号 `(1,)`）。

#### 核心特性：
- 有序且可重复
- 不可修改（一旦创建，元素不能增删改）
- 支持索引、切片（同字符串/列表）
- 可嵌套，可存储不同类型数据
- 比列表更节省内存，访问速度更快

#### 常用操作：
```python
#!/usr/bin/python3

# 定义元组
t1 = (1, 2, 3, 4)
t2 = (5, "Python", False)
t3 = (6, (7, 8))     # 嵌套元组
t4 = (9,)            # 单个元素的元组（必须加逗号）
t5 = ()              # 空元组

# 访问元素
print(t1[2])         # 输出 3
print(t3[1][0])      # 输出 7
print(t2[1:3])       # 输出 ('Python', False)

# 不可修改（以下代码会报错）
# t1[0] = 10  # TypeError: 'tuple' object does not support item assignment

# 常用操作
print(len(t1))       # 输出 4
print(max(t1))       # 输出 4
print(min(t1))       # 输出 1
print(t2.count("Python")) # 统计元素出现次数 1
print(t1.index(3))   # 查找元素索引 2

# 元组转列表（可间接修改）
lst = list(t1)
lst[0] = 10
t1_new = tuple(lst)
print(t1_new)        # 输出 (10, 2, 3, 4)
```

### 16、集合（Set）
集合是无序、不重复的可变序列，用大括号 `{}` 定义（空集合需用 `set()`，不能用 `{}`）。

#### 核心特性：
- 无序（无索引，不能通过索引访问）
- 元素唯一（自动去重）
- 支持集合运算（交集、并集、差集等）
- 元素必须是不可变类型（数字、字符串、元组，不能是列表/字典）

#### 常用操作：
```python
#!/usr/bin/python3

# 定义集合
s1 = {1, 2, 2, 3, 4}  # 自动去重，实际为 {1,2,3,4}
s2 = set([4, 5, 6])   # 列表转集合
s3 = set()            # 空集合（不能用 {}）

# 增加元素
s1.add(5)             # 添加单个元素
print(s1)             # 输出 {1,2,3,4,5}
s1.update([6,7])      # 添加多个元素
print(s1)             # 输出 {1,2,3,4,5,6,7}

# 删除元素
s1.remove(3)          # 删除指定元素（不存在则报错）
print(s1)             # 输出 {1,2,4,5,6,7}
s1.discard(10)        # 删除指定元素（不存在不报错）
s1.pop()              # 随机删除一个元素（集合无序）
print(s1)             # 输出（示例）{2,4,5,6,7}

# 集合运算
a = {1,2,3,4}
b = {3,4,5,6}
print(a & b)          # 交集 {3,4}
print(a | b)          # 并集 {1,2,3,4,5,6}
print(a - b)          # 差集 {1,2}
print(a ^ b)          # 对称差集（不重复的元素）{1,2,5,6}

# 其他操作
print(len(s1))        # 输出集合长度
print(5 in s1)        # 判断元素是否存在 True
s1.clear()            # 清空集合
print(s1)             # 输出 set()
```

### 17、字典（Dictionary）
字典是键值对（key:value）组成的可变、无序映射，用大括号 `{}` 定义，键唯一且不可变（字符串/数字/元组），值可任意。

#### 核心特性：
- 键值对映射，通过键访问值（无索引）
- 键唯一（重复键会覆盖）
- 可变（可增删改键值对）
- 无序（Python3.7+ 开始保留插入顺序）

#### 常用操作：
```python
#!/usr/bin/python3

# 定义字典
student = {
    "name": "张三",
    "age": 18,
    "gender": "男",
    "scores": {"math": 90, "english": 85}  # 嵌套字典
}

# 访问值
print(student["name"])          # 输出 张三（键存在）
# print(student["height"])      # 键不存在报错 KeyError
print(student.get("height"))    # 键不存在返回 None
print(student.get("height", 175)) # 键不存在返回默认值 175
print(student["scores"]["math"]) # 嵌套字典访问 90

# 修改值
student["age"] = 19
print(student)                  # age 变为 19

# 增加键值对
student["height"] = 175
student["hobbies"] = ["篮球", "编程"]
print(student)

# 删除键值对
del student["gender"]
print(student)                  # 移除 gender 键值对
pop_hobby = student.pop("hobbies")
print(pop_hobby)                # 输出 ['篮球', '编程']
student.clear()                 # 清空字典
print(student)                  # 输出 {}

# 其他常用操作
student = {"name": "张三", "age": 18}
print(len(student))             # 输出 2
print(student.keys())           # 输出所有键 dict_keys(['name', 'age'])
print(student.values())         # 输出所有值 dict_values(['张三', 18])
print(student.items())          # 输出所有键值对 dict_items([('name', '张三'), ('age', 18)])

# 遍历字典
for k, v in student.items():
    print(f"键：{k}，值：{v}")
```

### 18、条件语句
通过 `if/elif/else` 判断条件，执行不同代码块，核心是“条件为真则执行对应代码块”。

#### 语法格式：
```python
if 条件1:
    代码块1
elif 条件2:
    代码块2
else:
    代码块3
```

#### 示例：
```python
#!/usr/bin/python3

score = 85

if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")

# 嵌套条件
age = 18
if age >= 18:
    if age <= 25:
        print("青年")
    else:
        print("成年")
else:
    print("未成年")

# 多条件判断（and/or/not）
num = 10
if num > 0 and num < 20:
    print("0 < num < 20")
if num == 0 or num == 10:
    print("num 是 0 或 10")
if not (num < 0):
    print("num 非负数")
```

### 19、循环语句
#### （1）for 循环
遍历可迭代对象（列表、元组、字符串、字典、集合等），执行固定次数的循环。

```python
#!/usr/bin/python3

# 遍历列表
fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(f"水果：{fruit}")

# 遍历字符串
for char in "Python":
    print(char)

# 遍历字典
student = {"name": "张三", "age": 18}
for k in student:
    print(f"键：{k}，值：{student[k]}")

# range 生成序列（range(起始, 结束, 步长)，结束不包含）
# 遍历 0-4
for i in range(5):
    print(i)
# 遍历 2-8（步长2）
for i in range(2, 9, 2):
    print(i)  # 输出 2,4,6,8

# 循环嵌套（九九乘法表）
for i in range(1, 10):
    for j in range(1, i+1):
        print(f"{j}×{i}={i*j}", end="\t")
    print()  # 换行
```

#### （2）while 循环
满足条件时持续循环，需注意设置退出条件，避免死循环。

```python
#!/usr/bin/python3

# 基本 while 循环
count = 0
while count < 5:
    print(f"计数：{count}")
    count += 1  # 必须更新条件，否则死循环

# 死循环（需手动终止，如 break）
# while True:
#     print("按 Ctrl+C 终止")

# while + break/continue
num = 0
while num < 10:
    num += 1
    if num == 5:
        continue  # 跳过本次循环，不执行后续代码
    if num == 8:
        break     # 终止循环
    print(num)  # 输出 1,2,3,4,6,7
```

### 20、函数
函数是可复用的代码块，用 `def` 定义，可接收参数、返回值，提高代码复用性。

#### 核心概念：
- 函数名：符合标识符规则，见名知意
- 参数：形参（定义时）、实参（调用时）
- 返回值：`return` 语句返回，无返回值则返回 `None`
- 作用域：局部变量（函数内）、全局变量（函数外）

#### 示例：
```python
#!/usr/bin/python3

# 无参数、无返回值
def say_hello():
    print("Hello Python!")

say_hello()  # 调用函数

# 有参数、有返回值
def calculate_sum(a, b):
    """计算两个数的和（函数文档字符串）"""
    result = a + b
    return result

sum_num = calculate_sum(3, 5)
print(sum_num)  # 输出 8

# 默认参数（需放在非默认参数后）
def print_info(name, age=18):
    print(f"姓名：{name}，年龄：{age}")

print_info("张三")        # 使用默认年龄 18
print_info("李四", 20)    # 覆盖默认值

# 可变参数（*args 接收多个位置参数，**kwargs 接收多个关键字参数）
def print_args(*args):
    print("位置参数：", args)  # 元组类型

def print_kwargs(**kwargs):
    print("关键字参数：", kwargs)  # 字典类型

print_args(1, 2, 3)
print_kwargs(name="张三", age=18)

# 全局变量与局部变量
num = 10  # 全局变量
def change_num():
    global num  # 声明使用全局变量
    num = 20    # 修改全局变量
    local_num = 30  # 局部变量（函数外不可访问）
    print("函数内 num：", num)

change_num()
print("函数外 num：", num)  # 输出 20
# print(local_num)  # 报错：局部变量不可访问
```

### 21、异常处理
通过 `try/except/finally/raise` 捕获和处理程序运行时的异常，避免程序崩溃。

#### 核心语法：
```python
try:
    # 可能出错的代码
except 异常类型1:
    # 处理异常1
except 异常类型2 as e:
    # 处理异常2（e 为异常信息）
else:
    # 无异常时执行
finally:
    # 无论是否异常都执行（如关闭文件、释放资源）
```

#### 示例：
```python
#!/usr/bin/python3

# 捕获指定异常
try:
    num = 10 / 0  # 除数为0，触发 ZeroDivisionError
except ZeroDivisionError as e:
    print(f"异常信息：{e}")  # 输出 division by zero

# 捕获多个异常
try:
    lst = [1,2,3]
    print(lst[5])  # 索引越界 IndexError
    # num = 10 / 0
except ZeroDivisionError:
    print("除数不能为0")
except IndexError:
    print("索引超出范围")

# 捕获所有异常（不推荐，不利于调试）
try:
    with open("test.txt", "r") as f:
        f.read()
except Exception as e:
    print(f"发生异常：{e}")

# else 和 finally
try:
    num = 10 / 2
except ZeroDivisionError:
    print("除数为0")
else:
    print("无异常，计算结果：", num)
finally:
    print("无论是否异常，都会执行")

# 主动抛出异常
def check_age(age):
    if age < 0:
        raise ValueError("年龄不能为负数")
    print(f"年龄：{age}")

try:
    check_age(-5)
except ValueError as e:
    print(f"捕获异常：{e}")
```

## 二、进阶语法（新增）
### 1、推导式
推导式是简洁创建序列（列表、集合、字典）的方式，一行代码完成循环+判断。

#### （1）列表推导式
```python
# 基本格式：[表达式 for 变量 in 可迭代对象 if 条件]
lst1 = [i for i in range(10)]  # [0,1,2,...,9]
lst2 = [i*2 for i in range(10) if i % 2 == 0]  # [0,4,8,12,16]
lst3 = [x + y for x in [1,2] for y in [3,4]]  # [4,5,5,6]
print(lst2)
```

#### （2）集合推导式
```python
# 基本格式：{表达式 for 变量 in 可迭代对象 if 条件}
s1 = {i for i in range(10) if i > 5}  # {6,7,8,9}
s2 = {x**2 for x in [1,2,2,3]}  # {1,4,9}（自动去重）
print(s1)
```

#### （3）字典推导式
```python
# 基本格式：{键表达式:值表达式 for 变量 in 可迭代对象 if 条件}
d1 = {i: i*2 for i in range(5)}  # {0:0,1:2,2:4,3:6,4:8}
d2 = {k: v for k, v in {"a":1, "b":2, "c":3}.items() if v > 1}  # {"b":2, "c":3}
print(d1)
```

### 2、迭代器与生成器
#### （1）迭代器
可逐个返回元素的对象，需实现 `__iter__()` 和 `__next__()` 方法，通过 `next()` 取值，直到抛出 `StopIteration`。

```python
# 创建迭代器
lst = [1,2,3]
it = iter(lst)  # 转换为迭代器
print(next(it))  # 1
print(next(it))  # 2
print(next(it))  # 3
# print(next(it))  # 抛出 StopIteration

# 遍历迭代器
it = iter(lst)
for i in it:
    print(i)
```

#### （2）生成器
特殊的迭代器，用 `yield` 替代 `return`，惰性生成数据（节省内存）。

```python
# 生成器函数
def gen_numbers(n):
    i = 0
    while i < n:
        yield i  # 暂停并返回值
        i += 1

# 使用生成器
gen = gen_numbers(3)
print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 2

# 遍历生成器
for num in gen_numbers(3):
    print(num)
```

### 3、装饰器
装饰器是修改函数/类行为的工具，不修改原代码，实现功能扩展（如日志、计时、权限校验）。

#### 基础示例（无参数装饰器）：
```python
#!/usr/bin/python3

# 定义装饰器
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"调用函数：{func.__name__}")
        result = func(*args, **kwargs)
        print(f"函数 {func.__name__} 执行完成")
        return result
    return wrapper

# 使用装饰器
@log_decorator
def add(a, b):
    return a + b

# 调用函数
print(add(3, 5))
# 输出：
# 调用函数：add
# 函数 add 执行完成
# 8
```

## 三、常用内置函数
Python 提供了大量内置函数，无需导入即可使用，常用如下：

| 函数 | 功能 | 示例 |
|------|------|------|
| `print()` | 输出内容 | `print("Hello")` |
| `input()` | 获取用户输入 | `name = input("请输入姓名：")` |
| `type()` | 查看数据类型 | `type(123) → <class 'int'>` |
| `len()` | 计算长度 | `len([1,2,3]) → 3` |
| `max()` | 取最大值 | `max(1,2,3) → 3` |
| `min()` | 取最小值 | `min(1,2,3) → 1` |
| `sum()` | 求和 | `sum([1,2,3]) → 6` |
| `abs()` | 绝对值 | `abs(-5) → 5` |
| `range()` | 生成整数序列 | `range(5) → 0-4` |
| `enumerate()` | 枚举（索引+元素） | `enumerate(["a","b"]) → (0,"a"),(1,"b")` |
| `zip()` | 打包多个可迭代对象 | `zip([1,2], ["a","b"]) → (1,"a"),(2,"b")` |
| `sorted()` | 排序（返回新序列） | `sorted([3,1,2]) → [1,2,3]` |
| `reversed()` | 反转（返回迭代器） | `list(reversed([1,2,3])) → [3,2,1]` |

## 四、编程规范（新增）
### 1、命名规范
- 变量/函数/模块：小写+下划线（snake_case），如 `user_name`、`calculate_sum`
- 类名：大驼峰（PascalCase），如 `StudentInfo`
- 常量：全大写+下划线，如 `MAX_SIZE`
- 私有变量/函数：前置双下划线，如 `__private_var`

### 2、代码格式
- 缩进：4 个空格（禁止用制表符）
- 行宽：每行不超过 80 个字符
- 空行：函数/类之间空 2 行，逻辑块之间空 1 行
- 空格：运算符两侧、逗号后加空格，如 `a = b + c`、`func(1, 2)`

### 3、注释规范
- 单行注释：`#` 后加空格，注释内容与代码隔一行（关键逻辑）
- 函数/类注释：文档字符串（docstring），说明功能、参数、返回值
- 避免无用注释：注释应解释“为什么”，而非“做什么”（代码本身应自解释）

## 五、常见问题与解决
### 1、缩进错误（IndentationError）
- 原因：代码块缩进不一致（空格数不同、混用空格/制表符）
- 解决：统一用 4 个空格缩进，编辑器开启“制表符转空格”

### 2、键错误（KeyError）
- 原因：访问字典不存在的键
- 解决：用 `dict.get(key, 默认值)` 替代 `dict[key]`

### 3、索引错误（IndexError）
- 原因：访问列表/元组不存在的索引
- 解决：先判断索引是否在合法范围，或用切片（超出范围不报错）

### 4、类型错误（TypeError）
- 原因：数据类型不匹配（如字符串+数字、列表索引用字符串）
- 解决：检查数据类型，必要时用 `int()`/`str()`/`float()` 转换

### 5、名称错误（NameError）
- 原因：使用未定义的变量/函数
- 解决：检查拼写，确保变量/函数已定义，作用域正确