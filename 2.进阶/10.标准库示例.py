# -*- coding: utf-8 -*-

# Python 常用标准库完整示例

import os
import sys
import math
import random
import datetime
import time
import json
import pickle
import collections
import itertools
import hashlib
import base64
from pathlib import Path

# ====================== 1. os 文件/系统操作 ======================
def demo_os():
    print("===== os 模块 =====")
    print("当前目录:", os.getcwd())
    print("系统名称:", os.name)
    # 拼接路径
    path = os.path.join(os.getcwd(), "test.txt")
    print("路径拼接:", path)
    print("文件是否存在:", os.path.exists(path))


# ====================== 2. pathlib 面向对象路径操作 ======================
def demo_pathlib():
    print("\n===== pathlib 模块 =====")
    p = Path(".")
    print("当前目录文件:", list(p.iterdir()))
    file = p / "test.txt"
    print("路径是否存在:", file.exists())


# ====================== 3. sys 解释器交互 ======================
def demo_sys():
    print("\n===== sys 模块 =====")
    print("Python 路径:", sys.path[:2])
    print("命令行参数:", sys.argv)
    print("版本信息:", sys.version)


# ====================== 4. math 数学运算 ======================
def demo_math():
    print("\n===== math 模块 =====")
    print("圆周率:", math.pi)
    print("平方根:", math.sqrt(16))
    print("正弦值:", math.sin(math.pi / 2))
    print("向上取整:", math.ceil(3.2))
    print("向下取整:", math.floor(3.9))


# ====================== 5. random 随机数 ======================
def demo_random():
    print("\n===== random 模块 =====")
    print("0-1随机数:", random.random())
    print("1-100整数:", random.randint(1, 100))
    print("随机选择:", random.choice([1,2,3,4]))
    lst = [1,2,3]
    random.shuffle(lst)
    print("打乱列表:", lst)


# ====================== 6. datetime 时间日期 ======================
def demo_datetime():
    print("\n===== datetime 模块 =====")
    now = datetime.datetime.now()
    print("当前时间:", now)
    print("格式化时间:", now.strftime("%Y-%m-%d %H:%M:%S"))
    delta = datetime.timedelta(days=7)
    print("7天后:", now + delta)


# ====================== 7. time 时间戳/休眠 ======================
def demo_time():
    print("\n===== time 模块 =====")
    print("时间戳:", time.time())
    print("本地时间:", time.localtime())


# ====================== 8. json 序列化 ======================
def demo_json():
    print("\n===== json 模块 =====")
    data = {"name": "Tom", "age": 20}
    # 字典转json字符串
    json_str = json.dumps(data, ensure_ascii=False, indent=4)
    print("json字符串:\n", json_str)
    # 转回字典
    print("转回字典:", json.loads(json_str))


# ====================== 9. pickle 二进制序列化 ======================
def demo_pickle():
    print("\n===== pickle 模块 =====")
    data = {"a": 1, "b": [2,3]}
    b_data = pickle.dumps(data)
    print("pickle序列化长度:", len(b_data))
    print("反序列化:", pickle.loads(b_data))


# ====================== 10. collections 容器 ======================
def demo_collections():
    print("\n===== collections 模块 =====")
    # 计数器
    cnt = collections.Counter("aabbbcccc")
    print("字符计数:", cnt)
    # 有序字典
    od = collections.OrderedDict()
    od["x"] = 1
    od["y"] = 2
    # 命名元组
    Point = collections.namedtuple("Point", ["x", "y"])
    p = Point(10, 20)
    print("命名元组:", p.x, p.y)


# ====================== 11. itertools 迭代工具 ======================
def demo_itertools():
    print("\n===== itertools 模块 =====")
    print("排列:", list(itertools.permutations([1,2], 2)))
    print("组合:", list(itertools.combinations([1,2,3], 2)))


# ====================== 12. hashlib 加密 ======================
def demo_hashlib():
    print("\n===== hashlib 模块 =====")
    md5 = hashlib.md5()
    md5.update("hello".encode("utf-8"))
    print("MD5加密:", md5.hexdigest())


# ====================== 13. base64 编码 ======================
def demo_base64():
    print("\n===== base64 模块 =====")
    b = "测试文本".encode("utf-8")
    enc = base64.b64encode(b)
    print("base64编码:", enc)
    print("解码:", base64.b64decode(enc).decode())


# ====================== 主运行 ======================
if __name__ == '__main__':
    demo_os()
    demo_pathlib()
    demo_sys()
    demo_math()
    demo_random()
    demo_datetime()
    demo_time()
    demo_json()
    demo_pickle()
    demo_collections()
    demo_itertools()
    demo_hashlib()
    demo_base64()