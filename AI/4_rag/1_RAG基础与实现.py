"""
第4阶段：RAG 检索增强生成
==========================

学习目标：
1. 理解 RAG 的工作原理和为什么 Agent 需要它
2. 实现文档切分（Chunking）
3. 实现向量嵌入（Embedding）和相似度搜索
4. 构建一个完整的 RAG 管道
5. 将 RAG 集成到 Agent 中

为什么 Agent 需要 RAG？
- LLM 的知识有截止日期，不知道最新信息
- LLM 不知道你的私有数据（公司文档、个人笔记等）
- RAG 让 Agent 能"查阅资料"后再回答，提高准确性

RAG 流程：
  用户提问 → 检索相关文档 → 文档+问题一起给 LLM → LLM 基于文档回答
"""

import os
import json
import math
from typing import Optional
from openai import OpenAI

# ============================================================
# 1. RAG 核心概念
# ============================================================
"""
┌──────────────────────────────────────────────────────────────┐
│                      RAG 流程图                               │
│                                                              │
│  离线阶段（建库）：                                            │
│  文档 → 切分 → 嵌入(Embedding) → 向量数据库                    │
│                                                              │
│  在线阶段（查询）：                                            │
│  用户问题 → 嵌入 → 向量相似度搜索 → Top-K 文档片段              │
│           → 文档片段 + 问题 → LLM → 回答                      │
└──────────────────────────────────────────────────────────────┘

关键组件：
1. 文档加载器（Document Loader）：读取各种格式的文档
2. 文本切分器（Text Splitter）：将长文档切成小段
3. 嵌入模型（Embedding Model）：将文本转为向量
4. 向量数据库（Vector Store）：存储和检索向量
5. 检索器（Retriever）：根据问题找到最相关的文档
6. 生成器（Generator）：基于检索结果生成回答
"""


# ============================================================
# 2. 文档切分（Chunking）
# ============================================================
"""
为什么需要切分？
- LLM 有上下文长度限制
- 太长的文档包含太多无关信息，影响回答质量
- 切成小段后，可以精确检索最相关的部分

切分策略：
1. 固定长度切分：每段固定字符数
2. 按段落切分：按换行符或段落标记切分
3. 递归切分：先按段落，太长再按句子，太长再按字符
4. 语义切分：根据内容语义边界切分（最复杂但效果最好）
"""

class TextSplitter:
    """文本切分器"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Args:
            chunk_size: 每段最大字符数
            chunk_overlap: 相邻段落的重叠字符数（保证上下文连贯）
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str) -> list[str]:
        """固定长度切分（带重叠）"""
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += self.chunk_size - self.chunk_overlap
        return chunks
    
    def split_by_paragraph(self, text: str, max_chunk_size: int = 500) -> list[str]:
        """按段落切分（段落太长则进一步切分）"""
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            if len(current_chunk) + len(para) + 2 <= max_chunk_size:
                current_chunk += ("\n\n" if current_chunk else "") + para
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                # 如果单个段落太长，进一步切分
                if len(para) > max_chunk_size:
                    sub_chunks = self.split_text(para)
                    chunks.extend(sub_chunks[:-1])
                    current_chunk = sub_chunks[-1] if sub_chunks else ""
                else:
                    current_chunk = para
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks


# 测试切分
sample_doc = """
Python 是一种广泛使用的高级编程语言。它由 Guido van Rossum 于1991年首次发布。
Python 的设计哲学强调代码的可读性和简洁性，其语法允许程序员用更少的代码行来表达概念。

Python 支持多种编程范式，包括面向对象、命令式、函数式和过程式编程。
它有一个全面的标准库，通常被称为"内置电池"（batteries included）。

Python 的应用领域非常广泛，包括：
1. Web 开发：Django、Flask 等框架
2. 数据科学：NumPy、Pandas、Matplotlib
3. 人工智能：TensorFlow、PyTorch
4. 自动化脚本：系统管理、文件处理
5. 网络爬虫：Scrapy、BeautifulSoup

Python 的最新版本是 Python 3.12，它引入了许多新特性，
包括更好的错误消息、性能改进和新的类型提示功能。
"""

splitter = TextSplitter(chunk_size=200, chunk_overlap=30)
chunks = splitter.split_by_paragraph(sample_doc)
print("文档切分结果：")
for i, chunk in enumerate(chunks):
    print(f"  片段{i+1} ({len(chunk)}字): {chunk[:60]}...")


# ============================================================
# 3. 向量嵌入与相似度搜索（纯 Python 实现）
# ============================================================
"""
向量嵌入（Embedding）：将文本转换为一组数字（向量），
语义相似的文本 → 向量距离更近。

