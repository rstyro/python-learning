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

#### 知识点：

```
字符串常用方法速查：
  • 大小写转换：upper()、lower()、capitalize()、title()
  • 查找替换：find()、replace()、count()
  • 分割合并：split()、join()（推荐用 join 拼接字符串）
  • 去除空白：strip()、lstrip()、rstrip()
  • 判断内容：isdigit()、isalpha()、startswith()、endswith()

格式化方式：
  • f-string（推荐）：f"姓名：{name}，年龄：{age}"
  • format()："{} + {} = {}".format(a, b, a+b)
  • % 格式化："%s 今年 %d 岁" % (name, age)

不可变性的影响：
  • 每次修改字符串都会创建新对象，频繁拼接用 join() 或 io.StringIO
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
- 语法扩展：`lst[start:stop:step]`

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

#### 知识点

```
切片语法： [start:stop:step]
          ├─ start   默认0（正步长）或 -1（负步长）
          ├─ stop    默认 len（正步长）或 -len-1（负步长）
          └─ step    默认1；负数反向

取值用途：
  • 获取子列表 → 新列表
  • 浅拷贝 → lst[:]

赋值用途：
  • 替换子段 → lst[1:3] = [100,200]
  • 插入 → lst[2:2] = [a,b]
  • 删除 → lst[1:4] = []
  
列表作为栈（后进先出）：
  • append() → 入栈，pop() → 出栈（O(1)）

列表作为队列（先进先出）：
  • 效率低：pop(0) 是 O(n)
  • 推荐用 collections.deque

常用方法复杂度：
  • 索引/赋值：O(1)
  • append/pop()：O(1)
  • insert(i)/pop(i)/remove(val)：O(n)
  • in 判断：O(n)
  • 切片：O(k)（k 为切片长度）
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

#### 知识点

```
元组的“不可变”陷阱：
  • 若元组内包含可变元素（如列表），该列表的内容可以修改
  • 例：t = (1, [2,3])；t[1].append(4) 合法，但 t[1] = [5] 非法

元组解包（unpacking）：
  • a, b = (1, 2)   # 自动解包
  • a, *rest = (1, 2, 3, 4)   # rest = [2,3,4]（星号表达式）

单元素元组必须加逗号：
  • (1,)   # 元组
  • (1)    # 整数，不是元组

命名元组（collections.namedtuple）：
  • from collections import namedtuple
  • Point = namedtuple('Point', ['x', 'y'])
  • p = Point(10, 20)；print(p.x, p.y)
```





### 16、集合（Set）

集合是无序、不重复的可变序列，用大括号 `{}` 定义（空集合需用 `set()`，不能用 `{}`）。

#### 核心特性：
- 无序（无索引，不能通过索引访问）
- 元素唯一（自动去重）
- 支持集合运算（交集、并集、差集等）
- 元素必须是不可变类型（数字、字符串、元组，不能是列表/字典）

#### 

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



#### 知识点

```
字典的键必须可哈希：
  • 不可变类型：int, str, tuple, frozenset
  • 可变类型：list, dict, set 不能作为键

常用方法进阶：
  • setdefault(key, default)：键不存在则设置并返回 default
  • update(dict2)：批量更新/合并
  • 字典合并（Python 3.9+）：merged = dict1 | dict2

字典推导式：
  • {k: v for k, v in iterable if condition}

获取值时避免 KeyError：
  • value = d.get(key, default_value)

遍历时修改字典：
  • 不能直接在迭代时增删键，可先转为列表：for k in list(d.keys()):
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



#### 知识点

```
三元表达式（条件表达式）：
  • value = true_value if condition else false_value
  • 示例：age_status = "成年" if age >= 18 else "未成年"

短路逻辑：
  • and：若左边为 False，右边不计算
  • or：若左边为 True，右边不计算
  • 常用于默认值：name = input_name or "匿名"

链式比较：
  • 0 < age < 120  等价于 0 < age and age < 120
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



#### 知识点

```
for-else 与 while-else：
  • else 子句在循环正常结束（未遇到 break）时执行
  • 常用于查找后处理：for i in range(n): if found: break else: print("未找到")

enumerate() 获取索引和值：
  • for idx, val in enumerate(['a','b','c']): print(idx, val)

zip() 并行遍历：
  • for name, score in zip(names, scores): print(name, score)

range() 的 step 可以是负数：
  • for i in range(5, 0, -1): print(i)   # 5,4,3,2,1

循环中修改列表的安全方式：
  • 倒序遍历：for i in range(len(lst)-1, -1, -1): ...
  • 或遍历副本：for item in lst[:]:
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



#### 知识点

```python
# 参数传递机制：传递的是对象的引用（“共享传参”）
def modify(lst):
    lst.append(4)      # 修改可变对象，会影响外部
    lst = [1,2,3]      # 重新绑定，不影响外部

