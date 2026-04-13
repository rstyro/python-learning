# -*- coding: utf-8 -*-
"""
tqdm 全场景示例合集
"""

# 1. 导入所有依赖库
from tqdm import tqdm, trange
import time
import requests

# ====================== 第一阶段：入门基础用法 ======================
def demo1_basic():
    """示例1：最简单的进度条（包装for循环）"""
    print("\n【示例1】基础进度条")
    for i in tqdm(range(100)):
        time.sleep(0.01)

def demo2_trange():
    """示例2：简写 trange（等价 tqdm(range())）"""
    print("\n【示例2】trange 简写")
    for i in trange(100):
        time.sleep(0.01)

def demo3_desc():
    """示例3：添加文字描述 desc"""
    print("\n【示例3】自定义描述文字")
    data_list = list(range(10))
    for item in tqdm(data_list, desc="处理数据中"):
        time.sleep(0.2)

def demo4_iterable():
    """示例4：遍历列表/字典（通用可迭代对象）"""
    print("\n【示例4】遍历列表+字典")
    # 遍历列表
    names = ["张三", "李四", "王五"]
    for name in tqdm(names, desc="遍历名单"):
        time.sleep(0.3)

    # 遍历字典
    person = {"姓名": "小明", "年龄": 18, "城市": "北京"}
    for k, v in tqdm(person.items(), desc="遍历字典"):
        time.sleep(0.3)

def demo5_unit():
    """示例5：自定义单位（张/个/次）"""
    print("\n【示例5】自定义单位")
    for i in tqdm(range(50), desc="下载图片", unit="张"):
        time.sleep(0.05)

# ====================== 第二阶段：进阶美化与手动控制 ======================
def demo6_color():
    """示例6：彩色进度条"""
    print("\n【示例6】彩色进度条")
    for i in tqdm(range(50), desc="彩色进度条", colour="cyan"):
        time.sleep(0.05)

def demo7_manual():
    """示例7：手动更新进度条（下载/流式数据专用）"""
    print("\n【示例7】手动控制进度")
    with tqdm(total=100, desc="手动进度") as pbar:
        for i in range(10):
            time.sleep(0.2)
            pbar.update(10)  # 每次增加10%进度

def demo8_width():
    """示例8：自定义进度条宽度"""
    print("\n【示例8】窄进度条")
    for i in tqdm(range(50), desc="窄进度条", ncols=50):
        time.sleep(0.05)

def demo9_leave():
    """示例9：执行完不保留进度条"""
    print("\n【示例9】临时进度条（执行后消失）")
    for i in tqdm(range(20), desc="临时进度", leave=False):
        time.sleep(0.1)
    print("任务完成！")

# ====================== 第三阶段：实用场景（爬虫/下载/工作） ======================
def demo10_batch_download():
    """示例10：批量下载文件（贴合你的图片下载场景）"""
    print("\n【示例10】批量下载图片（模拟）")
    img_urls = ["1.png", "2.png", "3.png", "4.png"]
    for url in tqdm(img_urls, desc="📥 批量下载图片", unit="张", colour="blue"):
        time.sleep(0.3)

def demo11_big_file_download():
    """示例11：大文件分块下载（精确进度）"""
    print("\n【示例11】大文件分块下载（已注释，替换链接可运行）")
    # 真实使用时替换URL和保存路径
    # url = "https://example.com/large_file.zip"
    # download_big_file(url, "test.zip")

def demo12_dynamic_info():
    """示例12：动态显示当前处理内容"""
    print("\n【示例12】动态显示当前文件")
    files = ["封面.jpg", "头像.png", "背景图.jpg"]
    with tqdm(files, desc="处理图片") as pbar:
        for file in pbar:
            time.sleep(0.5)
            pbar.set_postfix(当前处理=file)

# ====================== 第四阶段：高级用法 ======================
def demo13_nested():
    """示例13：嵌套多层进度条"""
    print("\n【示例13】嵌套进度条")
    for epoch in tqdm(range(3), desc="总任务"):
        for batch in tqdm(range(5), desc=f"子任务{epoch+1}", leave=False):
            time.sleep(0.1)

def demo14_disable():
    """示例14：禁用进度条（调试用）"""
    print("\n【示例14】关闭进度条")
    for i in tqdm(range(10), disable=True):
        time.sleep(0.1)
    print("进度条已禁用，直接执行完成")

def demo15_print_compatible():
    """示例15：兼容打印（不破坏进度条）"""
    print("\n【示例15】安全打印")
    for i in tqdm(range(5)):
        time.sleep(0.5)
        tqdm.write(f"✅ 完成第 {i+1} 步")

def demo16_windows_fix():
    """示例16：Windows 终端乱码修复"""
    print("\n【示例16】Windows 兼容模式")
    for i in tqdm(range(50), ascii=True, desc="纯字符进度条"):
        time.sleep(0.02)

# ====================== 工具函数：大文件下载 ======================
def download_big_file(url, save_path):
    """大文件分块下载工具函数"""
    resp = requests.get(url, stream=True)
    total_size = int(resp.headers.get("content-length", 0))

    with open(save_path, "wb") as f, tqdm(
            desc="大文件下载",
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
    ) as pbar:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))

# ====================== 主函数：运行所有示例 ======================
if __name__ == "__main__":
    print("="*60)
    print("tqdm 全示例运行开始")
    print("="*60)

    # 运行入门示例
    demo1_basic()
    demo2_trange()
    demo3_desc()
    demo4_iterable()
    demo5_unit()

    # 运行进阶示例
    demo6_color()
    demo7_manual()
    demo8_width()
    demo9_leave()

    # 运行实用场景
    demo10_batch_download()
    demo11_big_file_download()
    demo12_dynamic_info()

    # 运行高级用法
    demo13_nested()
    demo14_disable()
    demo15_print_compatible()
    demo16_windows_fix()

    print("\n" + "="*60)
    print("所有 tqdm 示例运行完毕！")
    print("="*60)