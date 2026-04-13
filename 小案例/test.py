lit=[1, 2, 2, 3, 4, 4, 5]
new_lst=[]

for i in lit:
    if i not in new_lst:
        new_lst.append(i)

print("新数组：",new_lst)


def find_max_min():
    min_num=max_num=None
    lst=[]
    for i in range(0,5):
        num = float(input("请输入数字："))
        if i==0:
            min_num=max_num=num
        lst.append(num)
        if num>max_num:
            max_num=num
        if num<min_num:
            min_num=num
    print("数组为：",lst)
    print(f"最大值为:{max_num},最小值为：{min_num}")

find_max_min()