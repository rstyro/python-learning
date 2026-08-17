# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
# 需要安装，
import requests


# =============== 1. 使用内置库 urllib 发送 GET 请求 ===============
def urllib_get_demo():
    print("===== urllib GET =====")
    url = "https://httpbin.org/get"
    # 构造参数
    params = {"name": "python", "age": 20}
    # 参数编码
    param_str = urllib.parse.urlencode(params)
    full_url = f"{url}?{param_str}"

    try:
        # 发送请求
        response = urllib.request.urlopen(full_url, timeout=5)
        # 读取数据
        data = response.read().decode("utf-8")
        # 转json
        json_data = json.loads(data)
        print(json_data)
    except Exception as e:
        print("请求异常", e)


# =============== 2. 使用内置库 urllib 发送 POST 请求 ===============
def urllib_post_demo():
    print("\n===== urllib POST =====")
    url = "https://httpbin.org/post"
    data = {"username": "admin", "password": "123456"}
    # post数据编码
    data_bytes = urllib.parse.urlencode(data).encode("utf-8")

    req = urllib.request.Request(url, data=data_bytes, method="POST")
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    print(result)


# =============== 3. requests 库 GET 请求 ===============
def requests_get_demo():
    print("\n===== requests GET =====")
    url = "https://httpbin.org/get"
    params = {"page": 1, "size": 10}
    # 请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.get(url, params=params, headers=headers, timeout=5)
    # 获取json
    print("状态码:", response.status_code)
    print("响应json:", response.json())
    print("响应文本:", response.text)


# =============== 4. requests  POST 表单提交 ===============
def requests_post_form_demo():
    print("\n===== requests POST 表单 =====")
    url = "https://httpbin.org/post"
    data = {"user": "test", "msg": "hello"}
    response = requests.post(url, data=data)
    print(response.json())


# =============== 5. requests POST 提交JSON（常用）===============
def requests_post_json_demo():
    print("\n===== requests POST JSON =====")
    url = "https://httpbin.org/post"
    json_data = {
        "id": 1,
        "content": "测试数据"
    }
    # 自动设置Content-Type: application/json
    response = requests.post(url, json=json_data)
    print(response.json())


# =============== 6. 携带请求头、Cookie ===============
def requests_header_cookie():
    print("\n===== 请求头与Cookie =====")
    url = "https://httpbin.org/headers"
    headers = {
        "Token": "abcd1234",
        "Content-Type": "application/json"
    }
    cookies = {"uid": "1001", "token": "xyz"}
    res = requests.get(url, headers=headers, cookies=cookies)
    print(res.json())


# =============== 7. 文件上传 ===============
def requests_upload_file():
    print("\n===== 文件上传 =====")
    url = "https://httpbin.org/post"
    # 模拟文件
    files = {
        "file": ("test.txt", b"this is file content", "text/plain")
    }
    res = requests.post(url, files=files)
    print(res.json())


# =============== 8. 异常处理 ===============
def requests_exception():
    print("\n===== 异常处理 =====")
    try:
        res = requests.get("https://invalid.url", timeout=3)
        res.raise_for_status()  # 状态码非200抛出异常
    except requests.exceptions.Timeout:
        print("请求超时")
    except requests.exceptions.ConnectionError:
        print("连接失败")
    except requests.exceptions.RequestException as e:
        print("请求错误", e)


if __name__ == '__main__':
    urllib_get_demo()
    urllib_post_demo()
    requests_get_demo()
    requests_post_form_demo()
    requests_post_json_demo()
    requests_header_cookie()
    requests_upload_file()
    requests_exception()