实际项目中使用专门的嵌入模型（如 OpenAI embeddings），
这里用简单的 TF-IDF 方式演示原理。
"""

class SimpleVectorizer:
    """
    简单的向量化器（基于词频）
    
    实际项目中请使用：
    - OpenAI: client.embeddings.create(model="text-embedding-3-small", input=text)
    - 本地模型: sentence-transformers
    """
    
    def __init__(self):
        self.vocabulary: dict[str, int] = {}
        self.idf: dict[str, float] = {}
    
    def _tokenize(self, text: str) -> list[str]:
        """简单分词（中文按字符，英文按空格）"""
        # 简单处理：转小写，按空格和标点分割
        import re
        tokens = re.findall(r'[\u4e00-\u9fff]|[a-zA-Z]+', text.lower())
        return tokens
    
    def fit(self, documents: list[str]):
        """构建词汇表和 IDF"""
        doc_count = len(documents)
        doc_freq: dict[str, int] = {}
        
        for doc in documents:
            tokens = set(self._tokenize(doc))
            for token in tokens:
                doc_freq[token] = doc_freq.get(token, 0) + 1
        
        # 构建 IDF
        for token, freq in doc_freq.items():
            self.idf[token] = math.log(doc_count / (freq + 1)) + 1
        
        # 构建词汇表
        self.vocabulary = {word: idx for idx, word in enumerate(sorted(doc_freq.keys()))}
    
    def transform(self, text: str) -> list[float]:
        """将文本转为 TF-IDF 向量"""
        tokens = self._tokenize(text)
        tf: dict[str, int] = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1
        
        # TF-IDF 向量
        vector = [0.0] * len(self.vocabulary)
        for token, count in tf.items():
            if token in self.vocabulary:
                idx = self.vocabulary[token]
                vector[idx] = (count / len(tokens)) * self.idf.get(token, 1.0)
        
        return vector
    
    def cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        """计算余弦相似度"""
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)


# ============================================================
# 4. 简单向量数据库
# ============================================================

class SimpleVectorStore:
    """
    简单的向量数据库
    
    实际项目中请使用：
    - Chroma: pip install chromadb
    - FAISS: pip install faiss-cpu
    - Pinecone: 云端向量数据库
    - Milvus: 分布式向量数据库
    """
    
    def __init__(self):
        self.documents: list[dict] = []  # 存储文档和元数据
        self.vectors: list[list[float]] = []  # 存储向量
        self.vectorizer = SimpleVectorizer()
    
    def add_documents(self, texts: list[str], metadatas: list[dict] = None):
        """添加文档到向量数据库"""
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        # 重新拟合向量化器
        self.vectorizer.fit(texts + [d["text"] for d in self.documents] if self.documents else texts)
        
        # 重新计算所有向量（简化实现）
        self.vectors = []
        self.documents = []
        
        all_texts = texts
        all_metas = metadatas
        
        for text, meta in zip(all_texts, all_metas):
            vector = self.vectorizer.transform(text)
            self.vectors.append(vector)
            self.documents.append({"text": text, "metadata": meta})
    
    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """搜索最相关的文档"""
        query_vector = self.vectorizer.transform(query)
        
        similarities = []
        for i, doc_vector in enumerate(self.vectors):
            sim = self.vectorizer.cosine_similarity(query_vector, doc_vector)
            similarities.append((i, sim))
        
        # 按相似度排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for idx, score in similarities[:top_k]:
            results.append({
                "text": self.documents[idx]["text"],
                "metadata": self.documents[idx]["metadata"],
                "score": round(score, 4)
            })
        
        return results


# ============================================================
# 5. 完整的 RAG 管道
# ============================================================

class RAGPipeline:
    """
    RAG 检索增强生成管道
    
    流程：用户问题 → 检索相关文档 → 文档+问题 → LLM → 回答
    """
    
    def __init__(self, chunk_size: int = 300, chunk_overlap: int = 50):
        self.splitter = TextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.vector_store = SimpleVectorStore()
        self.client = OpenAI(
            api_key=os.environ.get('AI_DEEPSEEK_API_KEY'),
            base_url="https://api.deepseek.com"
        )
    
    def ingest(self, documents: list[str], source_names: list[str] = None):
        """
        导入文档到知识库
        
        Args:
            documents: 文档文本列表
            source_names: 文档来源名称列表
        """
        if source_names is None:
            source_names = [f"文档{i+1}" for i in range(len(documents))]
        
        all_chunks = []
        all_metadatas = []
        
        for doc, source in zip(documents, source_names):
            chunks = self.splitter.split_by_paragraph(doc)
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadatas.append({"source": source, "chunk_index": i})
        
        self.vector_store.add_documents(all_chunks, all_metadatas)
        print(f"✅ 已导入 {len(documents)} 个文档，共 {len(all_chunks)} 个片段")
    
    def retrieve(self, query: str, top_k: int = 3) -> list[dict]:
        """检索相关文档"""
        results = self.vector_store.search(query, top_k=top_k)
        print(f"\n🔍 检索到 {len(results)} 个相关片段：")
        for i, r in enumerate(results):
            print(f"  [{i+1}] 相似度={r['score']:.4f} | {r['text'][:60]}...")
        return results
    
    def generate(self, query: str, context_docs: list[dict]) -> str:
        """基于检索结果生成回答"""
        # 拼接上下文
        context = "\n\n".join([
            f"[来源: {doc['metadata'].get('source', '未知')}] {doc['text']}"
            for doc in context_docs
        ])
        
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": """你是一个知识助手。请根据以下参考资料回答用户的问题。

