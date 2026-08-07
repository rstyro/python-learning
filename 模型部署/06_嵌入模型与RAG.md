# 06 · 嵌入模型部署与 RAG 应用

> 难度：★ | 目的：部署文本向量化模型，构建 RAG 知识库
> 嵌入模型（Embedding Model）是大模型应用的基础设施，让机器理解"语义相似"

---

## 目录

1. [嵌入模型是什么](#1-嵌入模型是什么)
2. [主流嵌入模型对比](#2-主流嵌入模型对比)
3. [安装依赖](#3-安装依赖)
4. [快速上手 sentence-transformers](#4-快速上手-sentence-transformers)
5. [语义相似度检索](#5-语义相似度检索)
6. [构建 RAG 知识库](#6-构建-rag-知识库)
7. [向量数据库选型](#7-向量数据库选型)
8. [中文模型特别说明](#8-中文模型特别说明)
9. [OpenAI 兼容嵌入服务](#9-openai-兼容嵌入服务)
10. [性能优化](#10-性能优化)
11. [Reranker 精排模型](#11-reranker-精排模型)
12. [混合检索：BM25 + 向量](#12-混合检索bm25--向量)
13. [高级文本切分策略](#13-高级文本切分策略)

---

## 1. 嵌入模型是什么

```
嵌入模型的作用：把文本变成一串数字（向量）

"苹果很好吃"  →  [0.12, -0.35, 0.78, ...]  (1024维向量)
"香蕉真美味"  →  [0.15, -0.31, 0.74, ...]  ← 语义相近 → 向量距离近
"宇宙飞船"    →  [-0.9, 0.45, 0.12, ...]   ← 语义无关 → 向量距离远
```

### 为什么需要嵌入模型
```
RAG（检索增强生成）的核心流程：
用户问题 → 嵌入成向量 → 在知识库找最相似的文本 → 拼给 LLM → 回答

没有嵌入模型，机器无法判断"哪段文档和用户问题最相关"
```

### 与生成模型（LLM）的区别
| 对比 | 嵌入模型 | 生成模型(LLM) |
|------|---------|--------------|
| 输入 | 文本 | 文本 |
| 输出 | 向量（数字） | 文本 |
| 大小 | 100MB~1GB | 2~200GB |
| 显存需求 | 很小 | 很大 |
| 用途 | 检索/分类/聚类 | 生成/对话 |

## 2. 主流嵌入模型对比

### 2.1 中文场景推荐
| 模型 | 大小 | 维度 | 特点 |
|------|------|------|------|
| **bge-small-zh-v1.5** | ~100MB | 512 | 轻量、中文好、推荐 |
| **bge-base-zh-v1.5** | ~400MB | 768 | 效果更好 |
| **bge-large-zh-v1.5** | ~1.3GB | 1024 | 最强（需 GPU） |
| text2vec-base-chinese | ~400MB | 768 | 中文经典 |
| Qwen3-Embedding | ~4GB | 4096 | 最新旗舰 |

### 2.2 英文/多语言
| 模型 | 大小 | 特点 |
|------|------|------|
| all-MiniLM-L6-v2 | ~90MB | 快、小、经典 |
| sentence-transformers/all-mpnet-base-v2 | ~440MB | 效果均衡 |
| multilingual-e5-large | ~2.2GB | 多语言 |
| text-embedding-3-small | API | OpenAI 云端 |

> 通用选择：中文用 `BAAI/bge-small-zh-v1.5`（小、快、够用）

## 3. 安装依赖

```bash
pip install sentence-transformers

# 如果需要本地向量数据库
pip install chromadb
```

> sentence-transformers 依赖 torch。
> 有 GPU 会自动用 GPU，没有则用 CPU（小模型 CPU 也很快）。

## 4. 快速上手 sentence-transformers

### 4.1 加载与编码
```python
from sentence_transformers import SentenceTransformer

# 加载模型（首次自动从 HF 下载）
model = SentenceTransformer("BAAI/bge-small-zh-v1.5")

# 编码：文本 → 向量
sentences = [
    "今天天气真好",
    "外边阳光明媚",
    "我想去爬山",
    "Python 是一种编程语言",
]

embeddings = model.encode(sentences)

print(f"向量形状: {embeddings.shape}")       # (4, 512)
print(f"第一个向量: {embeddings[0][:5]}...")  # 前5个数字
```

### 4.2 批量与参数
```python
embeddings = model.encode(
    sentences,
    batch_size=32,        # 批量大小
    normalize_embeddings=True,  # 归一化（余弦相似度更快）
    show_progress_bar=True,
    convert_to_numpy=True,
)
```

## 5. 语义相似度检索

### 5.1 手动计算余弦相似度
```python
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-zh-v1.5")

docs = [
    "Python 装饰器用于增强函数功能",
    "生成器可以节省内存",
    "异步编程适合IO密集任务",
]

# 编码文档（归一化）
doc_vecs = model.encode(docs, normalize_embeddings=True)

# 编码查询
query = "什么是装饰器？"
query_vec = model.encode(query, normalize_embeddings=True)

# 余弦相似度（归一化后 = 点积）
scores = doc_vecs @ query_vec
for doc, score in zip(docs, scores):
    print(f"相似度 {score:.4f} | {doc}")
```

### 5.2 完整检索函数
```python
def semantic_search(query: str, docs: list[str], top_k: int = 3) -> list[tuple[str, float]]:
    """语义检索：返回最相关的 top_k 个文档"""
    query_vec = model.encode(query, normalize_embeddings=True)
    doc_vecs = model.encode(docs, normalize_embeddings=True)
    scores = doc_vecs @ query_vec

    # 取 top_k 个索引
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [(docs[i], float(scores[i])) for i in top_indices]

results = semantic_search("怎么优化Python性能？", docs, top_k=2)
for doc, score in results:
    print(f"{score:.4f} {doc}")
```

## 6. 构建 RAG 知识库

### 6.1 完整 RAG 管道
```python
import json
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# ========== 1. 嵌入模型（本地） ==========
embedder = SentenceTransformer("BAAI/bge-small-zh-v1.5")

# ========== 2. LLM（可以是本地 Ollama 或云端） ==========
llm = OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1",   # 本地 Ollama
)

# ========== 3. 知识库文档 ==========
documents = [
    "Python 装饰器是一种高级语法特性，用于在不修改原函数代码的情况下增强函数功能。",
    "生成器使用 yield 关键字，按需生成数据，节省内存。",
    "asyncio 是 Python 的异步编程框架，使用 async/await 语法。",
]

# ========== 4. 离线建库（文档 → 向量） ==========
doc_vectors = embedder.encode(documents, normalize_embeddings=True)

# ========== 5. 在线查询（问题 → 检索 → 生成） ==========
def ask(question: str) -> str:
    # 5.1 检索最相关的文档
    q_vec = embedder.encode(question, normalize_embeddings=True)
    scores = doc_vectors @ q_vec
    top_idx = scores.argsort()[::-1][:2]
    context = "\n".join([documents[i] for i in top_idx])

    # 5.2 把文档 + 问题 交给 LLM 生成
    response = llm.chat.completions.create(
        model="qwen2.5:7b",
        messages=[
            {"role": "system", "content": "只根据参考资料回答，资料中没有的就说不知道。"},
            {"role": "user", "content": f"参考资料：\n{context}\n\n问题：{question}"},
        ],
    )
    return response.choices[0].message.content

# 测试
print(ask("装饰器有什么用？"))
```

### 6.2 文本切分（Chunking）要点
```python
# 长文档要先切块，再向量化（每块 200-500 字）
def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks

# 推荐按段落切分，语义更完整：
def chunk_by_paragraph(text: str, max_len: int = 300) -> list[str]:
    chunks, current = [], ""
    for para in text.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        if len(current) + len(para) < max_len:
            current += ("\n" if current else "") + para
        else:
            if current:
                chunks.append(current)
            current = para
    if current:
        chunks.append(current)
    return chunks
```

## 7. 向量数据库选型

| 数据库 | 规模 | 部署方式 | 特点 |
|--------|------|---------|------|
| Chroma | 小/中 | pip 安装 | 简单、嵌入式、推荐入门 |
| FAISS | 中/大 | pip 安装 | Meta 出品、高性能、无持久化 |
| Milvus | 大 | Docker/集群 | 生产级、分布式 |
| Qdrant | 中/大 | Docker | Rust 实现、性能好 |
| Pinecone | 云 | 托管 | 免运维、按量付费 |
| pgvector | 中 | PostgreSQL 插件 | 复用数据库 |

### Chroma 快速示例
```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")   # 持久化
collection = client.get_or_create_collection("knowledge")

# 添加文档
collection.add(
    ids=["1", "2"],
    documents=documents,
)

# 查询（内置默认嵌入模型；也可指定自定义嵌入）
results = collection.query(query_texts=["装饰器是什么"], n_results=2)
print(results["documents"])
```

## 8. 中文模型特别说明

### 8.1 bge 系列使用建议
```python
# BGE 模型建议加指令前缀（提升检索效果）
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-zh-v1.5")

query = "装饰器是什么？"
# BGE 中文模型要求查询加前缀（文档不用加）
query_with_prefix = f"为这个句子生成表示以用于检索相关文章：{query}"
```

### 8.2 维度与内存
```
512 维向量 ≈ 2KB/条
10 万条文档 ≈ 200MB 内存（完全可接受）
→ 小规模知识库完全不用向量数据库，numpy 就够
```

## 9. OpenAI 兼容嵌入服务

Ollama 和 vLLM 都提供 `/v1/embeddings` 端点：

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 用 Ollama 的 nomic-embed-text 或 bge-m3 做嵌入
response = client.embeddings.create(
    model="bge-m3",                        # 需先 ollama pull bge-m3
    input="今天天气真好",
)
vector = response.data[0].embedding
print(f"维度: {len(vector)}")
```

## 10. 性能优化

### 10.1 缓存向量（避免重复计算）
```python
import json, os

CACHE_FILE = "embedding_cache.json"

def encode_cached(model, texts: list[str]):
    """带缓存的编码（文本 → 向量，重复文本不重新计算）"""
    cache = {}
    if os.path.exists(CACHE_FILE):
        cache = json.load(open(CACHE_FILE, encoding="utf-8"))

    new_texts = [t for t in texts if t not in cache]
    if new_texts:
        new_vecs = model.encode(new_texts, normalize_embeddings=True)
        for t, v in zip(new_texts, new_vecs.tolist()):
            cache[t] = v
        json.dump(cache, open(CACHE_FILE, "w", encoding="utf-8"))

    return [cache[t] for t in texts]
```

### 10.2 批处理加速
```python
# encode 天然支持批量，一次传入大量文本比循环调用快数倍
embeddings = model.encode(all_docs, batch_size=64, show_progress_bar=True)
```

### 10.3 模型量化
```python
# sentence-transformers 也支持量化加载（省内存）
model = SentenceTransformer("BAAI/bge-large-zh-v1.5")
# 内部可以配合 torch quantization 或换更小模型
```

---

## 11. Reranker 精排模型

### 11.1 为什么需要 Reranker
```
向量检索的局限：
  向量检索（如 bge + 余弦相似度）召回 top_k 文档时，
  "语义相关" ≠ "能回答问题"。
  
  例如：问"Python 装饰器怎么用？"
  向量可能召回"装饰器模式在 Python 中的应用"（讲了设计模式，没讲语法）
  → 召回率高，但准确率不一定高

Reranker 的作用：
  对向量检索结果做"精排"——逐对比较问题和文档，
  判断文档是否能真正回答问题。
```

### 11.2 推荐 Reranker 模型
| 模型 | 大小 | 特点 |
|------|------|------|
| **BAAI/bge-reranker-v2-m3** | ~2.2GB | 多语言，中文效果好，推荐 |
| BAAI/bge-reranker-large | ~1.3GB | 中文专用 |
| BAAI/bge-reranker-base | ~560MB | 轻量，速度更快 |
| cross-encoder/ms-marco-MiniLM-L-6-v2 | ~90MB | 英文经典 |

### 11.3 完整 RAG + Reranker 管道
```python
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder

# === 1. 初始化模型 ===
embedder = SentenceTransformer("BAAI/bge-small-zh-v1.5")        # 向量检索
reranker = CrossEncoder("BAAI/bge-reranker-v2-m3")              # 精排

# === 2. 知识库 ===
documents = [
    "Python 装饰器用于在不修改原函数代码的情况下增强函数功能。",
    "装饰器使用 @ 语法糖，本质是一个接受函数作为参数的高阶函数。",
    "生成器使用 yield 关键字按需生成数据，大幅节省内存。",
    "asyncio 是 Python 的异步编程框架，适合 IO 密集型任务。",
]
doc_vectors = embedder.encode(documents, normalize_embeddings=True)

# === 3. 两阶段检索 ===
def search_with_rerank(question: str, top_k: int = 5, final_k: int = 2) -> list[str]:
    """
    两阶段检索：
    阶段1：向量检索 → 召回 top_k 候选
    阶段2：Reranker → 精排取 final_k 结果
    """
    # 阶段1：向量粗筛
    q_vec = embedder.encode(question, normalize_embeddings=True)
    scores = doc_vectors @ q_vec
    top_indices = np.argsort(scores)[::-1][:top_k]
    candidates = [documents[i] for i in top_indices]
    
    # 阶段2：Reranker 精排
    pairs = [[question, doc] for doc in candidates]
    rerank_scores = reranker.predict(pairs)
    ranked = sorted(zip(candidates, rerank_scores), key=lambda x: x[1], reverse=True)
    
    return [doc for doc, _ in ranked[:final_k]]

# 测试
results = search_with_rerank("装饰器是什么？", top_k=5, final_k=2)
for i, doc in enumerate(results, 1):
    print(f"{i}. {doc}")
```

### 11.4 性能对比
```
检索方式               | 召回率 | 准确率 | 速度
----------------------|--------|--------|------
纯向量检索             | ~80%   | ~65%   | 快
向量 + Reranker 精排   | ~80%   | ~90%+  | 中等（多了精排步骤）

Reranker 一次比较一对（query, doc），top_k 设太大影响速度。
建议：top_k=10~20 → Reranker → final_k=3~5
```

## 12. 混合检索：BM25 + 向量

### 12.1 为什么需要混合检索
```
向量检索的优势：语义理解强，"苹果手机"能匹配"iPhone"
向量检索的劣势：精确关键词弱，"AK-47"可能匹配"M16"

BM25（关键词检索）恰好相反：
- 精确匹配强："AK-47"严格匹配
- 语义理解弱："苹果手机"匹配不到"iPhone"

混合检索 = 取两者之长
```

### 12.2 BM25 + 向量 + RRF 融合
```python
# pip install rank-bm25 jieba
import numpy as np
import jieba
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-zh-v1.5")

documents = [
    "Python 装饰器用于增强函数功能。",
    "JavaScript 的装饰器语法与 Python 不同。",
    "生成器使用 yield 节省内存。",
    "asyncio 适合 IO 密集型任务。",
]

# === 1. BM25 关键词检索 ===
tokenized_docs = [list(jieba.cut(doc)) for doc in documents]
bm25 = BM25Okapi(tokenized_docs)

# === 2. 向量语义检索 ===
doc_vectors = model.encode(documents, normalize_embeddings=True)

def hybrid_search(query: str, top_k: int = 3) -> list[tuple[str, float]]:
    """混合检索：BM25 + 向量，RRF 融合"""
    # BM25 分数
    tokenized_query = list(jieba.cut(query))
    bm25_scores = bm25.get_scores(tokenized_query)
    
    # 向量分数
    q_vec = model.encode(query, normalize_embeddings=True)
    vector_scores = doc_vectors @ q_vec
    
    # RRF（Reciprocal Rank Fusion）融合
    k = 60  # RRF 常数
    bm25_rank = np.argsort(np.argsort(-bm25_scores)) + 1      # 排名（1-based）
    vector_rank = np.argsort(np.argsort(-vector_scores)) + 1
    
    combined = 1/(k + bm25_rank) + 1/(k + vector_rank)
    
    # 取 top_k
    top_indices = np.argsort(combined)[::-1][:top_k]
    return [(documents[i], combined[i]) for i in top_indices]

# 测试
results = hybrid_search("装饰器语法", top_k=2)
for doc, score in results:
    print(f"融合分 {score:.4f} | {doc}")
```

### 12.3 混合检索 vs 单方案
```
场景                          | 纯向量 | 纯BM25 | 混合检索
-----------------------------|--------|--------|---------
"装饰器是什么"（语义查询）     | ✅     | ❌     | ✅
"AK-47型号参数"（精确查询）   | ❌     | ✅     | ✅
"怎么优化Python性能"（混合）  | ⚠️     | ⚠️     | ✅
```

## 13. 高级文本切分策略

### 13.1 为什么要好的切分
```
文档切分直接影响 RAG 检索质量：

切太碎（100字/块）→ 信息不完整 → LLM 上下文不够
切太大（2000字/块）→ 检索不精确 → 噪声太多
切断句子 → "装饰器..."的文档被切成"装饰"和"器..." → 无法检索
```

### 13.2 递归字符切分（推荐）
```python
def recursive_chunk(text: str, chunk_size: int = 500, overlap: int = 80) -> list[str]:
    """
    递归字符切分：按 \\n\\n → \\n → 。→ ， 优先级逐级切分
    保证段落在同一块中，句子不被切断
    """
    separators = ["\n\n", "\n", "。", "！", "？", "；", "，", " "]
    
    for sep in separators:
        if sep in text:
            break
    
    chunks = []
    parts = text.split(sep)
    current = ""
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if len(current) + len(part) + len(sep) <= chunk_size:
            current += (sep if current else "") + part
        else:
            if current:
                chunks.append(current)
            # 如果单个 part 超过 chunk_size，强制按字符切分
            if len(part) > chunk_size:
                for i in range(0, len(part), chunk_size - overlap):
                    chunks.append(part[i:i + chunk_size])
            else:
                current = part
    
    if current:
        chunks.append(current)
    return chunks

# 测试
text = """
第一章：Python 基础

Python 是一种解释型、面向对象的高级编程语言。
它由 Guido van Rossum 于 1991 年首次发布。

Python 的设计哲学强调代码的可读性和简洁的语法。
"""
chunks = recursive_chunk(text, chunk_size=80)
for i, c in enumerate(chunks):
    print(f"块{i}: [{c}]")
```

### 13.3 语义切分（Semantic Chunking）
```python
from sentence_transformers import SentenceTransformer
import numpy as np

def semantic_chunk(
    text: str, 
    model: SentenceTransformer, 
    threshold: float = 0.5,
    min_chunk_size: int = 100,
) -> list[str]:
    """
    语义切分：在语义"断崖"处切分文档
    
    原理：计算相邻句子的余弦相似度，相似度骤降处即为主题切换点
    """
    # 按句号切分为句子
    raw_sentences = text.replace("！", "。").replace("？", "。").replace("\n", "。").split("。")
    sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 5]
    
    if len(sentences) <= 1:
        return [text]
    
    # 编码所有句子
    embeddings = model.encode(sentences, normalize_embeddings=True)
    
    # 计算相邻句子相似度
    similarities = []
    for i in range(len(embeddings) - 1):
        sim = float(embeddings[i] @ embeddings[i+1])
        similarities.append(sim)
    
    # 在断崖处切分
    chunks, current_chunk = [], [sentences[0]]
    for i in range(1, len(sentences)):
        if similarities[i-1] < threshold and len("。".join(current_chunk)) >= min_chunk_size:
            # 断崖！这里切换主题
            chunks.append("。".join(current_chunk) + "。")
            current_chunk = []
        current_chunk.append(sentences[i])
    
    if current_chunk:
        chunks.append("。".join(current_chunk) + "。")
    
    return chunks

# 使用示例
model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
chunks = semantic_chunk(long_document, model, threshold=0.4)
```

### 13.4 切分策略对比
```
策略           | 语义完整性 | 检索精度 | 计算开销 | 适用场景
---------------|-----------|---------|---------|---------
固定字符切分    | ❌        | ⚠️      | 无      | 快速原型
递归字符切分    | ✅        | ✅      | 低      | 通用推荐
语义切分        | ✅✅      | ✅✅    | 中等    | 长文档/多主题
段落切分        | ✅        | ✅      | 低      | 结构清晰的文档

实战建议：
- 先用递归字符切分（chunk_size=500, overlap=80）
- 检索效果不好时，换语义切分
- 多轮对话场景加 overlap 保证上下文不丢失
```

## 小结

```
嵌入模型全流程：
安装 → SentenceTransformer加载 → encode(文本) → 向量
     → 相似度检索 → 拼给 LLM → RAG 完成
```

**核心收获**：
1. 嵌入模型把文本变向量，语义相近则向量相近
2. `encode()` 是唯一核心方法，`@` 点积算相似度
3. RAG = 向量检索 + LLM 生成，中文推荐 `bge-small-zh-v1.5`
