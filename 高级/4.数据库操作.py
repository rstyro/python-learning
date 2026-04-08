# -*- coding: utf-8 -*-
import sqlite3
import pymysql
import os
from pymysql import Error

# SQLite 数据库文件地址
SQLITE_DB_PATH='./db/test.db'

# 文件目录不存在则新建目录
def ensure_directory(file_path):
    dir_path = os.path.dirname(file_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)

# ==============================================
# 1. SQLite3 操作（内置数据库，无需安装）
# ==============================================
def sqlite_demo():
    print("===== SQLite3 操作 =====")
    ensure_directory(SQLITE_DB_PATH)
    # 1. 连接数据库（不存在则自动创建）
    conn = sqlite3.connect(SQLITE_DB_PATH)
    # 获取游标
    cursor = conn.cursor()

    # 2. 创建表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            address TEXT
        )
    ''')

    # 3. 插入单条数据
    cursor.execute("INSERT INTO user (name, age, address) VALUES (?, ?, ?)",
                   ("张三", 20, "北京"))

    # 4. 批量插入
    user_list = [
        ("李四", 21, "上海"),
        ("王五", 22, "广州"),
        ("赵六", 23, "深圳")
    ]
    cursor.executemany("INSERT INTO user (name, age, address) VALUES (?, ?, ?)", user_list)

    # 提交事务
    conn.commit()

    # 5. 查询数据
    cursor.execute("SELECT * FROM user")
    all_users = cursor.fetchall()
    print("所有用户：", all_users)

    # 查询单条
    cursor.execute("SELECT * FROM user WHERE name=?", ("张三",))
    user = cursor.fetchone()
    print("查询张三：", user)

    # 6. 更新数据
    cursor.execute("UPDATE user SET age=? WHERE name=?", (25, "张三"))
    conn.commit()

    # 7. 删除数据
    cursor.execute("DELETE FROM user WHERE age=?", (23,))
    conn.commit()

    # 关闭连接
    cursor.close()
    conn.close()


# ==============================================
# 2. MySQL 数据库操作
# ==============================================
def mysql_demo():
    print("\n===== MySQL 操作 =====")
    # 数据库连接配置（自行修改）
    config = {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "test",
        "charset": "utf8mb4"
    }

    conn = None
    try:
        # 连接 MySQL
        conn = pymysql.connect(**config)
        cursor = conn.cursor()

        # 创建表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(50) NOT NULL COMMENT '名称',
                age INT COMMENT '年龄',
                address VARCHAR(100) COMMENT '地址'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''')

        # 插入数据
        cursor.execute(
            "INSERT INTO user (name, age, address) VALUES (%s, %s, %s)",
            ("小明", 18, "杭州")
        )

        # 批量插入
        users = [("小红", 19, "成都"), ("小亮", 20, "重庆")]
        cursor.executemany(
            "INSERT INTO user (name, age, address) VALUES (%s, %s, %s)",
            users
        )
        conn.commit()

        # 查询
        cursor.execute("SELECT * FROM user")
        print("MySQL查询结果：", cursor.fetchall())

        cursor.close()

    except Error as e:
        print("MySQL错误：", e)
        if conn:
            conn.rollback()  # 回滚事务
    finally:
        if conn:
            conn.close()


# ==============================================
# 3. 上下文管理器 with 自动关闭连接
# ==============================================
def sqlite_with_demo():
    print("\n===== with 语句自动管理连接 =====")
    with sqlite3.connect(SQLITE_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        print(cursor.fetchall())
    # 自动关闭连接


if __name__ == "__main__":
    # 运行 SQLite 演示（直接可跑）
    sqlite_demo()
    sqlite_with_demo()

    # 运行 MySQL（需你本地有 MySQL 服务）
    mysql_demo()