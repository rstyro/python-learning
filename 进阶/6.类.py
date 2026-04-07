# -*- coding: utf-8 -*-

# 1. 基础类定义与实例化
class Person:
    # 构造方法：创建对象时自动执行
    def __init__(self, name, age):
        # 实例属性
        self.name = name
        self.age = age

    # 实例方法
    def introduce(self):
        return f"我叫{self.name}，今年{self.age}岁"

    def eat(self, food):
        return f"{self.name}正在吃{food}"


# 2. 继承：子类继承父类
class Student(Person):
    def __init__(self, name, age, student_id):
        # 调用父类构造方法
        super().__init__(name, age)
        self.student_id = student_id

    # 方法重写
    def introduce(self):
        return f"我是学生{self.name}，学号{self.student_id}"

    # 子类独有方法
    def study(self, subject):
        return f"{self.name}学习{subject}"


# 3. 多继承
class Teacher(Person):
    def teach(self):
        return f"{self.name}在授课"

class Assistant(Student, Teacher):
    pass


# 4. 类属性、类方法、静态方法
class MathUtil:
    # 类属性
    pi = 3.14159

    # 类方法
    @classmethod
    def circle_area(cls, r):
        return cls.pi * r ** 2

    # 静态方法
    @staticmethod
    def add(a, b):
        return a + b


# 5. 私有属性与私有方法（封装）
class BankCard:
    def __init__(self, card_id, money):
        self.card_id = card_id
        # 私有属性，两个下划线开头，声明该属性为私有，不能在类的外部被使用或直接访问
        self.__money = money

    # 私有方法
    def __check_money(self):
        return self.__money >= 0

    # 公开接口
    def save_money(self, num):
        if num > 0:
            self.__money += num

    def get_money(self):
        return self.__money


# 6. property装饰器：将方法伪装成属性
class Book:
    def __init__(self, title):
        self.__title = title

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, new_title):
        if len(new_title) > 0:
            self.__title = new_title


# 7. 魔术方法（特殊方法）
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 打印对象时显示
    def __str__(self):
        return f"Point({self.x}, {self.y})"

    # 对象相加
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    # 获取长度
    def __len__(self):
        return abs(self.x) + abs(self.y)


# 8. 抽象类（需导入abc模块）
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "汪汪汪"

class Cat(Animal):
    def speak(self):
        return "喵喵喵"


# 9. 多态
def make_speak(animal: Animal):
    print(animal.speak())


# 主程序测试
if __name__ == '__main__':
    print("=====1. 基础类测试=====")
    p = Person("张三", 20)
    print(p.introduce())
    print(p.eat("苹果"))

    print("\n=====2. 继承测试=====")
    stu = Student("李四", 18, "2025001")
    print(stu.introduce())
    print(stu.study("Python"))

    print("\n=====3. 多继承测试=====")
    assistant = Assistant("小王", 22, "2025002")
    print(assistant.study("高数"))
    print(assistant.teach())

    print("\n=====4. 类方法静态方法测试=====")
    print(MathUtil.pi)
    print(MathUtil.circle_area(5))
    print(MathUtil.add(10, 20))

    print("\n=====5. 封装测试=====")
    card = BankCard("6228xxxx", 1000)
    card.save_money(500)
    print(card.get_money())

    print("\n=====6. property测试=====")
    book = Book("Python入门")
    print(book.title)
    book.title = "Python进阶"
    print(book.title)

    print("\n=====7. 魔术方法测试=====")
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    print(p1 + p2)
    print(len(p1))

    print("\n=====8. 抽象类与多态测试=====")
    dog = Dog()
    cat = Cat()
    make_speak(dog)
    make_speak(cat)