# 关键字参数与位置参数的顺序：位置参数必须在关键字参数之前
def func(a, b, c=0): ...
func(1, b=2)           # 合法
# func(a=1, 2)         # 非法

# 可变参数混合使用：def func(a, b=1, *args, **kwargs):
#   *args 接收多余的位置参数（元组）
#   **kwargs 接收多余的关键字参数（字典）

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
print(add5(3))         # 8
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

### 4、文件操作（I/O）
- Python 使用内置 `open()` 函数操作文件，推荐使用 `with` 语句自动管理资源。
- **常用模式**：`'r'`（读）、`'w'`（写，覆盖）、`'a'`（追加）、`'rb'`/`'wb'`（二进制）

```python
# 写文件
with open('test.txt', 'w', encoding='utf-8') as f:
    f.write('第一行内容\n')
    f.write('第二行内容\n')

# 读文件（一次性读取全部）
with open('test.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)

# 逐行读取（适合大文件）
with open('test.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line, end='')

# 追加内容
with open('test.txt', 'a', encoding='utf-8') as f:
    f.write('追加的第三行\n')

# 二进制文件（如图片）
with open('image.jpg', 'rb') as f:
    data = f.read()
    print(f'读取了 {len(data)} 字节')
```

### 5、类与面向对象

- 类是创建对象的蓝图，支持封装、继承、多态。

**核心概念**：

- `__init__`：构造方法，初始化实例属性
- `self`：实例本身
- `@property`：将方法变成属性调用
- 继承：子类可重写父类方法



```python
# -*- coding: utf-8 -*-

# 1. 基础类定义与实例化
class Person:
    # 构造方法：创建对象时自动执行
    def __init__(self, name, age):
        # 实例属性
        self.name = name
        self.age = age

    # 实例方法
    def introduce(self):
        return f"我叫{self.name}，今年{self.age}岁"

    def eat(self, food):
        return f"{self.name}正在吃{food}"


# 2. 继承：子类继承父类
class Student(Person):
    def __init__(self, name, age, student_id):
        # 调用父类构造方法
        super().__init__(name, age)
        self.student_id = student_id

    # 方法重写
    def introduce(self):
        return f"我是学生{self.name}，学号{self.student_id}"

    # 子类独有方法
    def study(self, subject):
        return f"{self.name}学习{subject}"


# 3. 多继承
class Teacher(Person):
    def teach(self):
        return f"{self.name}在授课"

class Assistant(Student, Teacher):
    pass


# 4. 类属性、类方法、静态方法
class MathUtil:
    # 类属性
    pi = 3.14159

    # 类方法
    @classmethod
    def circle_area(cls, r):
        return cls.pi * r ** 2

    # 静态方法
    @staticmethod
    def add(a, b):
        return a + b


# 5. 私有属性与私有方法（封装）
class BankCard:
    def __init__(self, card_id, money):
        self.card_id = card_id
        # 私有属性，两个下划线开头，声明该属性为私有，不能在类的外部被使用或直接访问
        self.__money = money

    # 私有方法
    def __check_money(self):
        return self.__money >= 0

    # 公开接口
    def save_money(self, num):
        if num > 0:
            self.__money += num

    def get_money(self):
        return self.__money


# 6. property装饰器：将方法伪装成属性
class Book:
    def __init__(self, title):
        self.__title = title

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, new_title):
        if len(new_title) > 0:
            self.__title = new_title


# 7. 魔术方法（特殊方法）
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 打印对象时显示
    def __str__(self):
        return f"Point({self.x}, {self.y})"

    # 对象相加
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    # 获取长度
    def __len__(self):
        return abs(self.x) + abs(self.y)


# 8. 抽象类（需导入abc模块）
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "汪汪汪"

class Cat(Animal):
    def speak(self):
        return "喵喵喵"


# 9. 多态
def make_speak(animal: Animal):
    print(animal.speak())

```


### 6、类型注解（Type Hints）
- Python 3.5+ 支持类型注解，不强制检查，但可提高代码可读性，配合 IDE 实现静态类型检查。



