"""
第5阶段：LangChain 框架实战
============================

学习目标：
1. 理解 LangChain 的核心概念和架构
2. 使用 LangChain 的 Model I/O 组件
3. 使用 LangChain 的 RAG 组件
4. 使用 LangChain 的 Agent 组件
5. 构建一个完整的 LangChain 应用

LangChain 是目前最流行的 LLM 应用开发框架，
它提供了标准化的接口和丰富的组件，让你能快速构建 Agent 应用。

安装：pip install langchain langchain-openai langchain-community

⚠️ LangChain 版本更新很快，建议查看最新文档：
https://python.langchain.com/
"""
import os

# ============================================================
# 1. LangChain 核心概念
# ============================================================
"""
┌──────────────────────────────────────────────────────────────┐
│                  LangChain 核心架构                           │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Model I/O  │  │  Retrieval  │  │   Agent     │         │
│  │  模型交互    │  │  检索增强    │  │  智能代理    │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                  │
│  ┌──────┴──────────────────┴────────────────┴──────┐        │
│  │              Chains（链）                         │        │
│  │         将组件串联成工作流                         │        │
│  └──────────────────────┬──────────────────────────┘        │
│                         │                                    │
│  ┌──────────────────────┴──────────────────────────┐        │
│  │           Memory（记忆）                          │        │
│  │         维护对话状态和上下文                       │        │
│  └─────────────────────────────────────────────────┘        │
└──────────────────────────────────────────────────────────────┘

核心组件：
1. Model I/O：LLM 调用、Prompt 模板、输出解析器
2. Retrieval：文档加载、切分、嵌入、向量存储、检索
3. Agent：工具调用、决策循环、执行引擎
4. Chains：将多个组件串联成工作流
5. Memory：对话历史管理
"""

# ============================================================
# 2. Model I/O —— 模型交互
# ============================================================
"""
LangChain 的 Model I/O 包含三个部分：
- Prompts：管理和模板化提示词
- LLMs/ChatModels：调用语言模型
- Output Parsers：解析模型输出
"""

# --- 2.1 Chat Model ---
from langchain_openai import ChatOpenAI

# 初始化 Chat Model（兼容 DeepSeek）
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.environ.get('AI_DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
    temperature=0,
)

# 简单调用
# from langchain_core.messages import HumanMessage, SystemMessage
# messages = [
#     SystemMessage(content="你是一个 Python 专家。"),
#     HumanMessage(content="什么是装饰器？")
# ]
# response = llm.invoke(messages)
# print(response.content)


# --- 2.2 Prompt Template ---
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 创建 Prompt 模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，用{style}的风格回答问题。"),
    ("human", "{question}")
])

# 使用模板
formatted = prompt.invoke({"role": "Python导师", "style": "幽默", "question": "什么是GIL？"})
response = llm.invoke(formatted)
print(response.content)


# --- 2.3 Output Parser ---
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

# 字符串解析器（直接获取文本）
str_parser = StrOutputParser()

# JSON 解析器
class MovieReview(BaseModel):
    movie_name: str = Field(description="电影名称")
    rating: float = Field(description="评分 0-10")
    summary: str = Field(description="一句话评价")
    recommend: bool = Field(description="是否推荐")

json_parser = JsonOutputParser(pydantic_object=MovieReview)

# 使用 JSON 解析器的 Prompt
json_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个电影评论家。{format_instructions}"),
    ("human", "评价电影：{movie}")
])

# chain = json_prompt | llm | json_parser
# result = chain.invoke({
#     "movie": "盗梦空间",
#     "format_instructions": json_parser.get_format_instructions()
# })
# print(result)


# --- 2.4 LCEL（LangChain Expression Language）---
"""
LCEL 是 LangChain 的核心语法，用 | 管道符串联组件：

chain = prompt | llm | parser

等价于：
1. prompt.invoke(input) → 格式化提示词
2. llm.invoke(formatted_prompt) → 调用 LLM
3. parser.invoke(response) → 解析输出

LCEL 的优势：
- 简洁：一行代码定义完整工作流
- 灵活：可以任意组合组件
- 支持流式、批处理、异步
"""

# 简单链
# simple_chain = prompt | llm | str_parser
# result = simple_chain.invoke({
#     "role": "编程导师",
#     "style": "简洁",
#     "question": "Python 的列表和元组有什么区别？"
# })
# print(result)


# ============================================================
# 3. RAG with LangChain
# ============================================================

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- 3.1 文档切分 ---
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", ".", " ", ""]
)

