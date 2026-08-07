# 04 · vLLM 生产级部署详解

> 难度：★★★ | 目的：高吞吐、高并发的大模型推理服务
> vLLM 是目前最流行的生产级推理引擎，单卡吞吐量可达 transformers 的 10-20 倍

---

## 目录

1. [为什么需要 vLLM](#1-为什么需要-vllm)
2. [硬件要求](#2-硬件要求)
3. [安装](#3-安装)
4. [快速上手](#4-快速上手)
5. [OpenAI 兼容服务](#5-openai-兼容服务)
6. [服务化部署（vllm serve）](#6-服务化部署vllm-serve)
7. [高级调优](#7-高级调优)
8. [量化支持](#8-量化支持)
9. [多 GPU 与多节点](#9-多-gpu-与多节点)
10. [对比总结](#10-对比总结)
11. [工具调用（Function Calling）](#11-工具调用function-calling)
12. [结构化输出（Guided Decoding）](#12-结构化输出guided-decoding)
13. [LoRA 多租户适配器](#13-lora-多租户适配器)

---

## 1. 为什么需要 vLLM

### 核心痛点
```
transformers 的 generate() 每处理一个请求：
1. 要为该请求重新分配显存（KV Cache 大小预分配）
2. 无法共享模型权重
3. 请求间不能动态调度

→ 显存利用率低，并发一高就 OOM，吞吐量上不去
```

### vLLM 的三大创新
```
1. PagedAttention（分页注意力）
   ┌──────────────────────────────────────────┐
   │ 像操作系统虚拟内存一样，把 KV Cache 分页 │
   │ 只按需分配、用完即回收 → 显存利用率 90%+ │
   └──────────────────────────────────────────┘

2. Continuous Batching（连续批处理）
   ┌──────────────────────────────────────────┐
   │ 请求动态进出批次，有请求就喂给 GPU       │
   │ 而不是等一批全部完成再处理下一批          │
   └──────────────────────────────────────────┘

3. Prefix Caching（前缀缓存）
   相同前缀（如 system prompt）的 KV 缓存直接复用
```

### 性能对比（同硬件）
| 引擎 | 吞吐（tokens/秒） | 并发能力 |
|------|------------------|---------|
| transformers | 基线 | 低（易 OOM） |
| FasterTransformer | ~1.5x | 中 |
| TensorRT-LLM | ~3x | 高 |
| **vLLM** | **~10-20x** | **极高** |

## 2. 硬件要求

### 最低配置
- **GPU**：至少 16GB 显存（跑 7B 模型）
- **推荐配置**：单卡 24GB（如 4090）/ 48GB（A6000）/ 80GB（A100/H100）
- **CUDA**：11.8+（vLLM 需要较新驱动）

### 显存需求速查
| 模型 | FP16 | 4bit量化 |
|------|------|---------|
| 7B | 14GB | 4GB |
| 13B | 26GB | 7GB |
| 70B | 140GB | 40GB |
| 8x70B | 多卡 | 多卡 |

> 显存不足时 vLLM 会用 CPU 做 KV Cache offload，但性能大幅下降。
> 生产环境务必保证显存充足。

## 3. 安装

```bash
# 官方推荐（自动匹配 CUDA 版本）
pip install vllm

# 中国大陆加速（pip 换源后）
pip install vllm -i https://mirrors.aliyun.com/pypi/simple/

# 验证
python -c "import vllm; print(vllm.__version__)"
```

> ⚠️ vLLM 只支持 NVIDIA CUDA 或 AMD ROCm，不支持纯 CPU。
> Windows 支持有限，建议 Docker 或 WSL2 运行。

## 4. 快速上手

### 4.1 单次生成
```python
from vllm import LLM, SamplingParams

# 加载模型（首次自动从 HF 下载）
llm = LLM(model="Qwen/Qwen2.5-7B-Instruct")

# 生成参数
sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=512,
)

# 批量生成（传入列表，自动批处理）
outputs = llm.generate(
    ["介绍一下Python", "什么是机器学习？"],
    sampling_params,
)

for output in outputs:
    prompt = output.prompt
    generated = output.outputs[0].text
    print(f"提示词: {prompt}")
    print(f"回答: {generated}")
    print("-" * 40)
```

### 4.2 流式生成
```python
from vllm import LLM, SamplingParams

llm = LLM(model="Qwen/Qwen2.5-7B-Instruct")

outputs = llm.generate(
    ["讲一个关于程序员的笑话"],
    SamplingParams(max_tokens=200),
)

for output in outputs:
    for step in output.outputs[0]:
        print(step.text, end="", flush=True)   # 每个 step 是一小段文本
    print()
```

### 4.3 带聊天模板
```python
from vllm import LLM, SamplingParams

llm = LLM(model="Qwen/Qwen2.5-7B-Instruct")

# 直接传消息列表，vLLM 自动应用 chat 模板
outputs = llm.chat(
    messages=[
        {"role": "system", "content": "你是 Python 专家"},
        {"role": "user", "content": "什么是装饰器？"},
    ],
    sampling_params=SamplingParams(max_tokens=512),
)
print(outputs[0].outputs[0].text)
```

## 5. OpenAI 兼容服务

### 5.1 命令行启动
```bash
# 一键启动 OpenAI 兼容的 HTTP 服务
vllm serve Qwen/Qwen2.5-7B-Instruct \
    --port 8000 \
    --host 0.0.0.0 \
    --tensor-parallel-size 1       # 单卡
```

### 5.2 用 OpenAI 库调用
```python
from openai import OpenAI

client = OpenAI(
    api_key="vllm",                                # 任意值
    base_url="http://localhost:8000/v1",           # vLLM 服务地址
)

# 普通对话
response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[{"role": "user", "content": "你好"}],
    stream=True,
)
for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### 5.3 服务端支持的全部端点
```
GET  /v1/models                          # 模型列表
POST /v1/chat/completions                # 对话（支持 tools）
POST /v1/completions                     # 纯文本补全
POST /v1/embeddings                      # 向量化
GET  /health                             # 健康检查
POST /v1/chat/completions                # 流式（stream: true）
```

## 6. 服务化部署（vllm serve）

### 6.1 常用启动参数
```bash
vllm serve Qwen/Qwen2.5-7B-Instruct \
    --port 8000 \
    --gpu-memory-utilization 0.9 \      # 显存利用率上限 90%
    --max-model-len 8192 \              # 最大上下文长度
    --max-num-seqs 256 \                # 最大并发序列数
    --enable-prefix-caching \           # 开启前缀缓存
    --served-model-name my-model        # 对外暴露的模型名（可自定义）
```

### 6.2 多模型服务
```bash
# 同时服务两个模型（不同路径）
vllm serve Qwen/Qwen2.5-7B-Instruct --port 8000
# 另一个终端
vllm serve Llama-3.1-8B-Instruct --port 8001
```

### 6.3 与 Agent 集成
```python
# 你的 Agent 只要改 base_url，就把 LLM 大脑换成 vLLM 服务
client = OpenAI(
    api_key="vllm",
    base_url="http://localhost:8000/v1",   # ← 唯一改动
)
# tools / stream / 多轮对话 全部照常
```

## 7. 高级调优

### 7.1 吞吐优化参数
| 参数 | 作用 |
|------|------|
| --gpu-memory-utilization | 提高显存利用率（默认0.9） |
| --max-num-seqs | 增大批处理大小 |
| --enable-prefix-caching | 相同前缀缓存复用 |
| --kv-cache-dtype fp8 | KV 缓存量化，更省显存 |

### 7.2 在线吞吐测试
```bash
# 官方压测工具
python -m vllm.benchmark.benchmark_throughput \
    --model Qwen/Qwen2.5-7B-Instruct \
    --num-prompts 100 \
    --input-len 512 \
    --output-len 256
```

### 7.3 结构化输出（JSON）
```python
from vllm import LLM, SamplingParams

# 4.0+ 版本支持 response_format（OpenAI 兼容）
llm = LLM(model="Qwen/Qwen2.5-7B-Instruct")
sampling_params = SamplingParams(max_tokens=256, response_format={"type": "json_object"})

outputs = llm.generate(["返回一个JSON：{\"name\": \"张三\"}"], sampling_params)
print(outputs[0].outputs[0].text)   # 输出保证是合法 JSON
```

## 8. 量化支持

### 8.1 AWQ（推荐，质量和速度兼顾）
```bash
# 先离线量化（需要 GPU）
python -m vllm.entrypoints.quantization \
    --model Qwen/Qwen2.5-7B-Instruct \
    --quantization awq \
    --output-format safetensors \
    --output-dir ./qwen-awq
```

### 8.2 启动时加载量化模型
```bash
vllm serve TheBloke/Qwen2.5-7B-Instruct-AWQ \
    --quantization awq
```

### 8.3 支持矩阵
| 量化 | vLLM 支持 | 说明 |
|------|----------|------|
| AWQ | ✅ 完整 | 精度/速度均衡 |
| GPTQ | ✅ 完整 | 经典方案 |
| FP8 | ✅ | 需 H 卡 |
| bitsandbytes | ⚠️ 实验性 | 慢，不推荐 |

## 9. 多 GPU 与多节点

### 9.1 单机多卡（张量并行）
```bash
# 2 张卡跑同一个模型（模型被切分到两张卡）
vllm serve Qwen2.5-72B-Instruct --tensor-parallel-size 2
```

### 9.2 多机（需要集群）
```bash
# 需要 ray 集群（pip install ray），然后：
vllm serve Qwen2.5-72B-Instruct --tensor-parallel-size 8 --pipeline-parallel-size 2
```

## 10. 对比总结

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│              │ Ollama       │ Transformers │ vLLM         │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ 定位         │ 个人使用      │ 学习/研究     │ 生产服务      │
│ 并发能力     │ 低(默认1)     │ 低           │ 极高          │
│ 吞吐         │ 中           │ 低           │ 最高          │
│ 上手难度     │ ⭐最简单      │ ★★          │ ★★★          │
│ 适用场景     │ 本地开发      │ 实验/微调     │ 上线/多用户   │
│ 推荐硬件     │ 任意          │ 任意         │ 16GB+ 显存    │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

---

## 11. 工具调用（Function Calling）

vLLM 完整支持 OpenAI 兼容的 `tools` 参数，允许 LLM 决定调用外部工具。

### 11.1 定义工具并调用
```python
from openai import OpenAI

client = OpenAI(
    api_key="vllm",
    base_url="http://localhost:8000/v1",
)

# 定义工具（JSON Schema，与 OpenAI 格式完全一致）
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称（如'北京'）"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式（如 '3*4+5'）"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# 第一轮：LLM 决定调用哪个工具
response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[{"role": "user", "content": "北京今天天气怎么样？"}],
    tools=tools,
    tool_choice="auto",          # LLM 自动决定是否调用工具
)

# 检查是否有工具调用
msg = response.choices[0].message
if msg.tool_calls:
    for tc in msg.tool_calls:
        fn_name = tc.function.name
        fn_args = json.loads(tc.function.arguments)
        print(f"调用工具: {fn_name}({fn_args})")
        
        # 执行工具（你的业务逻辑）
        if fn_name == "get_weather":
            result = get_weather(fn_args["city"])
        
        # 第二轮：把工具结果反馈给 LLM
        messages = [
            {"role": "user", "content": "北京今天天气怎么样？"},
            msg.model_dump(),                               # LLM 的工具调用消息
            {"role": "tool", "content": result, "tool_call_id": tc.id},  # 工具结果
        ]
        response2 = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=messages,
            tools=tools,
        )
        print(response2.choices[0].message.content)         # 最终回答
```

### 11.2 可用的工具调用模型
工具调用需要模型原生支持。推荐：
- **Qwen2.5-Instruct 系列**（7B+）：原生支持，质量高
- **Llama 3.1-Instruct 系列**（8B+）：原生支持
- **DeepSeek-R1-Distill 系列**：部分支持
- **Mistral Nemo / Large**：原生支持

### 11.3 vLLM 原生 Python API 的工具调用
```python
from vllm import LLM, SamplingParams

llm = LLM(model="Qwen/Qwen2.5-7B-Instruct")

# 直接传 tools 到 SamplingParams
sampling_params = SamplingParams(
    max_tokens=256,
    temperature=0,
    tools=tools,                 # 工具列表
    tool_choice="auto",
)

outputs = llm.chat(
    messages=[{"role": "user", "content": "北京天气怎么样？"}],
    sampling_params=sampling_params,
)
```

## 12. 结构化输出（Guided Decoding）

vLLM 支持强制模型按指定格式输出，确保输出是合法 JSON、符合正则表达式等。

### 12.1 JSON 模式输出
```python
from vllm import LLM, SamplingParams
from vllm.sampling_params import GuidedDecodingParams

llm = LLM(model="Qwen/Qwen2.5-7B-Instruct")

# 方式1：简单的 JSON object 约束
sampling_params = SamplingParams(
    max_tokens=256,
    guided_decoding=GuidedDecodingParams(
        choice=["positive", "negative", "neutral"]   # 限制输出为三选一
    )
)

# 方式2：自定义 JSON Schema
json_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "skills": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["name", "age", "skills"]
}

sampling_params = SamplingParams(
    max_tokens=256,
    temperature=0,
    guided_decoding=GuidedDecodingParams(json=json_schema),
)

outputs = llm.generate(
    ["返回一个包含姓名、年龄、技能的 JSON"],
    sampling_params,
)
print(outputs[0].outputs[0].text)  # 输出保证符合 JSON Schema
```

### 12.2 正则表达式约束
```python
# 强制输出 YYYY-MM-DD 格式的日期
sampling_params = SamplingParams(
    max_tokens=64,
    guided_decoding=GuidedDecodingParams(
        regex=r"\d{4}-\d{2}-\d{2}"
    ),
)

# 强制输出选择题答案
sampling_params = SamplingParams(
    max_tokens=8,
    guided_decoding=GuidedDecodingParams(
        regex=r"[A-D]"             # 只允许 A、B、C、D
    ),
)
```

### 12.3 上下文无关文法（CFG）
```python
# 高级用法：EBNF 文法约束
grammar = '''
root ::= "Name: " name "\\n" "Age: " age
name ::= [A-Z][a-z]+
age ::= [0-9]+
'''
sampling_params = SamplingParams(
    guided_decoding=GuidedDecodingParams(grammar=grammar),
)
```

### 12.4 结构化输出的价值
```
使用场景：
- Agent 工具决策 → 强制 JSON，确保下游解析不报错
- 信息提取 → 正则约束字段格式（邮箱、电话、日期）
- 分类任务 → choice 约束，只输出预定义标签
- 代码生成 → 文法约束，确保语法正确

对比传统方式：
  普通 prompt "请以 JSON 格式输出" → 可能多几个换行/注释 → 解析失败
  Guided Decoding → 强制合法 → 100% 解析成功
```

## 13. LoRA 多租户适配器

vLLM 支持在同一个基座模型上加载多个 LoRA adapter，实现"一模型服务多业务"。

### 13.1 加载 LoRA 模块
```bash
# 启动时指定多个 LoRA adapter
vllm serve Qwen/Qwen2.5-7B-Instruct \
    --lora-modules finance=./loras/finance-adapter \
    --lora-modules medical=./loras/medical-adapter \
    --lora-modules code=./loras/code-adapter \
    --max-lora-rank 64
```

### 13.2 Python API 调用不同 LoRA
```python
from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest

llm = LLM(
    model="Qwen/Qwen2.5-7B-Instruct",
    enable_lora=True,
    max_lora_rank=64,
)

# 创建 LoRA 请求
finance_lora = LoRARequest("finance", 1, "./loras/finance-adapter")
medical_lora = LoRARequest("medical", 2, "./loras/medical-adapter")

# 不同请求使用不同 LoRA
outputs = llm.generate(
    ["分析这家公司的财报"],
    SamplingParams(max_tokens=256),
    lora_request=finance_lora,         # 用金融 LoRA
)

outputs = llm.generate(
    ["解读这份CT报告"],
    SamplingParams(max_tokens=256),
    lora_request=medical_lora,         # 用医疗 LoRA
)
```

### 13.3 LoRA 多租户的价值
```
场景：SaaS 平台需要为不同客户提供定制化模型

传统方式：
  客户A → 部署完整模型A（14GB）
  客户B → 部署完整模型B（14GB）
  客户C → 部署完整模型C（14GB）
  总计：42GB 显存

LoRA 方式：
  基座模型（14GB）+ LoRA-A（50MB）+ LoRA-B（50MB）+ LoRA-C（50MB）
  总计：~14.15GB 显存

节省 66% 显存！
```

> ⚠️ LoRA 适配器需提前训练，vLLM 只负责推理阶段的加载和切换。

## 小结

```
vLLM 全流程：
安装 → LLM()加载 → llm.chat/generate → 或 vllm serve 起服务 → Agent 接 base_url
```

**核心收获**：vLLM 用 PagedAttention + Continuous Batching 实现高吞吐。
`vllm serve` 一键提供 OpenAI 兼容服务，是生产环境的标准部署方式。
