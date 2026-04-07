# 九九乘法表
def print_multiplication(n):
    for i in range(1, n+1):
        for j in range(1, i+1):
            print(f"{j} * {i} = {i * j}", end="\t")
        print()

print_multiplication(9)