# 版本信息
__version__ = "1.0.0"
__author__ = "rstyro"

print("初始化 my_package")


# 导出主要的类和函数，隐藏内部实现
from .consts import MONEY
from .date_util import format_date_time

# 控制 from myutils import * 的内容
__all__=['consts','date_util','MONEY','format_date_time']