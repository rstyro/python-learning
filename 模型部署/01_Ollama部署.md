# 01 · Ollama 部署详解

> 难度：⭐ 最简单 | 目的：一行命令在本地跑起开源大模型
> Ollama 是目前个人部署大模型的事实标准，内置 llama.cpp 引擎 + GPU 加速 + OpenAI 兼容接口

---

## 目录

1. [Ollama 是什么](#1-ollama-是什么)
2. [安装 Ollama](#2-安装-ollama)
3. [下载与运行模型](#3-下载与运行模型)
4. [命令行日常操作](#4-命令行日常操作)
5. [Python 库调用](#5-python-库调用)
6. [流式输出](#6-流式输出)
7. [OpenAI 兼容接口（接入 Agent）](#7-openai-兼容接口接入-agent)
8. [Function Calling（工具调用）](#8-function-calling工具调用)
9. [Modelfile 自定义模型](#9-modelfile-自定义模型)
10. [性能与高级配置](#10-性能与高级配置)
11. [Ollama 嵌入模型（Embedding）](#11-ollama-嵌入模型embedding)
12. [多模态模型支持](#12-多模态模型支持)

---

## 1. Ollama 是什么

```
┌─────────────────────────────────────────────────┐
│                  你的 Python 代码                 │
│         ollama库 / OpenAI库 / requests           │
└────────────────────┬────────────────────────────┘
                     │ HTTP (11434端口)
┌────────────────────▼────────────────────────────┐
│              Ollama 服务（守护进程）               │
│  ┌─────────────┐  ┌──────────────────────────┐  │
│  │ 模型管理器    │  │ llama.cpp 推理引擎         │  │
│  │ 下载/缓存/加载│  │ GPU(CUDA) + CPU 混合计算   │  │
│  └─────────────┘  └──────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

**关键理解**：
- Ollama 分两部分：**服务端**（负责下载、加载、推理模型）+ **客户端**（CLI 命令或 Python 库）
- 模型文件缓存在 `~/.ollama/models`，一次下载永久复用
- 服务端在后台运行，监听 `127.0.0.1:11434`
- Python 库 `ollama` 只是客户端，**必须依赖服务端运行**

## 2. 安装 Ollama

### Windows
1. 访问官网 https://ollama.com/download/windows
2. 下载 `OllamaSetup.exe`，双击安装（会安装到 `%LOCALAPPDATA%\Programs\Ollama`）
3. 安装完成后，托盘区会出现 Ollama 图标（服务已自动启动）
4. 打开新的终端，验证：
   ```bash
   ollama --version        # 看到版本号即成功
   ```

### macOS
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Docker（服务器部署）
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
# GPU 支持需加 --gpus=all
```

### 验证服务是否运行
```bash
# 命令行验证
ollama list

# 或浏览器访问（应返回 JSON）
http://127.0.0.1:11434
```

## 3. 下载与运行模型

### 3.1 搜索有哪些模型
- 官网模型库：https://ollama.com/library
- 常用模型速查：

| 模型 | 命令 | 中文能力 | 显存(量化后) |
|------|------|---------|-------------|
| Qwen2.5 系列 | `ollama pull qwen2.5:7b` | 强 | 7B≈4.4GB / 3B≈2GB / 1.5B≈1.1GB |
| Llama 3.x | `ollama pull llama3.2` | 一般 | 3B≈2GB |
| DeepSeek-R1 | `ollama pull deepseek-r1:7b` | 强(推理型) | 7B≈4.5GB |
| Mistral | `ollama pull mistral` | 一般 | 7B≈4.4GB |
| 中文专用 | `ollama pull qwen2.5:7b` | 强 | 见上 |

### 3.2 下载模型（一条命令）
```bash
# 拉取模型（会自动选择合适的量化版本）
ollama pull qwen2.5:7b

# 指定标签（不同量化/尺寸）
ollama pull qwen2.5:3b       # 3B 模型
ollama pull qwen2.5:1.5b     # 1.5B 模型
ollama pull qwen2.5:14b      # 14B 模型（需要大显存）
```

> 国内下载慢？设置镜像环境变量（可选）：
> ```bash
> # Windows PowerShell
> $env:OLLAMA_MODELS = "D:\ollama-models"   # 可选：模型存到指定盘
> ollama pull qwen2.5:7b
> ```
> 若官方源极慢，可改用 ModelScope 下载再导入（见第 9 节 Modelfile 导入）

### 3.3 运行模型（交互式对话）
```bash
# 直接在终端对话（q 或 Ctrl+D 退出）
ollama run qwen2.5:7b

# 对话示例
>>> 你好，介绍一下你自己
>>> /exit                       # 退出
```

### 3.4 带参数运行
```bash
# 设置温度、上下文长度
ollama run qwen2.5:7b --temperature 0.3 --num-ctx 8192
```

## 4. 命令行日常操作

```bash
ollama list              # 列出已下载的模型
ollama pull <模型>        # 下载模型
ollama rm <模型>          # 删除模型（释放磁盘）
ollama cp <模型> <新名>   # 复制模型（Modelfile 继承用）
ollama show <模型>        # 查看模型详情（参数、量化、上下文）
ollama ps                # 查看当前加载在内存/显存中的模型
ollama stop <模型>        # 卸载已加载的模型（释放显存）
ollama serve             # 前台启动服务（排错用）
```

## 5. Python 库调用

### 5.1 安装客户端库
```bash
pip install ollama
```

### 5.2 基础对话
```python
import ollama

# 最简单的调用
response = ollama.chat(
    model="qwen2.5:7b",
    messages=[
        {"role": "user", "content": "什么是装饰器？"}
    ]
)

print(response["message"]["content"])
```

### 5.3 多轮对话（记忆）
```python
import ollama

messages = [{"role": "system", "content": "你是 Python 专家，用中文简洁回答"}]

while True:
    user_input = input("\n你: ")
    if user_input == "quit":
        break
    messages.append({"role": "user", "content": user_input})
    response = ollama.chat(model="qwen2.5:7b", messages=messages)
    reply = response["message"]["content"]
    print(f"AI: {reply}")
    messages.append({"role": "assistant", "content": reply})
```

### 5.4 结构化参数
```python
import ollama

response = ollama.chat(
    model="qwen2.5:7b",
    messages=[{"role": "user", "content": "写一首关于春天的诗"}],
    options={
        "temperature": 0.7,    # 创造性
        "top_p": 0.9,
        "num_predict": 200,    # 最多生成 200 tokens
        "seed": 42,            # 固定随机种子（可复现）
    }
)
print(response["message"]["content"])
```

## 6. 流式输出

```python
import ollama

# stream=True 逐字返回（打字机效果）
stream = ollama.chat(
    model="qwen2.5:7b",
    messages=[{"role": "user", "content": "用 500 字介绍 Python"}],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
print()
```

**关键点**：流式时每个 chunk 都是一个完整 dict，格式：
```python
{"model": "qwen2.5:7b", "message": {"role": "assistant", "content": "你"}, "done": False}
```
- `done: False` = 还在生成
- 最后一个 chunk `done: True`，且带 `eval_count`（用了多少token）和 `eval_duration`（耗时）

## 7. OpenAI 兼容接口（接入 Agent）

**这是最值钱的功能**：Ollama 提供了 OpenAI 格式的 API，`http://localhost:11434/v1`。
你的 Agent 代码从"调用 DeepSeek 云端"切换到"调用本地模型"，**只改一行 base_url**：

```python
from openai import OpenAI

# 云端版本：client = OpenAI(api_key="sk-xxx", base_url="https://api.deepseek.com")
# 本地版本：↓
client = OpenAI(
    api_key="ollama",                          # 任意值，本地不校验
    base_url="http://localhost:11434/v1"       # 指向本地 Ollama
)

response = client.chat.completions.create(
    model="qwen2.5:7b",
    messages=[{"role": "user", "content": "你好"}],
    stream=True                                # 流式同样支持
)
for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

**其他兼容端点**：
```
GET  /v1/models                          # 列出模型
POST /v1/chat/completions                # 对话（含 tools 参数）
POST /v1/embeddings                      # 文本向量化
```

## 8. Function Calling（工具调用）

新版 Qwen / Llama 3.1+ 原生支持工具调用，Ollama 直接透传 `tools` 参数：

```python
import ollama, json

# 定义工具（JSON Schema，与 OpenAI 格式完全一致）
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取城市天气",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"]
            }
        }
    }
]

def get_weather(city: str) -> str:
    weather = {"北京": "晴天 28°C", "上海": "多云 32°C"}
    return json.dumps(weather.get(city, "未知城市"), ensure_ascii=False)

# 第一轮：LLM 决定调用工具
response = ollama.chat(
    model="qwen2.5:7b",
    messages=[{"role": "user", "content": "北京天气怎么样？"}],
    tools=tools,
)

# 提取工具调用
tool_calls = response["message"].get("tool_calls", [])
if tool_calls:
    for tc in tool_calls:
        fn = tc["function"]
        result = get_weather(**json.loads(fn["arguments"]))
        # 第二轮：把结果反馈给 LLM
        response2 = ollama.chat(
            model="qwen2.5:7b",
            messages=[
                {"role": "user", "content": "北京天气怎么样？"},
                response["message"],                          # 保留 LLM 的工具调用消息
                {"role": "tool", "content": result, "tool_name": fn["name"]},  # 工具结果
            ],
            tools=tools,
        )
        print(response2["message"]["content"])   # 最终回答
```

> 注意：Ollama 的 tool 消息格式是 `{"role": "tool", "content": "...", "tool_name": "..."}`，
> 与 OpenAI 的 `tool_call_id` 略不同，写兼容层时留意。

## 9. Modelfile 自定义模型

Modelfile 类似 Dockerfile，用来定制模型行为（系统提示词、参数、导入 GGUF）：

### 9.1 创建自定义模型
```dockerfile
# Modelfile
FROM qwen2.5:7b          # 基于哪个模型

# 设置系统提示词（相当于 Agent 的 system prompt）
SYSTEM 你是一个Python编程导师，回答要简洁并带代码示例。

# 修改默认参数
PARAMETER temperature 0.3
PARAMETER num_ctx 8192
```

```bash
# 构建自定义模型
ollama create python-tutor -f Modelfile

# 使用
ollama run python-tutor
```

### 9.2 从 GGUF 文件导入（从 HuggingFace 手动下载的场景）
```dockerfile
# Modelfile
FROM ./qwen2.5-7b-q4_k_m.gguf
```

```bash
ollama create qwen-from-gguf -f Modelfile
```

### 9.3 从 ModelScope 下载导入（国内加速）
```bash
# 1. 安装 modelscope
pip install modelscope

# 2. 下载 GGUF 模型（脚本方式）
python -c "from modelscope import snapshot_download; snapshot_download('Qwen/Qwen2.5-7B-Instruct-GGUF', local_dir='./qwen-gguf')"

# 3. 写 Modelfile 导入
echo "FROM ./qwen-gguf/qwen2.5-7b-instruct-q4_k_m.gguf" > Modelfile
ollama create qwen-local -f Modelfile
```

## 10. 性能与高级配置

### 10.1 常用环境变量（Windows 设置方式）
```bash
# 模型存放位置（默认在 C 盘用户目录）
$env:OLLAMA_MODELS = "D:\ollama\models"

# 并发请求数（默认1，一次只跑一个模型）
$env:OLLAMA_NUM_PARALLEL = "4"

# 上下文窗口大小（默认 2048）
$env:OLLAMA_CONTEXT_LENGTH = "8192"

# 允许外部访问（默认只允许本机）
$env:OLLAMA_HOST = "0.0.0.0"

# 模型保持加载时间（默认5分钟自动卸载）
$env:OLLAMA_KEEP_ALIVE = "24h"            # 24小时内不卸载
$env:OLLAMA_KEEP_ALIVE = "-1"             # 永久常驻（开发环境推荐）
```

设置后重启 Ollama 生效。

### 10.2 模型常驻策略（KEEP_ALIVE）
Ollama 默认在模型闲置 5 分钟后自动从显存卸载，下次请求需重新加载（耗时数十秒）。

**开发/服务场景强烈建议设置：**
```bash
# Windows PowerShell（永久常驻）
$env:OLLAMA_KEEP_ALIVE = "-1"

# 或设置合理时长
$env:OLLAMA_KEEP_ALIVE = "24h"

# 启动时预加载模型（warm up）
ollama run qwen2.5:7b ""       # 发空消息触发加载
```

设置后重启 Ollama 生效。常驻会持续占用显存，需根据实际显存决定。

### 10.3 多模型并发加载
Ollama 默认同时只加载一个模型（切换模型时卸载旧模型）。如需同时加载多个模型：

```bash
$env:OLLAMA_MAX_LOADED_MODELS = "3"    # 最多同时加载3个模型
```

> 注意：每个模型都占用显存，多个模型同时加载需确保显存足够。

### 10.4 显存与内存策略
- 模型加载优先用显存（GPU 加速）
- 显存不够时自动卸载部分层到内存（CPU 计算），速度变慢但不崩
- `ollama ps` 可查看当前负载分布

### 10.5 低显存跑大模型的技巧
```bash
# 1. 用更小的量化（q2_k 比 q4 更省）
ollama pull qwen2.5:7b-q2_K

# 2. 用更小尺寸模型
ollama pull qwen2.5:3b

# 3. 运行时限制上下文（上下文也吃显存）
ollama run qwen2.5:7b --num-ctx 2048
```

### 10.6 Ollama 常见报错速查

| 报错 | 原因 | 解决 |
|------|------|------|
| `could not connect to default ollama client` | 服务未启动 | 重启 Ollama 托盘程序 / `ollama serve` |
| `model not found` | 模型未下载 | 先 `ollama pull` |
| `out of memory` | 显存不足 | 换小模型 / 小量化 / 减小 num_ctx |
| `cuda error: out of memory` | GPU 显存溢出 | 同上，或加 `--num-gpu 0` 强制 CPU |
| 下载卡住 | 网络问题 | 重试 / 换镜像 / Modelfile 导入 |

---

## 11. Ollama 嵌入模型（Embedding）

Ollama 除对话模型外，也内置了嵌入模型，可用于 RAG 知识库的文本向量化。

### 11.1 安装嵌入模型
```bash
# 轻量英文/多语言（~270MB，768维）
ollama pull nomic-embed-text

# 中英文多语言（~2GB，1024维，推荐）
ollama pull bge-m3

# 查看已安装
ollama list
```

### 11.2 Python 调用（OpenAI 兼容接口）
```python
from openai import OpenAI

client = OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)

# 生成向量
response = client.embeddings.create(
    model="bge-m3",
    input=["今天天气真好", "Python 是一种编程语言"],
)

# 提取向量
vectors = [item.embedding for item in response.data]
print(f"向量数量: {len(vectors)}, 维度: {len(vectors[0])}")
# 输出：向量数量: 2, 维度: 1024
```

### 11.3 语义相似度示例
```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

r = client.embeddings.create(model="bge-m3", input=["今天天气真好", "外边阳光明媚", "Python编程语言"])
a, b, c = [item.embedding for item in r.data]

print(f"'天气' vs '阳光': {cosine_similarity(a, b):.4f}")   # 高（语义相近）
print(f"'天气' vs 'Python': {cosine_similarity(a, c):.4f}")  # 低（语义无关）
```

### 11.4 与 RAG 集成
```python
# 完整 RAG 管道：嵌入模型做向量检索 + LLM 做生成
# 详见 06_嵌入模型与RAG.md，这里只展示嵌入模型可以完全用 Ollama 替代
```

> **提示**：Ollama 的嵌入端点完全兼容 OpenAI `/v1/embeddings` 格式。
> 如果你已有用 OpenAI embeddings 的代码，只需改 `base_url` 即可切换到本地。

## 12. 多模态模型支持

Ollama 支持视觉语言模型（VLM），可以理解图片内容。

### 12.1 安装多模态模型
```bash
# llava 系列（经典开源视觉模型）
ollama pull llava:13b

# 或 Qwen2.5-VL（中文视觉能力强）
# 需检查 Ollama 模型库是否有对应版本
```

### 12.2 Python 调用（图片理解）
```python
import ollama

# 传入本地图片路径
response = ollama.chat(
    model="llava:13b",
    messages=[{
        "role": "user",
        "content": "描述这张图片的内容",
        "images": ["./photo.jpg"]       # 本地图片路径
    }]
)
print(response["message"]["content"])
```

### 12.3 图片 Base64 传入
```python
import base64, ollama

with open("./photo.jpg", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

response = ollama.chat(
    model="llava:13b",
    messages=[{
        "role": "user",
        "content": "图片里有什么？",
        "images": [img_b64]
    }]
)
```

> 多模态模型对显存要求较高（llava:13b 约需 8-10GB），低显存请使用量化版本或更小的视觉模型。

---

## 小结

```
Ollama 全流程：
安装 → ollama pull qwen2.5:7b → ollama run 或 Python 调用
     → 需要工具调用？传 tools 参数
     → 需要接入 Agent？base_url 指向 http://localhost:11434/v1
```

**核心收获**：Ollama = 服务端（跑模型）+ 客户端（调用）。
5 分钟就能跑起一个支持流式、工具调用、OpenAI 兼容的本地模型服务。
