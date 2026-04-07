# -*- coding: utf-8 -*-
import json

# ==================== 1. JSON 字符串 → Python对象 (解析) ====================
def json_loads_demo():
    # JSON字符串
    json_str = '''
    {
        "name": "小明",
        "age": 20,
        "is_student": true,
        "hobbies": ["读书", "编程"],
        "info": {"height": 175, "weight": 65}
    }
    '''
    # 解析JSON字符串为字典
    data = json.loads(json_str)
    print("===== json.loads 解析结果 =====")
    print(type(data))
    print("姓名:", data["name"])
    print("爱好:", data["hobbies"][0])
    print("身高:", data["info"]["height"])

# ==================== 2. Python对象 → JSON字符串 (序列化) ====================
def json_dumps_demo():
    # Python字典
    person = {
        "name": "小红",
        "age": 19,
        "hobbies": ["绘画", "音乐"],
        "graduated": False
    }
    # 转换为JSON字符串
    # ensure_ascii=False 正常显示中文
    # indent=4 格式化缩进
    json_str = json.dumps(person, ensure_ascii=False, indent=4)
    print("\n===== json.dumps 序列化 =====")
    print(json_str)

# ==================== 3. 读取JSON文件，解析为Python对象 ====================
def json_load_file():
    # 先创建一个测试JSON文件
    test_data = {"id": 1, "title": "Python学习"}
    with open("test.json", "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    # 读取JSON文件
    with open("test.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print("\n===== json.load 读取文件 =====")
    print(type(data), data)

# ==================== 4. 将Python对象写入JSON文件 ====================
def json_dump_file():
    data = {
        "users": [
            {"name": "张三", "age": 22},
            {"name": "李四", "age": 23}
        ]
    }
    # 写入文件
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("\n===== json.dump 写入文件完成 =====")

# ==================== 5. 类型对应关系 ====================
def json_type_map():
    print("\n===== Python与JSON类型映射 =====")
    print("dict → object")
    print("list, tuple → array")
    print("str → string")
    print("int, float → number")
    print("True → true")
    print("False → false")
    print("None → null")

# ==================== 6. 处理复杂对象 & 异常处理 ====================
class Student:
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            self.name = args[0]
            self.age = 18
        elif len(args) == 2:
            self.name, self.age = args
        # 或者通过 kwargs 灵活接收
        for k, v in kwargs.items():
            setattr(self, k, v)



def complex_json_demo():
    print("\n===== 复杂对象与异常处理 =====")
    # 处理自定义对象，转换为字典
    stu = Student("小王", 21,money=999999,body_age=18)
    json_str = json.dumps(stu.__dict__, ensure_ascii=False)
    print("自定义对象序列化:", json_str)


    # 异常处理：解析非法JSON
    try:
        obj=json.loads('{"name":"rsyro", "money":"100000000000000"}');
        print(f"资产(万元)：{obj['money']}")
        json.loads('{name: test}')
    except json.JSONDecodeError as e:
        print("JSON解析错误:", e)

if __name__ == '__main__':
    json_loads_demo()
    json_dumps_demo()
    json_load_file()
    json_dump_file()
    json_type_map()
    complex_json_demo()