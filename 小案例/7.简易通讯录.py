# 简易通讯录
"""
功能要求：
可以添加联系人（姓名 + 电话）
可以查看所有联系人
可以根据姓名查找联系人
可以退出程序
"""

# 通讯录：列表里存字典，格式 [{"name":"张三", "phone":"13800138000"}, ...]
contacts = [{"name":"张三", "phone":"13800138000"},{"name":"三爷", "phone":"13800138000"}]

def show_menu():
    """显示菜单"""
    print("\n===== 简易通讯录 =====")
    print("1. 添加联系人")
    print("2. 查看所有联系人")
    print("3. 查找联系人")
    print("4. 退出程序")
    print("======================")

def add_contact():
    """添加联系人"""
    name = input("请输入姓名：")
    phone = input("请输入手机号：")
    contacts.append({"name": name, "phone": phone})
    print(f"联系人 {name} 添加成功！")

def show_all():
    """显示所有联系人"""
    if not contacts:
        print("通讯录为空")
        return
    print("\n所有联系人：")
    for i, c in enumerate(contacts, 1):
        print(f"{i}. {c['name']} — {c['phone']}")

def find_contact():
    """按姓名查找联系人"""
    name = input("请输入要查找的姓名：")
    found = False
    for c in contacts:
        if  name in c["name"]:
            print(f"找到：{c['name']} — {c['phone']}")
            found = True
    if not found:
        print("未找到该联系人")

def main():
    while True:
        show_menu()
        choice = input("请选择功能(1-4)：")
        if choice == "1":
            add_contact()
        elif choice == "2":
            show_all()
        elif choice == "3":
            find_contact()
        elif choice == "4":
            print("退出通讯录，再见！")
            break
        else:
            print("输入错误，请输入 1-4")

if __name__ == "__main__":
    main()