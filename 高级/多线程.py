# -*- coding: utf-8 -*-
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import requests

# 全局变量，用于测试线程安全
count = 0
# 创建锁对象
lock = threading.Lock()

# 1. 基础线程函数
def task(name, delay):
    print(f"线程 {name} 启动，延迟{delay}s执行")
    time.sleep(delay)
    print(f"线程 {name} 执行完成")

# 2. 线程安全的计数任务
def safe_count():
    global count
    # 加锁，保证同一时间只有一个线程修改
    lock.acquire()
    try:
        global count
        count += 1
        print(f"当前计数: {count}, 线程: {threading.current_thread().name}")
        time.sleep(0.1)
    finally:
        # 释放锁
        lock.release()

# 3. 不加锁的不安全计数
def unsafe_count():
    global count
    count += 1
    print(f"当前计数: {count}, 线程: {threading.current_thread().name}")
    time.sleep(0.1)

# 4. IO密集型任务（网络请求，适合多线程）
def fetch_url(url):
    try:
        res = requests.get(url, timeout=3)
        return f"url: {url}, 状态码: {res.status_code}"
    except Exception as e:
        return f"{url} 请求失败: {e}"

# 5. 自定义线程类
class MyThread(threading.Thread):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay

    def run(self):
        print(f"自定义线程 {self.name} 运行")
        time.sleep(self.delay)
        print(f"自定义线程 {self.name} 结束")

if __name__ == '__main__':
    print("========== 1. 基础线程创建 ==========")
    # 创建线程
    t1 = threading.Thread(target=task, args=("线程1", 1))
    t2 = threading.Thread(target=task, args=("线程2", 2))
    # 启动线程
    t1.start()
    t2.start()
    # 主线程等待子线程执行完毕
    t1.join()
    t2.join()

    print("\n========== 2. 自定义线程类 ==========")
    t3 = MyThread("自定义线程", 1)
    t3.start()
    t3.join()

    print("\n========== 3. 线程安全测试 ==========")
    count = 0
    threads = []
    for i in range(5):
        t = threading.Thread(target=safe_count)
        threads.append(t)
        t.start()
    # 等待所有线程结束
    for t in threads:
        t.join()
    print(f"加锁最终计数: {count}")

    print("\n========== 4. 线程池 ==========")
    urls = [
        "https://www.baidu.com",
        "https://httpbin.org/get",
        "https://www.bing.com"
    ]
    # 创建线程池，最大3个线程
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 批量提交任务
        results = executor.map(fetch_url, urls)
        for res in results:
            print(res)

    print("\n========== 主线程执行完毕 ==========")