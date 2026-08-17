# 请定义一个函数quadratic(a, b, c)，接收3个参数，返回一元二次方程 ax^2 + bx + c = 0 的两个解。
# x = (-b ± 根号b^2-4ac)/2a

import math

def quadratic(a, b, c):
    num =b ** 2 - 4*a*c
    if num<0:
        return "无解"
    sqrtNum = math.sqrt(num)
    x1=(-b+sqrtNum) / (2*a)
    x2=(-b-sqrtNum) / (2*a)
    return x1,x2


# 测试:
print('quadratic(2, 3, 1) =', quadratic(2, 3, 1))
print('quadratic(1, 3, -4) =', quadratic(1, 3, -4))

if quadratic(2, 3, 1) != (-0.5, -1.0):
    print('测试失败')
elif quadratic(1, 3, -4) != (1.0, -4.0):
    print('测试失败')
else:
    print('测试成功')