规则：
1. 只根据参考资料回答，不要编造信息
2. 如果参考资料中没有相关信息，请明确说明
3. 引用信息时标注来源
4. 用中文回答"""
                },
                {
                    "role": "user",
                    "content": f"参考资料：\n{context}\n\n问题：{query}"
                }
            ],
            temperature=0,
            stream=False
        )
        
        return response.choices[0].message.content
    
    def query(self, question: str, top_k: int = 3) -> str:
        """完整的 RAG 查询流程"""
        print(f"\n❓ 问题: {question}")
        
        # 1. 检索
        context_docs = self.retrieve(question, top_k=top_k)
        
        # 2. 生成
        answer = self.generate(question, context_docs)
        
        print(f"\n✅ 回答: {answer[:200]}...")
        return answer


# ============================================================
# 6. 测试 RAG 管道
# ============================================================

# 创建知识库
rag = RAGPipeline()

# 导入文档
knowledge_docs = [
    """
    Python 装饰器是一种高级语法特性，它允许在不修改原函数代码的情况下，
    为函数添加额外的功能。装饰器本质上是一个函数，它接受一个函数作为参数，
    返回一个新的函数。常见的用途包括：日志记录、性能计时、权限校验、缓存等。
    
    使用 @语法糖 可以简化装饰器的应用，例如：
    @timer
    def slow_function():
        time.sleep(1)
    
    这等价于 slow_function = timer(slow_function)
    """,
    
    """
    Python 的生成器是一种特殊的迭代器，使用 yield 关键字定义。
    生成器不会一次性生成所有数据，而是按需生成（惰性求值），
    这使得它在处理大数据集时非常节省内存。
    
    生成器表达式类似于列表推导式，但使用圆括号：
    (x**2 for x in range(1000000))  # 生成器表达式，不占内存
    [x**2 for x in range(1000000)]   # 列表推导式，占大量内存
    
    生成器的常见应用：读取大文件、数据流处理、无限序列。
    """,
    
    """
    asyncio 是 Python 的异步编程框架，使用 async/await 语法。
    异步编程适合 I/O 密集型任务（网络请求、文件读写、数据库查询），
    可以在等待 I/O 时执行其他任务，提高程序效率。
    
    核心概念：
    - async def：定义协程函数
    - await：等待异步操作完成（不阻塞事件循环）
    - asyncio.gather()：并发运行多个协程
    - asyncio.run()：运行入口协程
    
    与多线程的区别：异步是单线程并发，没有线程安全问题，
    但不适合 CPU 密集型任务。
    """
]

rag.ingest(knowledge_docs, ["装饰器详解", "生成器指南", "asyncio教程"])

# 测试查询
# answer1 = rag.query("Python 装饰器是什么？有什么用？")
# answer2 = rag.query("生成器和列表推导式有什么区别？")
# answer3 = rag.query("asyncio 适合什么场景？")


# ============================================================
# 7. 将 RAG 集成到 Agent 中
# ============================================================
"""
RAG 可以作为 Agent 的一个"工具"：
当 Agent 需要查找知识库中的信息时，调用 RAG 工具。

这样 Agent 就同时拥有了：
- 工具调用能力（Function Calling）
- 知识检索能力（RAG）
- 推理能力（LLM）
"""

def rag_search_tool(query: str) -> str:
    """RAG 搜索工具（可注册到 Agent 的工具系统中）"""
    results = rag.retrieve(query, top_k=2)
    if not results:
        return json.dumps({"answer": "未找到相关信息"}, ensure_ascii=False)
    
    # 返回最相关的文档片段
    context = "\n".join([r["text"] for r in results])
    return json.dumps({
        "relevant_docs": context[:500],
        "sources": [r["metadata"]["source"] for r in results]
    }, ensure_ascii=False)

# 可以把这个工具注册到第2阶段的 ToolRegistry 中
# registry.register(
#     name="knowledge_search",
#     description="搜索知识库获取专业信息",
#     func=rag_search_tool,
#     parameters={...}
# )


# ============================================================
# 💡 练习
# ============================================================
"""
练习1：实现一个文件加载器，支持读取 .txt 和 .md 文件，
       自动导入到 RAG 管道中。

练习2：将 SimpleVectorizer 替换为 OpenAI Embeddings：
       response = client.embeddings.create(
           model="text-embedding-3-small",
           input=text
       )
       embedding = response.data[0].embedding
       注意：这需要 API 调用，会产生费用。

练习3：实现"对话式 RAG"：
       - 支持多轮对话
       - 根据对话历史优化检索查询
       - 例如：用户问"它有什么优点？"，需要结合上下文理解"它"指什么

练习4（进阶）：实现"混合检索"：
       - 同时使用关键词检索和向量检索
       - 合并两种检索结果
       - 用 RRF（Reciprocal Rank Fusion）重排序
"""
