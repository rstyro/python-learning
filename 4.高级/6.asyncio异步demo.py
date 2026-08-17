# -*- coding: utf-8 -*-
import asyncio
import time

# ==========================================
# 1. 基础异步函数定义
# ==========================================
async def hello(name):
    print(f"Hello {name}")
    return f"结果：{name}"

# ==========================================
# 2. 异步等待 await
# ==========================================
async def async_wait(name, delay):
    print(f"[{name}] 启动，等待 {delay}s")
    await asyncio.sleep(delay)  # 异步等待（不阻塞CPU）
    print(f"[{name}] 执行完毕")
    return name

# ==========================================
# 3. 创建任务（并发核心）
# ==========================================
async def create_task_demo():
    print("===== 任务并发执行 =====")

    # 创建任务 → 立刻加入事件循环
    task1 = asyncio.create_task(async_wait("任务1", 1))
    task2 = asyncio.create_task(async_wait("任务2", 1))

    # 等待任务完成
    result1 = await task1
    result2 = await task2

    print("任务结果：", result1, result2)

# ==========================================
# 4. gather 批量并发
# ==========================================
async def gather_demo():
    print("\n===== gather 批量并发 =====")

    results = await asyncio.gather(
        async_wait("A", 1),
        async_wait("B", 1),
        async_wait("C", 1)
    )

    print("gather 全部结果：", results)

# ==========================================
# 5. wait 控制任务等待方式
# ==========================================
async def wait_demo():
    print("\n===== wait 灵活控制 =====")

    tasks = [
        asyncio.create_task(async_wait("wait-1", 1)),
        asyncio.create_task(async_wait("wait-2", 2)),
    ]

    # 等待所有完成
    done, pending = await asyncio.wait(tasks)
    for t in done:
        print("wait 完成结果：", t.result())

# ==========================================
# 6. 超时控制
# ==========================================
async def timeout_demo():
    print("\n===== 超时控制 =====")
    try:
        # 最多等 1 秒
        await asyncio.wait_for(async_wait("慢任务", 2), timeout=1)
    except asyncio.TimeoutError:
        print("任务超时！")

# ==========================================
# 7. 获取任务返回值
# ==========================================
async def task_result_demo():
    print("\n===== 获取任务结果 =====")
    task = asyncio.create_task(hello("测试返回值"))
    await task
    print("返回结果：", task.result())

# ==========================================
# 8. 任务取消
# ==========================================
async def cancel_demo():
    print("\n===== 任务取消 =====")
    task = asyncio.create_task(async_wait("可取消任务", 3))

    await asyncio.sleep(1)
    task.cancel()  # 取消任务

    try:
        await task
    except asyncio.CancelledError:
        print("任务已取消！")

# ==========================================
# 9. 异步循环事件 loop
# ==========================================
async def loop_demo():
    print("\n===== 异步循环演示 =====")
    for i in range(3):
        await asyncio.sleep(0.5)
        print(f"循环 {i}")

# ==========================================
# 10. 异步生成器
# ==========================================
async def async_generator():
    for i in range(3):
        await asyncio.sleep(0.3)
        yield i

async def gen_demo():
    print("\n===== 异步生成器 =====")
    async for num in async_generator():
        print("异步生成：", num)

# ==========================================
# 11. 异步上下文管理器
# ==========================================
class AsyncContext:
    async def __aenter__(self):
        print("进入异步上下文")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print("退出异步上下文")

async def context_demo():
    print("\n===== 异步上下文管理器 =====")
    async with AsyncContext():
        print("执行中...")

# ==========================================
# 12. 当前任务、事件循环信息
# ==========================================
async def info_demo():
    print("\n===== 任务信息 =====")
    task = asyncio.current_task()
    print("当前任务：", task.get_name())
    print("是否完成：", task.done())

# ==========================================
# 13. 异步队列（生产者-消费者）
# ==========================================
import random

async def producer(queue, name, count):
    """生产者：生产数据放入队列"""
    for i in range(count):
        item = f"{name}-{i}"
        await asyncio.sleep(random.uniform(0.2, 0.5))  # 模拟生产耗时
        await queue.put(item)
        print(f"[生产者 {name}] 生产: {item}")
    print(f"[生产者 {name}] 生产结束")

async def consumer(queue, name):
    """消费者：从队列取出数据"""
    while True:
        item = await queue.get()
        if item is None:  # 结束信号
            queue.task_done()
            break
        print(f"[消费者 {name}] 消费: {item}")
        await asyncio.sleep(random.uniform(0.1, 0.3))  # 模拟处理耗时
        queue.task_done()
    print(f"[消费者 {name}] 退出")

async def queue_demo():
    print("\n===== 异步队列 (生产者-消费者) =====")
    queue = asyncio.Queue(maxsize=5)

    # 创建生产者和消费者任务
    producers = [asyncio.create_task(producer(queue, f"P{i}", 3)) for i in range(2)]
    consumers = [asyncio.create_task(consumer(queue, f"C{i}")) for i in range(3)]

    # 等待所有生产者完成
    await asyncio.gather(*producers)

    # 向队列发送结束信号（每个消费者一个 None）
    for _ in consumers:
        await queue.put(None)

    # 等待所有消费者处理完毕
    await asyncio.gather(*consumers)
    await queue.join()  # 确保队列真正清空
    print("队列演示结束")

# ==========================================
# 14. 限制并发（信号量 Semaphore）
# ==========================================
async def limited_task(sem, task_id, delay):
    async with sem:  # 获取信号量，限制同时只有 2 个任务执行
        print(f"[限流任务 {task_id}] 开始，将耗时 {delay}s")
        await asyncio.sleep(delay)
        print(f"[限流任务 {task_id}] 完成")
        return task_id

