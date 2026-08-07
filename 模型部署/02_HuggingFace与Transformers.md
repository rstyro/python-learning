# 02 · Hugging Face 与 Transformers 部署详解

> 难度：★★ | 目的：掌握官方生态，理解模型加载/推理/量化的底层原理
> Transformers 是 Hugging Face 官方库，支持几乎全部开源模型，也是学习模型部署原理的最佳入口

---

## 目录

1. [Hugging Face 平台](#1-hugging-face-平台)
2. [环境安装](#2-环境安装)
3. [模型下载](#3-模型下载)
4. [加载模型（四种方式）](#4-加载模型四种方式)
5. [推理与生成参数](#5-推理与生成参数)
6. [流式输出](#6-流式输出)
7. [量化：小显存跑大模型](#7-量化小显存跑大模型)
8. [模型保存与本地加载](#8-模型保存与本地加载)
9. [推理加速技巧](#9-推理加速技巧)
10. [错误排查](#10-错误排查)

---

## 1. Hugging Face 平台

### 1.1 平台结构
```
HuggingFace.co（模型托管平台）
├── 模型库：几千个开源模型（Qwen/Llama/DeepSeek...）
├── 数据集库：公开数据集
└── 官方库：
    ├── transformers    # 加载/推理/微调 大模型
    ├── tokenizers      # 分词器（文本→token）
    ├── datasets        # 数据集处理
    ├── accelerate      # 多GPU/混合精度训练推理
    ├── peft           # 高效微调（LoRA）
    └── safetensors     # 安全权重格式
```

### 1.2 模型命名规范
`org/model-name`，如：
- `Qwen/Qwen2.5-7B-Instruct`
- `meta-llama/Llama-3.1-8B-Instruct`
- `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B`

`from_pretrained("Qwen/Qwen2.5-7B-Instruct")` 会自动从 HF 下载。

### 1.3 国内加速（重要）
```bash
# 设置镜像环境变量（Windows PowerShell）
$env:HF_ENDPOINT = "https://hf-mirror.com"

# Linux/macOS
export HF_ENDPOINT=https://hf-mirror.com
```
设置后所有下载自动走镜像，速度提升明显。

### 1.4 安全警告：.bin/.pt vs safetensors

**重要**：PyTorch 的 `.bin`/`.pt` 格式使用 `pickle` 序列化，
恶意模型可能包含任意代码执行（类似"模型病毒"）。
HuggingFace 默认使用 **safetensors** 格式（纯数据，无代码），安全得多。

```python
# ✅ 安全：safetensors 格式
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct",     # 默认使用 safetensors
)

# ⚠️ 注意：如果模型只有 .bin 格式，from_pretrained 默认拒绝加载
# 如需加载，必须确认来源可信：
model = AutoModelForCausalLM.from_pretrained(
    "some-legacy-model",
    use_safetensors=False,           # 显式允许 pickle 加载（仅可信来源！）
)
```

> **原则**：优先使用 safetensors 格式的模型，拒绝来源不明的 .bin 模型。
> HuggingFace 上主流模型均已提供 safetensors 版本。

## 2. 环境安装

### 2.1 安装 PyTorch（核心依赖）
```bash
# 先确认已有 CUDA 环境：nvidia-smi 看到 CUDA 版本
# 有 GPU 装 CUDA 版（以 cu118 为例）：
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 无 GPU / 只想 CPU 跑：
pip install torch
```

> **重要**：`pip install torch` 默认装 CPU 版。
> 要 GPU 加速必须用 `--index-url .../cuXXX` 指定 CUDA 版本。
> 检查：`python -c "import torch; print(torch.cuda.is_available())"` 输出 True 才对。

### 2.2 安装 transformers 全家桶
```bash
pip install transformers            # 核心库
pip install accelerate             # 设备管理（device_map）
pip install bitsandbytes           # 量化（4bit/8bit）
pip install safetensors            # 安全权重加载
pip install sentencepiece          # 某些模型的 tokenizer 依赖
pip install protobuf               # 某些模型的配置文件依赖
```

## 3. 模型下载

### 3.1 自动下载（from_pretrained 时）
```python
# 第一次调用会自动下载权重（几 GB），之后用缓存
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-7B-Instruct")
```

### 3.2 显式下载（提前下好，方便离线）
```python
from huggingface_hub import snapshot_download

# 下载整个模型仓库到本地目录
snapshot_download(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    local_dir="./models/qwen2.5-7b",    # 下载到本地
    local_dir_use_symlinks=False
)
```

### 3.3 从 ModelScope 下载（国内更快）
```python
# pip install modelscope
from modelscope import snapshot_download

snapshot_download(
    "Qwen/Qwen2.5-7B-Instruct",
    local_dir="./models/qwen2.5-7b"
)
```
ModelScope 下载的文件和 HF 完全一样，之后可以本地加载。

### 3.4 断点续传
HF 下载支持断点续传，重跑同样的命令会跳过已下载的部分。

## 4. 加载模型（四种方式）

### 方式1：pipeline（最简单，推荐入门）
```python
from transformers import pipeline

# 一行加载对话模型
gen = pipeline("text-generation", model="Qwen/Qwen2.5-7B-Instruct")

# 调用
result = gen("介绍一下Python", max_new_tokens=200)
print(result[0]["generated_text"])
```

### 方式2：AutoModel（标准方式，可控性强）
```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 加载分词器和模型
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct")
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct",
    torch_dtype=torch.bfloat16,   # 半精度，省一半显存
    device_map="auto",            # 自动分配到 GPU/CPU
    trust_remote_code=True,       # 某些模型需要执行自定义代码
)
```

### 方式3：从本地目录加载（离线部署）
```python
model = AutoModelForCausalLM.from_pretrained(
    "./models/qwen2.5-7b",       # 本地路径（前面下载好的）
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
```

### 方式4：低显存加载（4bit 量化）
```python
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct",
    device_map="auto",
    load_in_4bit=True,            # 4bit 量化，显存需求降 75%
)
```
详见第 7 节。

### device_map 详解
| 取值 | 行为 |
|------|------|
| `"auto"` | 自动分配：优先 GPU，不够放 CPU |
| `0` | 全部放第 0 块 GPU |
| `"cpu"` | 全部放 CPU（纯 CPU 推理） |
| `"cuda"` | 全部放 GPU |
| `"sequential"` | 强制顺序分配到 GPU（不跨设备） |

### 推理函数封装（推荐模式）
```python
def generate_answer(prompt: str, max_new_tokens: int = 512) -> str:
    """封装推理：输入提示词，输出回答"""
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(   # 应用 chat 模板（Qwen/llama 特有）
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,          # 贪心解码（确定性）
    )
    return tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
```

## 5. 推理与生成参数

### generate() 核心参数
```python
outputs = model.generate(
    **inputs,
    max_new_tokens=512,        # 最多生成 512 个新 token
    do_sample=True,            # 采样模式（False=贪心，确定性）
    temperature=0.7,           # 采样温度
    top_p=0.9,                 # 核采样
    top_k=50,                  # 只从概率最高的 50 个词采样
    repetition_penalty=1.1,    # 重复惩罚（>1 抑制重复）
    num_return_sequences=1,    # 返回几个候选
    pad_token_id=tokenizer.eos_token_id,  # 防止 padding 报错
)
```

### 参数速查表
| 参数 | 用途 | 推荐值 |
|------|------|--------|
| max_new_tokens | 生成长度上限 | 任务而定 |
| do_sample | True=采样 / False=贪心 | Agent 决策用 False |
| temperature | 创造性 | 代码0.2 / 对话0.7 / 创意1.2 |
| top_p | 核采样阈值 | 0.9 |
| repetition_penalty | 防重复 | 1.1 |
| num_beams | 束搜索（质量更高但慢） | 4（可选） |

## 6. 流式输出

```python
from transformers import TextStreamer

# 流式打印到终端（打字机效果）
streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

outputs = model.generate(
    **inputs,
    max_new_tokens=512,
    streamer=streamer,          # 加这一行即可
)

# 或者自定义流式处理（用于 API 场景）
from transformers import TextIteratorStreamer
import threading

streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
# 在后台线程生成，主线程消费 streamer
thread = threading.Thread(target=model.generate, kwargs={**gen_kwargs, "streamer": streamer})
thread.start()
for text in streamer:
    print(text, end="", flush=True)   # 这里可以做实时转发
```

## 7. 量化：小显存跑大模型

### 7.1 为什么要量化
```
7B 模型原始显存需求：
  FP32 (32bit):  7B × 4字节 = 28GB
  FP16 (16bit):  7B × 2字节 = 14GB
  INT8 (8bit):   7B × 1字节 = 7GB
  INT4 (4bit):   7B × 0.5字节 = 3.5GB
```

### 7.2 bitsandbytes 4bit 量化（一行）
```python
import torch
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

# 配置 4bit 量化
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,               # 4bit 加载
    bnb_4bit_compute_dtype=torch.float16,  # 计算时用 fp16（加速）
    bnb_4bit_quant_type="nf4",       # 量化类型 nf4（效果好）
    bnb_4bit_use_double_quant=True,  # 双重量化（更省）
)

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct",
    quantization_config=quant_config,
    device_map="auto",
)
```

### 7.3 8bit 量化（质量损失更小）
```python
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct",
    load_in_8bit=True,
    device_map="auto",
)
```

### 7.4 量化选择建议
| 场景 | 推荐 |
|------|------|
| 显存充足（≥16GB） | FP16 或 bf16（无损失） |
| 显存中等（8GB） | INT8（损失极小） |
| 显存紧张（4-6GB） | INT4 / NF4 |
| 追求极致省显存 | INT4 + 小模型（1.5B/3B） |

> 注：bitsandbytes 目前在 Windows 上支持有限，建议 Windows 用户用
> GGUF + llama.cpp（见 05 篇）或 Ollama 做量化推理。

## 8. 模型保存与本地加载

```python
# 保存模型和分词器到本地（下次秒加载，不用再下载）
model.save_pretrained("./saved_model")
tokenizer.save_pretrained("./saved_model")

# 之后从本地加载
model = AutoModelForCausalLM.from_pretrained("./saved_model", device_map="auto")
```

## 9. 推理加速技巧

### 9.1 性能对比
| 方法 | 加速效果 | 要求 |
|------|---------|------|
| 半精度 (bf16/fp16) | 省50%显存 | 现代 GPU |
| torch.compile | 1.2-1.5x | PyTorch 2.x |
| FlashAttention-2 | 1.5-2x，省显存 | GPU 支持 |
| 批处理 (batch) | 多用户时吞吐↑ | 服务场景 |
| vLLM | 3-10x | 见 04 篇 |

### 9.2 代码示例
```python
# FlashAttention（需 GPU 支持）
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct",
    attn_implementation="flash_attention_2",   # 注意力机制优化
    device_map="auto",
)

# torch.compile
model = torch.compile(model, mode="reduce-overhead")
```

## 10. 错误排查

| 报错 | 原因 | 解决 |
|------|------|------|
| `CUDA out of memory` | 显存不足 | 量化 / 换小模型 / 减小 max_new_tokens |
| `can't load tokenizer` | 网络/镜像问题 | 设置 HF_ENDPOINT 镜像 |
| `ValueError: not a valid package name` | 模型名写错 | 检查 org/model-name 格式 |
| `trust_remote_code=True` 警告 | 模型有自定义代码 | 确认模型来源可信后加上 |
| `sentencepiece is required` | 缺分词依赖 | `pip install sentencepiece` |
| `KeyError: 'chat_template'` | 模型无 chat 模板 | 用非 Instruct 模型需手动拼 prompt |
| Windows 下 bitsandbytes 报错 | 兼容性问题 | 用 GGUF/Ollama 替代量化推理 |

---

## 小结

```
Transformers 全流程：
安装 → (设置镜像) → from_pretrained 加载 → generate 推理 → 流式/量化优化
```

**核心收获**：`from_pretrained + generate` 是核心两板斧。
`device_map` 控制设备、`torch_dtype` 控制精度、`quantization_config` 控制量化——这是部署的三大旋钮。
