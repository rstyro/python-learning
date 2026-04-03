#!/usr/bin/python3

# 字符串基础用法大全
var1 = 'Hello World!'
var2 = "Python"
var3 = "123456"
var4 = "  python test  "

# ============== 1. 访问字符串中的字符（索引）==============
# 索引从 0 开始
print("1. 索引取值")
print("var1[0]:    ", var1[0])    # 取第1个字符
print("var1[-1]:   ", var1[-1])   # 取最后1个字符
print("var2[0]:    ", var2[0])

# ============== 2. 字符串切片（截取子串）==============
print("\n2. 字符串切片")
print("var2[1:5]:  ", var2[1:5])  # 从索引1取到4（不包含5）
print("var2[2:]:   ", var2[2:])   # 从索引2取到末尾
print("var2[:4]:   ", var2[:4])   # 从开头取到索引3
print("var2[::2]:  ", var2[::2])  # 步长为2，隔一个取一个
print("var2[::-1]:  ",var2[::-1])  # 反转字符串，结果：nohtyP

# ============== 3. 字符串拼接 + 重复 * ==============
print("\n3. 拼接与重复")
print(var1 + " " + var2)          # 拼接：+
print(var2 * 3)                   # 重复：*

# ============== 4. 成员运算符 in / not in ==============
print("\n4. 成员判断")
print("World" in var1)           # 存在返回 True
print("Java" in var1)            # 不存在返回 False

# ============== 5. 字符串格式化（旧式 %）==============
print("\n5. 旧式格式化 %")
print("我叫 %s 今年 %d 岁!" % ('小明', 10))
print("圆周率：%.2f" % 3.14159)   # 保留2位小数

# ============== 6. 字符串格式化（format 推荐）==============
print("\n6. 新式格式化 {}")
print("姓名：{}，年龄：{}".format("小红", 12))
print("姓名：{name}，年龄：{age}".format(name="小李", age=15))

# ============== 7. f-string 格式化（Python3.6+ 最佳）==============
print("\n7. f-string 格式化")
name = "小王"
age = 18
print(f"姓名：{name}，年龄：{age}")

# ============== 8. 常用字符串方法 ==============


# 1. 大小写转换
print("\n8-1. 大小写转换")
print(var1.upper())  # 全大写
print(var1.lower())  # 全小写
print(var1.title())  # 首字母大写
print(var1.swapcase()) # 大小写互换

# 2. 去除空白字符
print("\n8-2. 去除空白")
print(var4.strip())   # 去除首尾空格
print(var4.lstrip())  # 去除左侧空格
print(var4.rstrip())  # 去除右侧空格

# 3. 查找与替换
print("\n8-3. 查找替换")
print(var1.find('World')) # 查找子串索引，不存在返回-1
print(var1.index('e'))    # 查找索引，不存在报错
print(var1.replace('World', 'Python')) # 替换字符

# 4. 分割与拼接
print("\n8-4. 分割拼接")
print(var1.split(' ')) # 按空格分割为列表
print('-'.join(['a','b','c'])) # 拼接列表为字符串

# 5. 统计字符出现次数
print("\n8-5. count() 统计次数")
print(var1.count('l'))

# 6. 判断字符串类型
print("\n8-6. 类型判断")
print(var3.isdigit())   # 是否全为数字
print(var2.isalpha())   # 是否全为字母
print(var2.isalnum())   # 是否为字母+数字
print(var1.isspace())   # 是否全为空白字符
print(var2.istitle())   # 是否首字母大写

# 7. 填充对齐
print("\n8-7. 对齐填充")
print(var2.center(10, '*')) # 居中填充
print(var2.ljust(10, '-'))  # 左对齐
print(var2.rjust(10, '='))  # 右对齐

# 8. 判断开头结尾
print("\n8-8. 首尾判断")
print(var1.startswith('Hello')) # 是否以Hello开头
print(var1.endswith('!')) # 是否以!结尾

# 9. len()：获取字符串长度
print("\n8-9. len() 字符串长度")
print(len(var1))
print(len(var2))