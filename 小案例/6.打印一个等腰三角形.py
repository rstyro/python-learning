# 用循环打印一个等腰三角形（5 行）

def test(n=5):
    for i in range(1, n+1):  # 从1开始，到n结束
        # 每行星号数是 2*i-1
        print(("*" * (2*i-1)).center(2*n-1," "))

if __name__ == "__main__":
    test(5)