# --- 3.2 嵌入模型 ---
# embeddings = OpenAIEmbeddings(
#     model="text-embedding-3-small",
#     api_key=os.environ.get('AI_DEEPSEEK_API_KEY'),
#     base_url="https://api.deepseek.com"  # DeepSeek 可能不支持 embedding
# )

# --- 3.3 向量存储 ---
# vectorstore = Chroma.from_documents(
#     documents=splits,
#     embedding=embeddings,
#     persist_directory="./chroma_db"
# )

# --- 3.4 检索器 ---
# retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# --- 3.5 RAG Chain ---
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """根据以下上下文回答问题。如果上下文中没有相关信息，请说"我不知道"。

上下文：
{context}"""),
    ("human", "{question}")
])

# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | rag_prompt
#     | llm
#     | StrOutputParser()
# )
# result = rag_chain.invoke("什么是装饰器？")


# ============================================================
# 4. Agent with LangChain
# ============================================================

from langchain_core.tools import tool

# --- 4.1 用 @tool 装饰器定义工具 ---
@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    weather_data = {
        "北京": "28°C，晴天",
        "上海": "32°C，多云",
        "深圳": "35°C，雷阵雨",
    }
    return weather_data.get(city, f"未找到{city}的天气数据")

@tool
def calculate(expression: str) -> str:
    """执行数学计算"""
    try:
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return "不安全的表达式"
        return str(eval(expression))
    except Exception as e:
        return f"计算错误: {e}"

@tool
def search_knowledge(query: str) -> str:
    """搜索知识库获取信息"""
    # 这里可以接入 RAG 系统
    return f"关于'{query}'的信息：[模拟搜索结果]"

# --- 4.2 创建 Agent ---
from langchain.agents import create_tool_calling_agent, AgentExecutor

tools = [get_weather, calculate, search_knowledge]

agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能助手，可以调用工具帮助用户。用中文回答。"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),  # Agent 的思考过程
])

# agent = create_tool_calling_agent(llm, tools, agent_prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 运行 Agent
# result = agent_executor.invoke({"input": "北京今天天气怎么样？适合出门吗？"})
# print(result["output"])


# ============================================================
# 5. Memory —— 对话记忆
# ============================================================

from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 简单的内存对话历史
message_history = ChatMessageHistory()

# 带记忆的链
# chain_with_history = RunnableWithMessageHistory(
#     chain,
#     get_session_history=lambda session_id: message_history,
#     input_messages_key="question",
#     history_messages_key="chat_history",
# )


# ============================================================
# 6. 完整示例：知识问答 Agent
# ============================================================
"""
将 RAG + Agent + Memory 组合，构建一个完整的知识问答 Agent。

这个 Agent 可以：
1. 回答知识库中的问题（RAG）
2. 调用外部工具（Agent）
3. 记住之前的对话（Memory）
"""

# 完整代码结构（需要安装所有依赖后运行）：
"""
# 1. 初始化
llm = ChatOpenAI(model="deepseek-chat", ...)

# 2. 构建知识库
texts = load_documents()
splits = text_splitter.split_text(texts)
vectorstore = Chroma.from_texts(splits, embeddings)
retriever = vectorstore.as_retriever()

# 3. 定义工具
@tool
def knowledge_search(query: str) -> str:
    \"\"\"搜索知识库\"\"\"
    docs = retriever.invoke(query)
    return "\\n".join([doc.page_content for doc in docs])

tools = [knowledge_search, get_weather, calculate]

# 4. 创建 Agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. 运行
result = agent_executor.invoke({"input": "什么是装饰器？"})
"""


# ============================================================
# 💡 练习
# ============================================================
"""
练习1：使用 LangChain 构建一个"代码解释器 Agent"：
       - 用户输入 Python 代码
       - Agent 分析代码功能
       - 如果代码有 bug，指出并修复
       - 提供优化建议

练习2：使用 LangChain 构建一个"文档问答系统"：
       - 加载一个 .txt 或 .md 文件
       - 切分并建立向量索引
       - 支持多轮对话问答

练习3：对比 LangChain Agent 和第6阶段手写 Agent 的区别：
       - 开发效率
       - 灵活性
       - 可控性
       - 调试难度

练习4（进阶）：使用 LangGraph（LangChain 的新 Agent 框架）
       构建一个有状态的多步骤 Agent。
       LangGraph 文档：https://langchain-ai.github.io/langgraph/
"""
