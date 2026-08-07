# 07 · 模型服务化与 API 封装

> 难度：★★★ | 目的：把模型封装成标准 HTTP 服务，供任何语言/客户端调用
> 服务化 = 部署的最后一步，让模型从"本地脚本"变成"产品接口"

---

## 目录

1. [为什么需要服务化](#1-为什么需要服务化)
2. [方案选择](#2-方案选择)
3. [FastAPI 封装 LLM](#3-fastapi-封装-llm)
4. [封装 Ollama（代理模式）](#4-封装-ollama代理模式)
5. [流式响应（SSE）](#5-流式响应sse)
6. [并发与性能](#6-并发与性能)
7. [Docker 容器化](#7-docker-容器化)
8. [环境变量与配置管理](#8-环境变量与配置管理)
9. [安全与认证](#9-安全与认证)
10. [完整示例：RAG 服务](#10-完整示例rag-服务)
11. [异步 FastAPI 模式](#11-异步-fastapi-模式)
12. [生产部署进阶](#12-生产部署进阶)

---

## 1. 为什么需要服务化

```
本地脚本的局限：
1. 只有 Python 能调用
2. 每次调用都要重新加载模型（慢）
3. 无法多用户并发
4. 无法远程访问

服务化的好处：
┌─────────────────────────────────────┐
│  HTTP API（标准协议）                │
│  → 任何语言（Java/Go/JS）都能调用    │
│  → 模型常驻内存，响应快              │
│  → 支持并发请求                      │
│  → 可以部署到服务器/云              │
└─────────────────────────────────────┘
```

**设计原则**：模型进程常驻，API 只做"转发"。
模型加载一次，服务所有请求。

## 2. 方案选择

| 方案 | 场景 | 是否需要写代码 |
|------|------|--------------|
| `ollama serve` | 本地快速服务 | 否（自带 OpenAI 接口） |
| `vllm serve` | 生产高性能 | 否（自带 OpenAI 接口） |
| **FastAPI + transformers** | 自定义逻辑 | 是 |
| **FastAPI + 代理 Ollama** | 自定义 + 加逻辑 | 是（少量） |
| Triton/TensorRT | 企业级 | 否（配置复杂） |

> 如果只需要标准 OpenAI 接口 → 直接用 `ollama serve` / `vllm serve`，零代码。
> 如果需要自定义逻辑（RAG、鉴权、路由、多模型）→ FastAPI 封装。

## 3. FastAPI 封装 LLM

### 3.1 安装
```bash
pip install fastapi uvicorn
```

### 3.2 最简单的 LLM 服务
```python
# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# ---- 启动时加载模型（只加载一次） ----
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, torch_dtype=torch.bfloat16, device_map="auto"
)

app = FastAPI(title="LLM 推理服务")

# ---- 请求/响应模型 ----
class ChatRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 256
    temperature: float = 0.7

class ChatResponse(BaseModel):
    answer: str

# ---- 接口 ----
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """聊天接口"""
    messages = [{"role": "user", "content": req.prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=req.max_new_tokens,
            do_sample=req.temperature > 0,
            temperature=req.temperature if req.temperature > 0 else 1.0,
            pad_token_id=tokenizer.eos_token_id,
        )
    answer = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    return ChatResponse(answer=answer)

@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}

# ---- 启动：uvicorn app:app --host 0.0.0.0 --port 8000 ----
```

### 3.3 启动服务
```bash
# 单进程
uvicorn app:app --host 0.0.0.0 --port 8000

# 开发模式（改代码自动重启）
uvicorn app:app --reload

# 生产（多worker，注意模型会加载多次）
uvicorn app:app --workers 2
```

### 3.4 客户端调用
```python
import requests

resp = requests.post("http://localhost:8000/chat", json={
    "prompt": "什么是装饰器？",
    "max_new_tokens": 200,
})
print(resp.json()["answer"])
```

## 4. 封装 Ollama（代理模式）

把自定义逻辑（RAG、缓存、日志、限流）加在 Ollama 前面：

```python
# proxy.py —— Ollama 代理服务
from fastapi import FastAPI, Request
from openai import OpenAI
import time

app = FastAPI(title="LLM 代理服务")

# 指向底层 Ollama
llm = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

@app.post("/v1/chat/completions")
async def chat_completions(req: Request):
    body = await req.json()

    # 自定义逻辑：记录请求
    start = time.time()
    print(f"[LOG] 收到请求: {body.get('messages', [{}])[0].get('content', '')[:50]}")

    # 转发给 Ollama（保持 OpenAI 兼容格式）
    response = llm.chat.completions.create(
        model=body.get("model", "qwen2.5:7b"),
        messages=body.get("messages", []),
        stream=body.get("stream", False),
    )

    # 自定义逻辑：性能监控
    print(f"[LOG] 响应耗时: {time.time() - start:.2f}s")

    if body.get("stream"):
        return StreamingResponse(generate_stream(response), media_type="text/event-stream")
    return response
```

## 5. 流式响应（SSE）

### 5.1 什么是 SSE
```
SSE (Server-Sent Events)：HTTP 长连接，服务端分块推送文本

客户端收到的格式：
data: {"choices":[{"delta":{"content":"你"}}]}

data: {"choices":[{"delta":{"content":"好"}}]}
```

### 5.2 FastAPI 流式转发
```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from openai import OpenAI

app = FastAPI()
llm = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def generate_stream(response):
    """把 OpenAI 流式响应转发为 SSE 格式"""
    for chunk in response:
        # chunk 是 OpenAI SDK 的对象，转成 JSON 行
        data = chunk.model_dump_json()
        yield f"data: {data}\n\n"
    yield "data: [DONE]\n\n"

@app.post("/v1/chat/completions")
async def chat(req: Request):
    body = await req.json()
    stream = body.get("stream", False)

    response = llm.chat.completions.create(
        model=body.get("model", "qwen2.5:7b"),
        messages=body.get("messages", []),
        stream=True,               # 底层强制流式
    )

    if stream:
        return StreamingResponse(
            generate_stream(response),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )
    else:
        # 非流式：聚合完整内容
        full = ""
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                full += chunk.choices[0].delta.content
        return {"choices": [{"message": {"role": "assistant", "content": full}}]}
```

### 5.3 前端/客户端消费 SSE
```python
import requests, json

resp = requests.post(
    "http://localhost:8000/v1/chat/completions",
    json={"model": "qwen2.5:7b", "messages": [{"role": "user", "content": "你好"}], "stream": True},
    stream=True,
)

for line in resp.iter_lines():
    if not line or line.startswith(b":"):
        continue
    line = line.decode("utf-8").removeprefix("data: ")
    if line == "[DONE]":
        break
    data = json.loads(line)
    delta = data["choices"][0]["delta"].get("content", "")
    print(delta, end="", flush=True)
print()
```

## 6. 并发与性能

### 6.1 关键认知：模型推理是 CPU/GPU 密集的
```
FastAPI 可以轻松处理 1000 并发 HTTP 连接
但底层模型同一时刻只能算有限个请求

瓶颈在模型，不在 Web 框架！

解决方案：
1. 单模型 + 排队（uvicorn 默认排队）
2. 多模型实例 + 负载均衡
3. 用 vLLM 的 Continuous Batching（吞吐更高）
```

### 6.2 线程安全
```python
# ⚠️ 模型推理期间要加锁，防止并发冲突
import threading

lock = threading.Lock()

@app.post("/chat")
def chat(req: ChatRequest):
    with lock:                       # 同一时刻只推理一个
        ... # 模型推理
    return answer

# 更好的方式：用独立的推理线程池
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=1)  # 模型只能串行

def run_inference(prompt):
    ...  # 模型推理
    return answer
```

### 6.3 加载速度优化
```python
# 模型加载很慢（7B 约 30 秒），生产环境建议：
# 1. 启动时预加载（模块级加载，如第3节）
# 2. 保存为本地模型，避免联网
# 3. 使用 vLLM（加载更快，还有模型常驻）
```

### 6.4 线程安全（重要）

⚠️ **模型推理期间必须加锁**，防止并发请求导致显存冲突或输出错乱。

```python
import threading

model_lock = threading.Lock()

@app.post("/chat")
def chat(req: ChatRequest):
    with model_lock:                    # 同一时刻只推理一个
        return run_inference(req.prompt)
```

### 6.5 异步模式（推荐）

同步 `def` 会阻塞 FastAPI 的 event loop，导致 health check 等轻量请求也被卡住。
用 `async def` + `run_in_executor` 解决：

```python
from concurrent.futures import ThreadPoolExecutor
import asyncio

# 单线程推理池（因为模型只能串行，多线程无意义）
inference_pool = ThreadPoolExecutor(max_workers=1)

async def async_inference(prompt: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(inference_pool, run_inference, prompt)

@app.post("/chat")
async def chat(req: ChatRequest):           # async def
    answer = await async_inference(req.prompt)
    return {"answer": answer}

@app.get("/health")
async def health():                         # 轻量请求不阻塞
    return {"status": "ok"}
```

> **原理**：`run_in_executor` 把模型推理放进独立线程，不阻塞主 event loop。
> `max_workers=1` 确保模型串行推理（防止显存冲突）。

## 7. Docker 容器化

### 7.1 Dockerfile
```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install fastapi uvicorn

# 复制代码和模型
COPY app.py .
COPY ./models ./models          # 本地模型直接打进镜像

# 环境变量
ENV HF_ENDPOINT=https://hf-mirror.com
ENV MODEL_PATH=./models/qwen2.5-1.5b

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 7.2 构建与运行
```bash
# 构建
docker build -t llm-service .

# 运行（映射端口）
docker run -d -p 8000:8000 --gpus all --name llm llm-service

# 查看日志
docker logs -f llm
```

### 7.3 模型放镜像 vs 挂载卷
```yaml
# docker-compose.yml（模型用卷挂载，避免打进镜像）
services:
  llm:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models      # 模型挂载
      - ./.ollama:/root/.ollama   # Ollama 缓存挂载
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

## 8. 环境变量与配置管理

```python
import os
from dataclasses import dataclass

@dataclass
class Config:
    """集中配置管理"""
    model_name: str = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-1.5B-Instruct")
    model_path: str = os.getenv("MODEL_PATH", "./models")
    port: int = int(os.getenv("PORT", "8000"))
    host: str = os.getenv("HOST", "0.0.0.0")
    max_tokens: int = int(os.getenv("MAX_TOKENS", "512"))
    api_key: str = os.getenv("API_KEY", "")     # 认证密钥

config = Config()
```

## 9. 安全与认证

### 9.1 API Key 认证（简单中间件）
```python
from fastapi import FastAPI, Header, HTTPException
import secrets

API_KEY = "your-secret-key"   # 应从环境变量读取

app = FastAPI()

@app.post("/chat")
def chat(req: ChatRequest, authorization: str = Header(None)):
    # 校验 Bearer Token
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="未授权")
    ...
```

### 9.2 安全清单
```
✅ 必须做：
   - API Key / JWT 认证
   - HTTPS（生产环境）
   - 输入长度限制（防超长请求）
   - 速率限制（防滥用）

⚠️ 注意：
   - 不把 API Key 写在代码里（用环境变量）
   - 不把模型服务直接暴露公网
   - Prompt 注入防护（用户输入可能包含恶意指令）
   - 日志脱敏（不记录敏感对话）
```

### 9.3 限流（Rate Limit）
```python
# pip install slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/chat")
@limiter.limit("10/minute")      # 每 IP 每分钟 10 次
def chat(req: ChatRequest):
    ...
```

## 10. 完整示例：RAG 服务

```python
# rag_service.py —— 一个带 RAG 的完整推理服务
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import numpy as np

# ---------- 初始化 ----------
embedder = SentenceTransformer("BAAI/bge-small-zh-v1.5")
llm = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 知识库
documents = [
    "Python 装饰器用于增强函数功能。",
    "生成器使用 yield 节省内存。",
    "asyncio 适合 IO 密集型任务。",
]
doc_vectors = embedder.encode(documents, normalize_embeddings=True)

app = FastAPI(title="RAG 问答服务")

class AskRequest(BaseModel):
    question: str
    model: str = "qwen2.5:7b"

# ---------- 接口 ----------
@app.post("/ask")
def ask(req: AskRequest):
    # 1. 检索
    q_vec = embedder.encode(req.question, normalize_embeddings=True)
    scores = doc_vectors @ q_vec
    top_idx = scores.argsort()[::-1][:2]
    context = "\n".join([documents[i] for i in top_idx])

    # 2. 生成
    response = llm.chat.completions.create(
        model=req.model,
        messages=[
            {"role": "system", "content": "只根据参考资料回答。"},
            {"role": "user", "content": f"参考资料：\n{context}\n\n问题：{req.question}"},
        ],
    )
    return {"answer": response.choices[0].message.content, "context": context}
```

## 11. 异步 FastAPI 模式

### 11.1 同步 vs 异步对比
```
同步 def chat():       → 阻塞整个 event loop → health check 也会卡住
async def chat():      → 推理在独立线程 → event loop 继续处理其他请求

生产环境强烈建议用 async，用户体验差异显著。
```

### 11.2 WebSocket 流式对话（进阶）
```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        # 接收用户消息
        data = await websocket.receive_text()
        
        # 流式返回 LLM 响应
        stream = llm.chat.completions.create(
            model="qwen2.5:7b",
            messages=[{"role": "user", "content": data}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                await websocket.send_text(chunk.choices[0].delta.content)
        
        await websocket.send_text("[DONE]")
```

> WebSocket 适合需要双向实时通信的场景（如聊天机器人前端）。

### 11.3 后台任务（长时间推理不阻塞）
```python
from fastapi import BackgroundTasks
import uuid

tasks_store = {}  # 存储任务状态

@app.post("/async-generate")
async def async_generate(prompt: str, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks_store[task_id] = {"status": "processing"}
    
    def run():
        result = run_inference(prompt)
        tasks_store[task_id] = {"status": "done", "result": result}
    
    background_tasks.add_task(run)
    return {"task_id": task_id, "status": "processing"}

@app.get("/task/{task_id}")
async def get_task(task_id: str):
    return tasks_store.get(task_id, {"status": "not_found"})
```

## 12. 生产部署进阶

### 12.1 负载均衡（多实例）
生产环境单实例容易成为瓶颈，用 Nginx 做反向代理 + 多模型实例：

```nginx
# nginx.conf
upstream llm_backend {
    # 轮询分发请求
    server 127.0.0.1:8001 weight=1;
    server 127.0.0.1:8002 weight=1;
    server 127.0.0.1:8003 weight=2;  # 更强的 GPU 设更高权重
    
    # 健康检查（Nginx Plus 或 nginx-upsync-module）
    # check interval=3000 rise=2 fall=3 timeout=1000;
}

server {
    listen 8000;
    
    location / {
        proxy_pass http://llm_backend;
        proxy_read_timeout 300s;        # LLM 推理可能很慢
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

启动多实例：
```bash
# GPU 0 启动实例1（模型自动绑定 GPU 0）
CUDA_VISIBLE_DEVICES=0 uvicorn app:app --port 8001 &

# GPU 1 启动实例2
CUDA_VISIBLE_DEVICES=1 uvicorn app:app --port 8002 &
```

### 12.2 优雅关闭（Graceful Shutdown）
```python
import signal, sys

def cleanup():
    """释放 GPU 资源"""
    print("\n[SHUTDOWN] 正在卸载模型，释放显存...")
    if hasattr(model, 'cpu'):
        model.cpu()
    del model
    import torch
    torch.cuda.empty_cache()
    print("[SHUTDOWN] 模型已卸载，服务关闭")

# 注册信号处理
signal.signal(signal.SIGINT, lambda s, f: (cleanup(), sys.exit(0)))
signal.signal(signal.SIGTERM, lambda s, f: (cleanup(), sys.exit(0)))

# 或者在 FastAPI 事件中处理
@app.on_event("shutdown")
async def shutdown_event():
    cleanup()
```

### 12.3 监控与指标（Prometheus）
```python
# pip install prometheus-fastapi-instrumentator
from prometheus_fastapi_instrumentator import Instrumentator

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# 访问 http://localhost:8000/metrics 即可拿到 Prometheus 指标
# 包含：请求数、延迟分布、错误率等
```

**生产环境必看指标：**
```
http_request_duration_seconds_bucket   → P50/P95/P99 延迟
http_requests_total                     → 每秒请求数
http_requests_total{status="500"}       → 错误率
```

### 12.4 请求日志中间件
```python
import time
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    
    # 结构化日志（方便后续 ELK/Loki 采集）
    print(f"[{response.status_code}] {request.method} {request.url.path} - {duration:.2f}s")
    
    return response
```

### 12.5 CORS 配置（前端调用）
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],   # 生产环境指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 12.6 生产部署全景架构
```
┌─────────────────────────────────────────────────────┐
│                    用户/客户端                         │
└────────────┬────────────────────────────────────────┘
             │ HTTPS
┌────────────▼────────────────────────────────────────┐
│               Nginx（反向代理 + SSL）                  │
│         负载均衡 │ 限流 │ 静态资源 │ 日志               │
└───────┬──────────────────┬──────────────────────────┘
        │                  │
┌───────▼──────┐   ┌───────▼──────┐
│ FastAPI:8001 │   │ FastAPI:8002 │    ← 多实例
│ GPU 0        │   │ GPU 1        │
│ (模型推理)    │   │ (模型推理)    │
└──────────────┘   └──────────────┘
        │                  │
┌───────▼──────────────────▼──────┐
│        Prometheus + Grafana      │    ← 监控
└─────────────────────────────────┘
```

### 12.7 部署检查清单
```
上线前自检（逐项打勾）：
□ 异步模式启用（async def + run_in_executor）
□ 模型推理有锁保护（threading.Lock）
□ 优雅关闭实现（SIGTERM 释放显存）
□ 健康检查端点正常（/health 返回 ok）
□ 监控指标暴露（/metrics 可访问）
□ 日志结构化（状态码/方法/路径/耗时）
□ CORS 配置正确（仅允许合法域名）
□ 认证生效（无 Key 返回 401）
□ 限流生效（超频请求返回 429）
□ 请求超时配置（proxy_read_timeout 足够长）
□ 环境变量管理（密钥不在代码中）
```

---

## 小结

```
服务化全流程：
模型加载一次 → FastAPI 定义接口 → 转发/增强 → uvicorn 启动 → Docker 部署
```

**核心收获**：
1. 模型**常驻内存** + HTTP 接口 = 服务化
2. 流式用 SSE（`StreamingResponse`）
3. 生产环境：认证 + 限流 + Docker + 环境变量
4. 模型是瓶颈，Web 框架不是