```python
# 变量注解
name: str = "Alice"
age: int = 20
scores: list[int] = [90, 85, 88]
person: dict[str, any] = {"name": "Bob", "age": 25}

# 函数注解
def greet(name: str, age: int = 18) -> str:
    return f"{name} 今年 {age} 岁"

# 复杂类型需从 typing 导入（Python 3.9+ 可使用内置泛型）
from typing import List, Tuple, Optional

def process(items: List[str]) -> Tuple[int, Optional[str]]:
    if not items:
        return 0, None
    return len(items), items[0]

# 自定义类型别名
UserId = int
def get_user(uid: UserId) -> dict:
    return {"id": uid, "name": "test"}
```



### 7、命名空间与作用域

命名空间是变量名称到对象的映射。Python 的作用域遵循 **LEGB 规则**：

- **L**ocal：函数内部
- **E**nclosing：外层函数（闭包）
- **G**lobal：模块全局
- **B**uilt-in：内置名称（如 `print`、`len`）



```python
# 全局变量
global_var = 100

def outer():
    enclosing_var = 200   # 闭包变量

    def inner():
        local_var = 300   # 局部变量
        print(local_var)
        print(enclosing_var)   # 可以访问外层变量
        print(global_var)      # 可以访问全局变量

    return inner

func = outer()
func()

# global 和 nonlocal 关键字
x = 10
def modify_global():
    global x
    x = 20   # 修改全局变量

modify_global()
print(x)   # 20

def outer():
    y = 30
    def inner():
        nonlocal y   # 修改外层函数的变量
        y = 40
    inner()
    print(y)   # 40

outer()
```



### 8、正则表达式

正则表达式用于字符串匹配、查找、替换。Python 使用 `re` 模块。

**常用函数**：

- `re.search()`：查找第一个匹配
- `re.match()`：从开头匹配
- `re.findall()`：返回所有匹配列表
- `re.sub()`：替换
- `re.compile()`：预编译正则



```python
import re

text = "我的电话是 138-1234-5678，他的电话是 139-8765-4321"

# 匹配手机号（简单示例）
pattern = r'\d{3}-\d{4}-\d{4}'
phones = re.findall(pattern, text)
print(phones)   # ['138-1234-5678', '139-8765-4321']

# search 返回第一个匹配
match = re.search(pattern, text)
if match:
    print(match.group())   # 138-1234-5678

# 替换
new_text = re.sub(pattern, '***-****-****', text)
print(new_text)

# 分组提取
pattern2 = r'(\d{3})-(\d{4})-(\d{4})'
for phone in phones:
    m = re.search(pattern2, phone)
    if m:
        print(f"区号：{m.group(1)}，号码：{m.group(2)}{m.group(3)}")

# 预编译（提高效率）
phone_re = re.compile(pattern)
print(phone_re.findall(text))

# 常用元字符：. ^ $ * + ? { } [ ] \ | ( )
# 示例：匹配邮箱
email_pattern = r'\b[\w.-]+@[\w.-]+\.\w+\b'
emails = re.findall(email_pattern, "联系我：test@example.com 或 admin@company.cn")
print(emails)
```



### 9、常用标准库示例

- Python 标准库非常庞大，所提供的组件涉及范围十分广泛，使用标准库我们可以让您轻松地完成各种任务

#### os 模块（操作系统交互）



```python
import os

print(os.getcwd())               # 当前工作目录
print(os.listdir('.'))           # 列出当前目录文件
os.makedirs('test_dir', exist_ok=True)   # 创建目录
os.remove('test.txt')            # 删除文件
os.path.exists('test_dir')       # 判断路径是否存在
print(os.path.join('folder', 'file.txt'))  # 路径拼接
```



#### sys 模块（Python 解释器相关）

```python
import sys

print(sys.argv)                  # 命令行参数列表
print(sys.version)               # Python 版本
sys.exit(0)                      # 退出程序
print(sys.path)                  # 模块搜索路径
```



#### datetime 模块（日期时间处理）

```python
from datetime import datetime, timedelta

now = datetime.now()
print(now)                       # 当前时间
print(now.strftime('%Y-%m-%d %H:%M:%S'))   # 格式化

today = datetime(2025, 4, 9)
tomorrow = today + timedelta(days=1)
print(tomorrow)

# 字符串转 datetime
dt = datetime.strptime('2025-04-09', '%Y-%m-%d')
print(dt)
```



#### random 模块（随机数）

