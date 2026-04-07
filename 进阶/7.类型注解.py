# -*- coding: utf-8 -*-

from typing import (
    List, Tuple, Dict, Set,
    Optional, Union, Any,
    Callable, Iterable, Generator,
    TypeVar, Generic
)


# 1. 基础变量类型注解
name: str = "张三"
age: int = 20
height: float = 1.75
is_student: bool = True


# 2. 函数参数与返回值注解
def add(a: int, b: int) -> int:
    return a + b


def greet(name: str) -> None:
    print(f"你好, {name}")


# 3. 容器类型注解（旧版写法，Python3.9+ 可直接用 list/dict）
nums: List[int] = [1, 2, 3]
person: Tuple[str, int, float] = ("李四", 21, 1.80)
student_dict: Dict[str, str] = {"name": "小明", "id": "1001"}
unique_nums: Set[int] = {1, 2, 2, 3}


# 4. Optional：可以是类型 或 None
def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "admin"
    return None


# 5. Union：多种可能类型
def format_data(data: Union[int, str]) -> str:
    return str(data)


# 6. Any：任意类型（不推荐滥用）
def anything(value: Any) -> Any:
    return value


# 7. 可调用对象 Callable
def run_func(func: Callable[[int, int], int], x: int, y: int) -> int:
    return func(x, y)


# 8. 生成器 Generator[返回类型, 发送类型, 终止类型]
def count_gen(n: int) -> Generator[int, None, None]:
    for i in range(n):
        yield i


# 9. 类的类型注解
class Person:
    # 实例属性注解
    name: str
    age: int

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def introduce(self) -> str:
        return f"{self.name}, {self.age}岁"


# 10. 自引用类型（类内部使用自身类型）
class Node:
    def __init__(self, value: int) -> None:
        self.value: int = value
        self.next: Optional["Node"] = None


# 11. TypeVar + 泛型
T = TypeVar("T")

class Box(Generic[T]):
    def __init__(self, content: T) -> None:
        self.content: T = content

    def get(self) -> T:
        return self.content


# 12. 可迭代对象 Iterable
def print_items(items: Iterable[int]) -> None:
    for item in items:
        print(item)


# 13. Python 3.9+ 原生标准写法
new_list: list[int] = [1, 2, 3]
new_dict: dict[str, float] = {"a": 1.1, "b": 2.2}


# ------------------- 测试 -------------------
if __name__ == '__main__':
    print(add(10, 20))
    greet("Python")

    user = find_user(1)
    print(user)

    print(run_func(add, 5, 3))

    p = Person("小红", 22)
    print(p.introduce())

    int_box = Box(123)
    print(int_box.get())

    print_items([1, 2, 3])