async def semaphore_demo():
    print("\n===== 信号量限制并发 =====")
    sem = asyncio.Semaphore(2)  # 最多同时执行 2 个任务
    tasks = [limited_task(sem, i, random.uniform(0.5, 1.5)) for i in range(5)]
    results = await asyncio.gather(*tasks)
    print("所有任务结果:", results)

# ==========================================
# 15. as_completed：按完成顺序处理
# ==========================================
async def as_completed_demo():
    print("\n===== as_completed 按完成顺序 =====")
    async def work(name, delay):
        print(f"任务 {name} 开始，将耗时 {delay}s")
        await asyncio.sleep(delay)
        return name

    tasks = [work(f"任务{i}", random.uniform(0.2, 1.0)) for i in range(4)]
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"完成顺序: {result}")

# ==========================================
# 16. 在异步中运行同步阻塞代码（线程池/进程池）
# ==========================================
def sync_blocking(name, seconds):
    """模拟一个阻塞的同步函数（如文件IO、CPU计算）"""
    time.sleep(seconds)  # 同步阻塞
    return f"阻塞函数 {name} 完成，耗时 {seconds}s"

async def run_in_executor_demo():
    print("\n===== 执行同步阻塞代码 =====")
    loop = asyncio.get_running_loop()

    # 使用默认的线程池执行器
    result = await loop.run_in_executor(None, sync_blocking, "线程任务", 1)
    print(result)

    # 并发执行多个阻塞任务
    tasks = [
        loop.run_in_executor(None, sync_blocking, f"并发{i}", 0.5)
        for i in range(3)
    ]
    results = await asyncio.gather(*tasks)
    print("多个阻塞任务结果:", results)

    # 如果需要 CPU 密集型，可使用进程池（需创建 ProcessPoolExecutor）
    # with concurrent.futures.ProcessPoolExecutor() as pool:
    #     result = await loop.run_in_executor(pool, sync_blocking, "CPU任务", 1)

# ==========================================
# 17. 任务同步：Event（事件）
# ==========================================
async def waiter(event, name):
    print(f"[等待者 {name}] 等待事件...")
    await event.wait()  # 阻塞直到 event.set()
    print(f"[等待者 {name}] 收到事件，继续执行")

async def setter(event):
    await asyncio.sleep(1)
    print("[设置者] 触发事件")
    event.set()

async def event_demo():
    print("\n===== 事件 Event 同步 =====")
    event = asyncio.Event()
    waiters = [asyncio.create_task(waiter(event, i)) for i in range(3)]
    setter_task = asyncio.create_task(setter(event))

    await asyncio.gather(*waiters, setter_task)

# ==========================================
# 18. 任务同步：Lock（互斥锁）
# ==========================================
shared_resource = 0

async def increment(lock, name):
    global shared_resource
    async with lock:
        print(f"[{name}] 获得锁，当前值: {shared_resource}")
        value = shared_resource
        await asyncio.sleep(0.1)  # 模拟一些异步操作
        shared_resource = value + 1
        print(f"[{name}] 更新为: {shared_resource}")

async def lock_demo():
    print("\n===== 互斥锁 Lock =====")
    lock = asyncio.Lock()
    tasks = [asyncio.create_task(increment(lock, i)) for i in range(5)]
    await asyncio.gather(*tasks)
    print(f"最终 shared_resource = {shared_resource}")

# ==========================================
# 19. shield：保护任务不被取消
# ==========================================
async def important_work():
    print("重要工作开始，不能被取消")
    await asyncio.sleep(2)
    print("重要工作完成")
    return "关键结果"

async def shield_demo():
    print("\n===== shield 保护任务 =====")
    task = asyncio.create_task(important_work())
    # 用 shield 包装，即使外层超时也不会取消内部任务
    shielded = asyncio.shield(task)
    try:
        result = await asyncio.wait_for(shielded, timeout=1)
    except asyncio.TimeoutError:
        print("外层超时，但内部任务仍在运行")
        result = await task  # 仍然能拿到结果
    print(f"最终结果: {result}")

# ==========================================
# 20. gather 的 return_exceptions 用法
# ==========================================
async def failing_task(name, fail):
    if fail:
        raise ValueError(f"{name} 失败")
    return f"{name} 成功"

async def gather_exceptions_demo():
    print("\n===== gather 异常处理 =====")
    tasks = [
        failing_task("A", False),
        failing_task("B", True),
        failing_task("C", False)
    ]
    # return_exceptions=True 让 gather 返回异常对象而不是抛出
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for r in results:
        if isinstance(r, Exception):
            print(f"捕获异常: {r}")
        else:
            print(f"成功结果: {r}")

# ==========================================
# 21. 当前任务与所有任务信息
# ==========================================
async def all_tasks_info():
    print("\n===== 查看所有活动任务 =====")
    current = asyncio.current_task()
    print(f"当前任务: {current.get_name()}")
    all_tasks = asyncio.all_tasks()
    print(f"活动任务数量: {len(all_tasks)}")
    for t in all_tasks:
        print(f"  - {t.get_name()}: done={t.done()}, cancelled={t.cancelled()}")


# ==========================================
# 主函数：运行所有示例
# ==========================================
async def main():
    await hello("asyncio")
    await create_task_demo()
    await gather_demo()
    await wait_demo()
    await timeout_demo()
    await task_result_demo()
    await cancel_demo()
    await loop_demo()
    await gen_demo()
    await context_demo()
    await info_demo()

    await queue_demo()
    await semaphore_demo()
    await as_completed_demo()
    await run_in_executor_demo()
    await event_demo()
    await lock_demo()
    await shield_demo()
    await gather_exceptions_demo()
    await all_tasks_info()

if __name__ == '__main__':
    asyncio.run(main())