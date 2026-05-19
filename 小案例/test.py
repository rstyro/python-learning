import os
from tqdm import tqdm

# 定义文件夹名称和对应的文件数量
configs = [
    ("test3000", 3000),
    ("test1w", 10000),
]

print("开始生成文件...")
for folder_name, file_count in configs:
    # 创建文件夹
    os.makedirs(folder_name, exist_ok=True)

    # 使用 tqdm 显示当前文件夹的进度条
    with tqdm(total=file_count, desc=f"正在生成 {folder_name}", unit="file") as pbar:
        for i in range(1, file_count + 1):
            file_path = os.path.join(folder_name, f"test{i}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(str(i))
            pbar.update(1)  # 每生成一个文件，进度条+1

print("所有文件生成完毕！")