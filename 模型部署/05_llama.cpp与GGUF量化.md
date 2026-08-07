# 05 · llama.cpp 与 GGUF 量化详解

> 难度：★★ | 目的：理解量化原理，掌握无 GPU 也能跑的部署方式
> llama.cpp 是 Ollama 的底层引擎，GGUF 是它的模型格式。理解它 = 理解量化推理的全部秘密

---

## 目录

1. [llama.cpp 是什么](#1-llamacpp-是什么)
2. [GGUF 模型格式](#2-gguf-模型格式)
3. [量化等级详解](#3-量化等级详解)
4. [下载 GGUF 模型](#4-下载-gguf-模型)
5. [安装 llama.cpp](#5-安装-llamacpp)
6. [CPU 推理](#6-cpu-推理)
7. [GPU 推理](#7-gpu-推理)
8. [llama-cpp-python（Python 库）](#8-llama-cpp-pythonpython-库)
9. [自己动手量化模型](#9-自己动手量化模型)
10. [与 Ollama 的关系](#10-与-ollama-的关系)

---

## 1. llama.cpp 是什么

```
llama.cpp = 一个用 C/C++ 写的推理引擎
┌────────────────────────────────────────────┐
│ 特点：                                      │
│ 1. 纯 C/C++，无 Python 依赖                │
│ 2. 高度优化，CPU 也能跑（AVX/NEON 指令加速）│
│ 3. 原生支持 GGUF 量化格式                   │
│ 4. 内存占用极低                             │
└────────────────────────────────────────────┘
```

**为什么重要**：
- **Ollama 的底层就是 llama.cpp**（理解它 = 理解 Ollama 内部）
- 能在没 GPU 的服务器、树莓派、老笔记本上跑模型
- 量化格式 GGUF 是开源模型分发的实际标准之一

## 2. GGUF 模型格式

### 2.1 什么是 GGUF
GGUF（GPT-Generated Unified Format）是 llama.cpp 的专用模型格式，
把权重、分词器、配置、量化信息打包在**单个文件**里。

```
一个 .gguf 文件包含：
├── 魔数（文件头）
├── 元数据（模型名、参数量、上下文长度...）
├── 分词器词汇表
└── 量化后的权重张量（Q4_K_M 等）
```

### 2.2 GGUF vs safetensors
| 对比项 | GGUF | safetensors |
|--------|------|-------------|
| 单文件 | ✅ 一个文件 | 多个文件（shard） |
| 量化 | 内置支持 | 需额外工具 |
| 引擎 | llama.cpp 系列 | transformers |
| 加载速度 | 快（直接内存映射） | 一般 |
| 用途 | 推理分发 | 训练/微调 |

## 3. 量化等级详解

### 3.1 GGUF 量化命名规则
```
Q4_K_M  ← 命名解析
│││└─ 变体：M=中等 S=小 L=大（精度递增）
││└─ 类型：K=K-quant（混合精度量化）
│└─ 位数：4 = 4bit
└─ 前缀：Q = Quantized
```

### 3.2 常用量化等级对比
| 等级 | 位宽 | 7B模型大小 | 质量 | 场景 |
|------|------|-----------|------|------|
| F16 | 16bit | ~14GB | 无损 | 显存充足 |
| Q8_0 | 8bit | ~7GB | 接近无损 | 质量优先 |
| Q6_K | ~6bit | ~5.6GB | 很好 | 均衡 |
| **Q5_K_M** | ~5bit | ~4.8GB | 好 | **推荐** |
| **Q4_K_M** | ~4bit | ~4.4GB | 良好 | **推荐/均衡** |
| Q3_K_M | ~3bit | ~3.3GB | 一般 | 显存紧张 |
| Q2_K | ~2bit | ~2.6GB | 差 | 极限省显存 |

### 3.2.1 IQ 量化（Importance Quantization，2024 新方案）

IQ 量化是 llama.cpp 在 K-Quant 之后推出的新一代量化方案，
核心改进是 **按权重的重要性分配位宽**——重要权重用更高精度，不重要权重可以压到 2bit 以下。

| 等级 | 位宽 | 7B模型大小 | 质量 | 对比 K-Quant |
|------|------|-----------|------|-------------|
| IQ4_NL | ~4.5bit | ~4.8GB | 全面优于 Q4_K_M | **新甜点** |
| IQ4_XS | ~4.2bit | ~4.5GB | 略优于 Q4_K_M | 更小更快 |
| IQ3_M | ~3.5bit | ~3.8GB | 接近 Q4_K_M | 省 1GB |
| IQ3_XXS | ~3.0bit | ~3.1GB | 接近 Q4_K_S | 极度省空间 |
| IQ2_M | ~2.5bit | ~2.8GB | 接近 Q3_K_M | 极限场景 |
| IQ2_XXS | ~2.0bit | ~2.5GB | 接近 Q3_K_S | 最小体积 |
| IQ1_S | ~1.5bit | ~2.0GB | 勉强可用 | 仅限实验 |

> **升级建议**：
> - 一直在用 Q4_K_M → 换 **IQ4_NL**，同体积下质量更好
> - 4-8GB 显存用户 → 试试 **IQ3_XXS**，3.1GB 跑 7B 质量可接受
> - IQ2 以下质量损失显著，除非极度空间受限否则不推荐

### 3.2.2 IQ vs K-Quant 选择指南

```
你的显存 → K-Quant 方案 → IQ 升级方案
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
24GB+    → Q8_0 / Q6_K   → IQ4_NL（质量更好）
16GB     → Q5_K_M        → IQ4_NL（更快）
8-12GB   → Q4_K_M        → IQ4_XS / IQ3_M（更省）
6-8GB    → Q3_K_M        → IQ3_XXS（质变提升）
4GB      → Q2_K          → IQ2_M（极限场景仍有优化）
```

> **命名规律**：IQ = Importance Quantization，数字 = 平均位宽，S/M/L = 块大小。
> IQ 对重要层（attention、FFN 前几层）用更高精度，对不重要层大胆压缩。

> **实战建议**：
> - 8GB+ 显存 → Q6_K 或 Q8_0
> - 4-8GB → Q4_K_M / Q5_K_M
> - 2-4GB → Q3_K_M 或换更小参数量模型

### 3.3 量化损失的可感知程度
```
质量损失（从小到大）：
F16 ≈ Q8_0 < Q6_K < Q5_K_M < Q4_K_M < Q3_K_M < Q2_K

经验法则：
- 日常聊天/写作：Q4 完全够用
- 代码生成：建议 Q5 以上
- 数学推理：尽量 Q6 以上（低精度对数字敏感）
```

IQ 系列由于重要性感知，同一位宽下的代码生成和数学推理能力明显优于 K-Quant。
实测 IQ3_XXS 的代码生成质量 ≈ Q4_K_M 水平，但模型只有 3.1GB。

## 4. 下载 GGUF 模型

### 4.1 从 HuggingFace（推荐）
GGUF 模型通常在 `TheBloke` 或 `Qwen` 官方账号下：
```
https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF
https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF
```

```bash
# 方式1：huggingface-cli 下载单个文件
$env:HF_ENDPOINT = "https://hf-mirror.com"
pip install huggingface_hub

# 下载指定量化文件（用 hf download 命令）
hf download Qwen/Qwen2.5-7B-Instruct-GGUF qwen2.5-7b-instruct-q4_k_m.gguf \
    --local-dir ./models
```

### 4.2 从 ModelScope（国内加速）
```bash
# ModelScope 上有 GGUF 仓库
pip install modelscope

python -c "
from modelscope import snapshot_download
snapshot_download('Qwen/Qwen2.5-7B-Instruct-GGUF', local_dir='./models')
"
```

### 4.3 命名识别
```
文件名解析：
qwen2.5-7b-instruct-q4_k_m.gguf
      ├─ 模型名 qwen2.5-7b-instruct
      └─ 量化等级 q4_k_m
```

## 5. 安装 llama.cpp

### 5.1 方式1：官方编译版（GitHub Releases）
```bash
# 访问 https://github.com/ggerganov/llama.cpp/releases
# 下载对应平台包：
#   Windows: llama-bXXXX-bin-win-cuda-cu12.4-x64.zip（GPU版）
#   Windows: llama-bXXXX-bin-win-avx2-x64.zip（CPU版）
# 解压后，文件夹内就是可执行文件（llama-cli.exe 等）
```

### 5.2 方式2：源码编译（Linux/macOS）
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
mkdir build && cd build

# CPU 版
cmake .. && cmake --build . --config Release

# CUDA 版
cmake .. -DGGML_CUDA=ON && cmake --build . --config Release
```

### 5.3 方式3：Python 库（llama-cpp-python，最方便）
```bash
# CPU 版
pip install llama-cpp-python

# CUDA 版（有 GPU 时）
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python
```

## 6. CPU 推理

### 6.1 命令行（llama-cli）
```bash
# 交互式对话
./llama-cli -m ./models/qwen2.5-7b-instruct-q4_k_m.gguf \
    -p "你好" \
    -n 256 \
    -t 8                    # CPU 线程数
```

### 6.2 参数速查
| 参数 | 含义 |
|------|------|
| -m | 模型文件路径 |
| -p | 初始提示词 |
| -n | 生成 token 数 |
| -t | CPU 线程数 |
| -c | 上下文长度（默认512） |
| --temp | 温度 |
| -ngl | 多少层放到 GPU（见下节） |

## 7. GPU 推理

### 7.1 显存分层策略（关键概念）
```
llama.cpp 支持"部分层放 GPU，部分层留 CPU"：
-ngl N  = 前 N 层放到 GPU 加速
-ngl 99 = 全部层放 GPU（显存够时最快）
-ngl 0  = 纯 CPU

好处：显存不够也能跑，GPU 加速一部分，速度介于纯CPU和纯GPU之间
```

### 7.2 实战示例
```bash
# 8GB 显存跑 7B 模型（全部放 GPU）
./llama-cli -m ./qwen-7b-q4_k_m.gguf -ngl 99

# 4GB 显存跑 7B 模型（部分层卸载到 CPU）
./llama-cli -m ./qwen-7b-q4_k_m.gguf -ngl 20 -t 8

# 无 GPU
./llama-cli -m ./qwen-7b-q4_k_m.gguf -ngl 0 -t 8
```

### 7.3 GPU 服务模式（llama-server）
```bash
# 启动 OpenAI 兼容服务
./llama-server -m ./qwen-7b-q4_k_m.gguf \
    --host 0.0.0.0 \
    --port 8080 \
    -ngl 99

# 测试
curl http://localhost:8080/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model":"qwen","messages":[{"role":"user","content":"你好"}]}'
```

## 8. llama-cpp-python（Python 库）

### 8.1 基础调用
```python
from llama_cpp import Llama

# 加载 GGUF 模型
llm = Llama(
    model_path="./models/qwen2.5-7b-instruct-q4_k_m.gguf",
    n_ctx=2048,        # 上下文长度
    n_gpu_layers=99,   # GPU 层数（-1 或 99 = 全部 GPU）
    n_threads=8,       # CPU 线程
    verbose=False,
)

# 生成
output = llm(
    "什么是Python装饰器？",
    max_tokens=256,
    temperature=0.7,
    echo=False,               # 不重复输入
)
print(output["choices"][0]["text"])
```

### 8.2 聊天模板
```python
output = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "你是Python专家"},
        {"role": "user", "content": "什么是列表推导式？"},
    ],
    max_tokens=256,
)
print(output["choices"][0]["message"]["content"])
```

### 8.3 流式输出
```python
for chunk in llm(
    "写一段关于大海的描述",
    max_tokens=200,
    stream=True,               # 流式
):
    text = chunk["choices"][0]["text"]
    print(text, end="", flush=True)
print()
```

### 8.4 OpenAI 兼容服务（可选）
```python
from llama_cpp.server.app import create_app   # 实验性
# 或直接用命令行：llama-cpp-python 自带 llama-server
```

## 9. 自己动手量化模型

### 9.1 准备 HF 模型
```bash
# 先下载 safetensors 格式模型
$env:HF_ENDPOINT = "https://hf-mirror.com"
hf download Qwen/Qwen2.5-7B-Instruct --local-dir ./hf-model
```

### 9.2 转 GGUF 并量化
```bash
# 1. 转 GGUF（hf-to-gguf 转换脚本在 llama.cpp 仓库）
python convert_hf_to_gguf.py ./hf-model \
    --outfile ./model-f16.gguf \
    --outtype f16

# 2. 量化到 Q4_K_M
./llama-quantize ./model-f16.gguf \
    ./model-q4_k_m.gguf \
    Q4_K_M
```

### 9.3 量化等级表（llama-quantize 参数）
```bash
# 常用量化类型（Q 系列 + IQ 系列）
./llama-quantize ./model-f16.gguf ./model-q4_k_m.gguf Q4_K_M
./llama-quantize ./model-f16.gguf ./model-iq4_nl.gguf IQ4_NL
./llama-quantize ./model-f16.gguf ./model-iq3_xxs.gguf IQ3_XXS

# 全部可用类型（llama-quantize --help 查看完整列表）：
# Q2_K Q3_K_S Q3_K_M Q3_K_L Q4_0 Q4_K_S Q4_K_M Q5_0 Q5_K_S Q5_K_M Q6_K Q8_0
# IQ1_S IQ1_M IQ2_XXS IQ2_XS IQ2_S IQ2_M IQ3_XXS IQ3_S IQ3_M IQ4_XS IQ4_NL
```

## 10. 与 Ollama 的关系

```
┌─────────────────────────────────────────────┐
│  Ollama（面向用户）                          │
│  ├── 客户端：ollama CLI / Python 库          │
│  ├── 模型管理：pull/run/list                 │
│  └── 引擎：内置 llama.cpp 编译版             │
│       ├── 模型统一转 GGUF                    │
│       └── 支持 -ngl 类似策略（自动显存管理）  │
└─────────────────────────────────────────────┘

结论：Ollama 的 pull 就是把 HF 上的 GGUF（或转换后的模型）
      缓存在本地，run 时调用 llama.cpp 引擎推理。
```

### 两者选择
| 需求 | 选择 |
|------|------|
| 快速使用、不折腾 | Ollama |
| 精细控制量化/层卸载 | llama.cpp 直接操作 |
| 开发产品 | 优先 vLLM（见04篇） |
| 嵌入到 Python 项目 | llama-cpp-python 或 Ollama |

---

## 小结

```
llama.cpp 全流程：
下载 GGUF → llama-cli/llama-server 运行 → -ngl 控制 GPU 分层
        → 或 pip install llama-cpp-python 嵌入 Python
```

**核心收获**：
1. GGUF = 单文件 + 内置量化，是最流行的分发格式
2. `-ngl` 分层加载 = 显存不足时的核心技巧
3. Ollama 底层就是 llama.cpp，理解它 = 理解 Ollama
