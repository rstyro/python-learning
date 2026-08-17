# -*- coding: utf-8 -*-
import redis
from redis.exceptions import RedisError

# ====================== 1. 连接 Redis ======================
def connect_redis():
    # 普通连接
    r = redis.Redis(
        host="localhost",
        port=6379,
        # 替换为你的密码
        password="abcsee2see",
        db=0,
        decode_responses=True  # 自动解码为字符串，不用 bytes
    )
    # 测试连通
    print("ping:", r.ping())
    return r


# ====================== 2. 字符串 String ======================
def demo_string(r):
    print("\n===== String 操作 =====")
    # 设置键值
    r.set("name", "张三")
    # 获取
    print("name:", r.get("name"))

    # 设置过期时间 10秒
    r.set("code", "1234", ex=10)

    # 不存在才设置 nx = not exist
    r.set("name", "李四", nx=True)

    # 数值增减
    r.set("count", 10)
    r.incr("count")    # +1
    r.decr("count")    # -1
    r.incrby("count", 5)  # +5
    print("count:", r.get("count"))


# ====================== 3. 哈希 Hash ======================
def demo_hash(r):
    print("\n===== Hash 操作 =====")
    # hset 哈希表 字段 值
    r.hset("user:1001", "name", "小明")
    r.hset("user:1001", "age", 20)
    r.hset("user:1001", "city", "北京")

    # 获取单个字段
    print("name:", r.hget("user:1001", "name"))

    # 获取所有字段和值
    print("user:1001:", r.hgetall("user:1001"))

    # 获取所有字段 / 所有值
    print("keys:", r.hkeys("user:1001"))
    print("values:", r.hvals("user:1001"))

    # 判断字段是否存在
    print("hexists age:", r.hexists("user:1001", "age"))


# ====================== 4. 列表 List ======================
def demo_list(r):
    print("\n===== List 操作 =====")
    # 右推入
    r.rpush("fruit", "apple", "banana", "orange")
    # 左推入
    r.lpush("fruit", "grape")

    # 获取列表长度
    print("len:", r.llen("fruit"))

    # 获取 [0, -1] 全部
    print("list:", r.lrange("fruit", 0, -1))

    # 右弹出
    r.rpop("fruit")
    # 左弹出
    r.lpop("fruit")

    print("after pop:", r.lrange("fruit", 0, -1))


# ====================== 5. 集合 Set ======================
def demo_set(r):
    print("\n===== Set 操作 =====")
    r.sadd("tag", "python", "java", "c++", "python")

    # 获取所有成员
    print("members:", r.smembers("tag"))

    # 判断是否存在
    print("sismember python:", r.sismember("tag", "python"))

    # 随机移除一个
    r.spop("tag")
    print("after spop:", r.smembers("tag"))


# ====================== 6. 有序集合 ZSet ======================
def demo_zset(r):
    print("\n===== ZSet 有序集合 =====")
    r.zadd("score", {
        "张三": 90,
        "李四": 85,
        "王五": 99
    })

    # 按分数从小到大
    print("zrange:", r.zrange("score", 0, -1, withscores=True))

    # 获取分数
    print("张三分数:", r.zscore("score", "张三"))


# ====================== 7. 通用键操作 ======================
def demo_key(r):
    print("\n===== 通用键操作 =====")
    # 判断键是否存在
    print("exists name:", r.exists("name"))

    # 设置过期
    r.expire("name", 60)

    # 查看剩余过期秒数
    print("ttl name:", r.ttl("name"))

    # 获取所有键
    print("keys *:", r.keys("*"))

    # 删除键
    r.delete("code")


# ====================== 8. 异常处理 ======================
def demo_exception():
    try:
        r = redis.Redis(host="localhost", port=6379, decode_responses=True)
        r.ping()
    except RedisError as e:
        print("Redis 错误:", e)


if __name__ == '__main__':
    r = connect_redis()

    demo_string(r)
    demo_hash(r)
    demo_list(r)
    demo_set(r)
    demo_zset(r)
    demo_key(r)
    demo_exception()