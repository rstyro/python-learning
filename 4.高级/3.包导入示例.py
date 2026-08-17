# 1、导入模块
# import utils.date_util
# print(utils.date_util.format_now())


# 2、导入相对路径，如果本文件移动位置了，容易报错
# from utils import date_util
# print(date_util.format_now())

# 3、导入绝对路径，移动此文件不影响
# from 高级.utils import date_util
# print(date_util.format_now())


# 4、注意:如果通过 from myutils import * 导入包下的所有模块,需要在 __init__.py 文件中添加 __all__=['你要导入的模块名']
from myutils import *
print(date_util.format_now())
print(consts.NAME)

# 在 __init__.py 隐藏内部实现,直接可以调用
print(MONEY)
print(format_date_time())
