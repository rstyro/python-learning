# -*- coding: utf-8 -*-
# Python 正则表达式 re 模块示例
import re

# ====================== 1. 常用匹配函数 ======================
def demo_match_search_findall():
    text = "Hello 123 Python 456 Regex 789"

    # 1. match：从字符串**开头**匹配
    match_res = re.match(r'Hello', text)
    print("match 匹配结果:", match_res.group() if match_res else "无匹配")

    # 2. search：扫描整个字符串，返回**第一个匹配**
    search_res = re.search(r'\d+', text)
    print("search 找到第一个数字:", search_res.group() if search_res else "无匹配")

    # 3. findall：返回所有匹配结果列表
    all_nums = re.findall(r'\d+', text)
    print("findall 所有数字:", all_nums)

    # 4. finditer：返回迭代器，节省内存
    print("finditer 迭代匹配:")
    for item in re.finditer(r'\d+', text):
        print(item.group())


# ====================== 2. 常用元字符 ======================
def demo_pattern():
    text = "abc123DEF_中国@qq.com"

    # \d 数字    \D 非数字
    print("数字:", re.findall(r'\d', text))
    # \w 字母数字下划线    \W 非单词字符
    print("单词字符:", re.findall(r'\w', text))
    # \s 空白符
    # . 任意字符（除换行）
    # ^ 开头  $ 结尾


# ====================== 3. 量词 ======================
def demo_quantifier():
    text = "aaabbb12345"

    # + 至少1次
    print(r"a+ :", re.findall(r'a+', text))
    # * 0次或多次
    print(r"b* :", re.findall(r'b+', text))
    # ? 0次或1次
    # {n} 精确n次  {n,m} n到m次
    print(r"\d{3,5}:", re.findall(r'\d{3,5}', text))


# ====================== 4. 分组 () ======================
def demo_group():
    text = "姓名:张三,年龄:20;姓名:李四,年龄:21"
    # 分组提取姓名和年龄
    pattern = r"姓名:(.*?),年龄:(\d+)"
    results = re.findall(pattern, text)
    print("分组提取结果:", results)

    # group获取分组
    match_obj = re.search(pattern, text)
    if match_obj:
        print("完整匹配:", match_obj.group(0))
        print("姓名:", match_obj.group(1))
        print("年龄:", match_obj.group(2))


# ====================== 5. 贪婪与非贪婪 ======================
def demo_greedy():
    html = "<div>Python</div><div>Regex</div>"

    # 贪婪匹配（默认）：尽可能多匹配
    greedy = re.findall(r"<div>(.*)</div>", html)
    print("贪婪匹配:", greedy)

    # 非贪婪 ?：尽可能少匹配
    non_greedy = re.findall(r"<div>(.*?)</div>", html)
    print("非贪婪匹配:", non_greedy)


# ====================== 6. 替换 sub ======================
def demo_sub():
    text = "123abc456def789"
    # 替换数字为#
    new_text = re.sub(r'\d+', '#', text)
    print("替换后:", new_text)


# ====================== 7. 分割 split ======================
def demo_split():
    text = "a,b;c d|e"
    # 按, ; 空格 | 分割
    res = re.split(r'[,; |]', text)
    print("正则分割:", res)


# ====================== 8. 编译正则（提高效率） ======================
def demo_compile():
    pattern = re.compile(r'\d+')
    text = "1a2b3c"
    print("编译后匹配:", pattern.findall(text))


# ====================== 9. 常用实战案例 ======================
def demo_practical():
    # 1. 手机号验证
    phone = "13812345678"
    phone_pattern = r'^1[3-9]\d{9}$'
    print("手机号是否合法:", bool(re.fullmatch(phone_pattern, phone)))

    # 2. 邮箱验证
    email = "test123@qq.com"
    email_pattern = r'^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$'
    print("邮箱是否合法:", bool(re.fullmatch(email_pattern, email)))

    # 3. 提取URL
    url_text = "访问https://www.baidu.com和http://google.com"
    urls = re.findall(r'https?://\S+', url_text)
    print("提取URL:", urls)


# ====================== 修饰符 ======================
def demo_flags():
    text = "Hello\nhello"
    # re.I 忽略大小写  re.S 让.匹配换行符
    res = re.findall(r'hello', text, re.I)
    print("忽略大小写匹配:", res)


if __name__ == '__main__':
    demo_match_search_findall()
    print("-" * 50)
    demo_pattern()
    print("-" * 50)
    demo_quantifier()
    print("-" * 50)
    demo_group()
    print("-" * 50)
    demo_greedy()
    print("-" * 50)
    demo_sub()
    print("-" * 50)
    demo_split()
    print("-" * 50)
    demo_compile()
    print("-" * 50)
    demo_practical()
    print("-" * 50)
    demo_flags()