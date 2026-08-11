# -*- coding: utf-8 -*-

# argparse 最小实战：在终端里直接跑这个脚本试试
#
# 用法示例：
#   python 11.argparse_mini_demo.py                          # 默认输出
#   python 11.argparse_mini_demo.py --help                    # 查看帮助
#   python 11.argparse_mini_demo.py --name Tom --count 5      # 输出 5 次
#   python 11.argparse_mini_demo.py -n Jerry -c 3             # 短参数写法

import argparse

# 1. 创建解析器
parser = argparse.ArgumentParser(description="一个最小的 argparse 示例")

# 2. 定义参数（这就是你"声明"你要收什么命令行参数）
parser.add_argument("--name", "-n", default="World", help="你的名字")
parser.add_argument("--count", "-c", type=int, default=3, help="输出次数")

# 3. 解析命令行参数（没有传列表！直接读 sys.argv = 你敲的命令）
args = parser.parse_args()

# 4. 用 args.xxx 取值
for i in range(args.count):
    print(f"{i+1}: Hello, {args.name}!")
