import random
from datetime import datetime
from pathlib import Path

def _dated_path(base):
    """按当天日期生成文件路径：warn.txt -> warn-2026-08-17.txt，每天一个文件（跨天自动切换）"""
    p = Path(base)
    return p.with_name(f"{p.stem}-{datetime.now():%Y-%m-%d}{p.suffix}")

if __name__ == '__main__':
    rn = random.Random()
    print(rn)
    for i in range(100):
        print(rn.random())
    print(_dated_path("log.txt"))