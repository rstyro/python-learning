# -*- coding: utf-8 -*-
# Python文件操作完整示例 file.py
import os

def file_basic_operation():
    # 1. 写入模式w：文件不存在创建，存在则清空覆盖
    with open("test.txt", "w", encoding="utf-8") as f:
        f.write("Hello Python文件操作\n")
        f.write("基础写入内容\n")
        f.writelines(["多行写入1\n", "多行写入2\n"])
    print("==========覆盖写入完成==========")

    # 2. 追加模式a：在文件末尾添加内容，不清空原有数据
    with open("test.txt", "a", encoding="utf-8") as f:
        f.write("这是追加的文本内容\n")
    print("==========追加写入完成==========")

    # 3. 读取模式r：读取文件全部内容
    print("\n==========读取全部内容==========")
    with open("test.txt", "r", encoding="utf-8") as f:
        content = f.read()
        print(content)

    # 4. 按行读取readline
    print("\n==========readline单行读取==========")
    with open("test.txt", "r", encoding="utf-8") as f:
        line = f.readline()
        while line:
            print(line.strip())
            line = f.readline()

    # 5. 读取所有行返回列表readlines
    print("\n==========readlines读取==========")
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            print(f"第{index + 1}行：{line.strip()}")

    # 6. 迭代读取，适合大文件
    print("\n==========迭代读取大文件==========")
    with open("test.txt", "r", encoding="utf-8") as f:
        for line in f:
            print(line.strip())

    # 7. 读写模式r+，文件需存在
    # + 打开一个文件进行更新(可读可写)。
    print("\n==========r+读写模式==========")
    with open("test.txt", "r+", encoding="utf-8") as f:
        f.read()
        f.write("\nr+模式新增内容\n")

def binary_file_operation():
    # 8. 二进制文件读写，适用于图片、视频等
    print("\n==========二进制文件操作==========")
    try:
        # b 二进制模式
        # rb+ 以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。一般用于非文本文件如图片等。
        with open("source.bin", "rb") as f_read:
            data = f_read.read()
        # 二进制写入复制文件
        with open("copy.bin", "wb") as f_write:
            f_write.write(data)
        print("二进制文件复制完成")
    except FileNotFoundError:
        print("未找到source.bin，跳过二进制复制演示")

def file_folder_manage():
    # 9. 文件与文件夹管理
    print("\n==========文件文件夹操作==========")
    # 判断文件是否存在
    if os.path.exists("test.txt"):
        print("test.txt文件存在")
        # 获取文件大小
        print(f"文件大小：{os.path.getsize('test.txt')}字节")

    # 创建文件夹
    if not os.path.exists("demo_folder"):
        os.mkdir("demo_folder")
        print("文件夹demo_folder创建成功")

    # 查看当前目录文件
    print("当前目录文件：", os.listdir("./"))

    # 安全重命名
    if os.path.exists("test.txt"):
        os.rename("test.txt", "rename_test.txt")
        print("文件重命名完成")

    # 删除文件
    os.remove("rename_test.txt")
    # 删除空文件夹
    os.rmdir("demo_folder")

def exception_handle_demo():
    # 10. 文件操作异常处理
    print("\n==========异常处理演示==========")
    try:
        with open("not_exist.txt", "r", encoding="utf-8") as f:
            f.read()
    except FileNotFoundError:
        print("捕获异常：文件不存在")
    except PermissionError:
        print("捕获异常：无文件操作权限")
    except Exception as e:
        print(f"其他异常：{e}")

if __name__ == "__main__":
    file_basic_operation()
    binary_file_operation()
    file_folder_manage()
    exception_handle_demo()

# 获取系统环境变量,如果环境变量不存在，返回 None
home_directory = os.getenv("PYTHON_HOME")
print("HOME 目录:", home_directory)