```python
import random

print(random.randint(1, 100))    # 随机整数
print(random.choice(['a', 'b', 'c']))   # 随机选择
print(random.sample(range(10), 3))      # 无放回抽样
lst = [1,2,3,4,5]
random.shuffle(lst)              # 打乱顺序
print(lst)
```



#### math 模块（数学函数）

```python
import math

print("圆周率:", math.pi)
print("平方根:", math.sqrt(16))
print("正弦值:", math.sin(math.pi / 2))
print("向上取整:", math.ceil(3.2))
print("向下取整:", math.floor(3.9))
```



#### json 模块（JSON 数据解析）

```python
import json

data = {"name": "张三", "age": 20}
json_str = json.dumps(data, ensure_ascii=False)
print(json_str)                  # {"name": "张三", "age": 20}

obj = json.loads(json_str)
print(obj['name'])

# 读写文件
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
with open('data.json', 'r', encoding='utf-8') as f:
    loaded = json.load(f)
```



### 10、多线程（threading）

- 多线程允许程序同时执行多个任务，适用于 I/O 密集型操作（如网络请求、文件读写）。Python 的全局解释器锁（GIL）限制了 CPU 密集型任务的并行效果。

**核心概念**：
- `Thread`：线程类
- `start()`：启动线程
- `join()`：等待线程结束
- `Lock`：互斥锁，防止数据竞争

```python
import threading
import time

# 基本线程示例
def print_numbers():
    for i in range(5):
        time.sleep(0.5)
        print(f"数字：{i}")

def print_letters():
    for letter in 'ABCDE':
        time.sleep(0.5)
        print(f"字母：{letter}")

# 创建线程
t1 = threading.Thread(target=print_numbers)
t2 = threading.Thread(target=print_letters)

# 启动线程
t1.start()
t2.start()

# 等待线程完成
t1.join()
t2.join()
print("所有线程执行完毕")

# 线程锁（避免共享资源冲突）
counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        with lock:   # 自动获取和释放锁
            counter += 1

threads = []
for _ in range(5):
    t = threading.Thread(target=increment)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(f"最终计数（应为 500000）：{counter}")

# 线程池（concurrent.futures）
from concurrent.futures import ThreadPoolExecutor

def task(n):
    time.sleep(1)
    return n * n

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(task, i) for i in range(5)]
    for f in futures:
        print(f.result())
```



### 11、异步编程（asyncio）

异步编程是单线程并发模型，适用于高 I/O 密集型任务（如网络爬虫、Web 服务器）。通过 `async/await` 语法实现。

**核心概念**：

- `async def`：定义协程函数
- `await`：等待另一个协程完成（不阻塞事件循环）
- `asyncio.run()`：运行入口协程
- `asyncio.gather()`：并发运行多个协程



```python
import asyncio
import time

# 基本协程
async def say_hello():
    print("Hello")
    await asyncio.sleep(1)   # 模拟 I/O 操作，不阻塞
    print("World")

# 运行协程
asyncio.run(say_hello())

# 并发执行多个协程
async def task(name, delay):
    print(f"任务 {name} 开始，等待 {delay} 秒")
    await asyncio.sleep(delay)
    print(f"任务 {name} 完成")
    return f"{name} 的结果"

async def main():
    # 并发运行三个任务
    results = await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 3)
    )
    print(results)

asyncio.run(main())

# 异步上下文管理器（如异步网络请求）
import aiohttp   # 需安装：pip install aiohttp

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# 模拟异步 I/O 与同步代码对比
async def async_demo():
    start = time.time()
    await asyncio.gather(
        asyncio.sleep(1),
        asyncio.sleep(1),
        asyncio.sleep(1)
    )
    print(f"异步总耗时：{time.time() - start:.2f} 秒")

def sync_demo():
    start = time.time()
    time.sleep(1)
    time.sleep(1)
    time.sleep(1)
    print(f"同步总耗时：{time.time() - start:.2f} 秒")

asyncio.run(async_demo())
sync_demo()
# 输出示例：
# 异步总耗时：1.00 秒
# 同步总耗时：3.00 秒
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



## 六、包管理与虚拟环境

### requirements.txt 格式

```bash
# ~= 兼容版本运算符：相当于 >=2.33.1, ==2.33.*
requests ~= 2.33.1

# 固定精确版本
PyMySQL == 1.1.2
```



### 常用命令

```bash
# 创建虚拟环境
python -m venv myenv

# 激活环境（Windows）
myenv\Scripts\activate
# 激活环境（macOS/Linux）
source myenv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 导出当前环境依赖
pip freeze > requirements.txt
```
