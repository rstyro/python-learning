"""
第1阶段：Prompt Engineering 与 LLM 交互深入
============================================

学习目标：
1. 理解 LLM 的三种消息角色（system / user / assistant）
2. 掌握多轮对话管理
3. 学会设计高效的 System Prompt
4. 理解流式输出与非流式输出的区别与使用场景

前置知识：你已经会基本的 API 调用（见 deepseek.py），这里深入理解消息机制
"""

import os
from openai import OpenAI

# ============================================================
# 1. 初始化客户端
# ============================================================
# 使用 DeepSeek API（兼容 OpenAI SDK）
client = OpenAI(
    api_key=os.environ.get('AI_DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

# ============================================================
# 2. 三种消息角色 —— 理解对话的核心
# ============================================================
"""
messages 列表中的每条消息都有一个 role 字段：

┌──────────┬──────────────────────────────────────────────────┐
│  role    │  作用                                             │
├──────────┼──────────────────────────────────────────────────┤
│  system  │  设定 AI 的行为、人格、约束条件（全局指令）          │
│  user    │  用户的输入（问题、指令）                           │
│  assistant│ AI 的回复（历史回复，用于维持上下文）              │
└──────────┴──────────────────────────────────────────────────┘

对话流程：
  system  → "你是一个专业的 Python 导师"
  user    → "什么是装饰器？"
  assistant → "装饰器是..."  （AI 的回复）
  user    → "能举个例子吗？"  （AI 能理解"它"指装饰器，因为有上下文）
"""

# --- 示例：不同 system prompt 的效果对比 ---

# 无 system prompt：通用回答
response_default = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "什么是装饰器？"}
    ],
    stream=False
)
print("【无 system prompt】")
print(response_default.choices[0].message.content)
print("=" * 60)

# 有 system prompt：专业、简洁的回答
response_with_system = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
            "role": "system",
            "content": "你是一个 Python 编程导师。回答要求：1.简洁 2.带代码示例 3.用中文"
        },
        {"role": "user", "content": "什么是装饰器？"}
    ],
    stream=False
)
print("【有 system prompt - Python导师】")
print(response_with_system.choices[0].message.content)
print("=" * 60)


# ============================================================
# 3. 多轮对话管理 —— Agent 的记忆基础
# ============================================================
"""
Agent 需要记住之前的对话，才能做出连贯的决策。

核心思路：把历史消息全部传给 API
  messages = [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "第1个问题"},
    {"role": "assistant", "content": "第1个回答"},
    {"role": "user", "content": "第2个问题"},   # AI 能理解上下文
  ]

⚠️ 注意：LLM 没有真正的"记忆"，每次调用都是无状态的！
   "记忆"是通过把历史消息重新传给 API 实现的。
"""

# --- 示例：多轮对话 ---
messages = [
    {"role": "system", "content": "你是一个有帮助的助手，用中文回答。"}
]

# 第1轮
messages.append({"role": "user", "content": "我想学习 Python 的列表推导式"})
response1 = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    stream=False
)
assistant_reply1 = response1.choices[0].message.content
messages.append({"role": "assistant", "content": assistant_reply1})
print("【第1轮 - AI 回复】")
print(assistant_reply1[:200], "...\n")

# 第2轮（AI 能记住之前的对话）
messages.append({"role": "user", "content": "能给我一个更复杂的例子吗？"})
response2 = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    stream=False
)
assistant_reply2 = response2.choices[0].message.content
messages.append({"role": "assistant", "content": assistant_reply2})
print("【第2轮 - AI 回复（理解\"更复杂\"指列表推导式）】")
print(assistant_reply2[:200], "...\n")


# ============================================================
# 4. 封装一个对话管理类 —— Agent 的基础组件
# ============================================================
class ChatSession:
    """
    对话会话管理器
    
    核心功能：
    - 自动维护消息历史
    - 支持流式/非流式输出
    - 支持设置 system prompt
    - 支持获取完整对话记录
    
    这是构建 Agent 的基础 —— Agent 需要一个"记忆"来维持上下文
    """

    def __init__(self, system_prompt: str = "你是一个有帮助的助手。", model: str = "deepseek-chat"):
        self.client = OpenAI(
            api_key=os.environ.get('AI_DEEPSEEK_API_KEY'),
            base_url="https://api.deepseek.com"
        )
        self.model = model
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]

    def chat(self, user_input: str, stream: bool = False) -> str:
        """
        发送消息并获取回复
        
        Args:
            user_input: 用户输入
            stream: 是否使用流式输出
            
        Returns:
            AI 的回复文本
        """
        # 添加用户消息
        self.messages.append({"role": "user", "content": user_input})

        if stream:
            return self._chat_stream()
        else:
            return self._chat_normal()

    def _chat_normal(self) -> str:
        """非流式调用：等待完整回复后返回"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=False
        )
        reply = response.choices[0].message.content
        # 记录 AI 回复到历史
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def _chat_stream(self) -> str:
        """流式调用：逐字输出，适合实时交互"""
        stream_response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True
        )
        full_reply = ""
        for chunk in stream_response:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta.content:
                    print(delta.content, end="", flush=True)
                    full_reply += delta.content
        print()  # 换行
        # 记录完整回复到历史
        self.messages.append({"role": "assistant", "content": full_reply})
        return full_reply

    def get_history(self) -> list[dict]:
        """获取完整对话历史"""
        return self.messages.copy()

    def clear_history(self, keep_system: bool = True):
        """清空对话历史"""
        if keep_system and self.messages and self.messages[0]["role"] == "system":
            self.messages = [self.messages[0]]
        else:
            self.messages = []

    def token_count_estimate(self) -> int:
        """
        估算当前消息的 token 数（粗略估算）
        
        经验法则：1 个中文字 ≈ 1-2 tokens，1 个英文单词 ≈ 1 token
        这里用简单的字符数/2 来估算
        """
        total_chars = sum(len(m["content"]) for m in self.messages)
        return total_chars // 2  # 粗略估算


# --- 使用 ChatSession ---
print("\n" + "=" * 60)
print("【使用 ChatSession 进行多轮对话】")
print("=" * 60)

session = ChatSession(system_prompt="你是一个 Python 专家，回答简洁，带代码示例。")

# 第1轮
reply1 = session.chat("Python 中 *args 和 **kwargs 是什么？")
print(f"AI: {reply1[:150]}...\n")

# 第2轮（有上下文）
reply2 = session.chat("它们可以一起用吗？给个例子")
print(f"AI: {reply2[:150]}...\n")

# 查看对话历史
print(f"对话轮数: {len([m for m in session.get_history() if m['role'] != 'system'])}")
print(f"估算 token 数: {session.token_count_estimate()}")


# ============================================================
# 5. System Prompt 设计技巧 —— Agent 的"人格"与"规则"
# ============================================================
"""
System Prompt 是 Agent 的"灵魂"，决定了 Agent 的行为边界。

好的 System Prompt 应该包含：
1. 角色定义：你是谁？
2. 能力范围：你能做什么？不能做什么？
3. 输出格式：应该怎样回答？
4. 约束条件：有什么限制？
5. 示例（Few-shot）：给出期望的回答样例

Agent 的 System Prompt 通常比普通聊天机器人更复杂，
因为 Agent 需要明确的"行动规则"。
"""

# --- 示例：为不同场景设计 System Prompt ---

# 代码审查 Agent
CODE_REVIEWER_PROMPT = """你是一个高级代码审查员。

你的职责：
1. 审查用户提交的 Python 代码
2. 找出潜在的 bug、性能问题、安全漏洞
3. 给出改进建议和重构方案

输出格式：
- 🔴 严重问题：...
- 🟡 改进建议：...
- 🟢 优秀之处：...
- 📝 重构代码：...

规则：
- 必须指出所有潜在问题，不要遗漏
- 每个问题都要给出具体原因和修复方案
- 如果代码很好，也要指出优点
"""

# 数据分析 Agent
DATA_ANALYST_PROMPT = """你是一个数据分析专家。

你的职责：
1. 分析用户提供的业务数据
2. 发现数据中的趋势、异常和洞察
3. 给出数据驱动的建议

输出格式：
1. 数据概览：关键指标总结
2. 趋势分析：主要趋势和变化
3. 异常发现：值得关注的异常点
4. 行动建议：基于数据的下一步行动

规则：
- 所有结论必须有数据支撑
- 不确定的内容要明确标注
- 建议要具体可执行
"""

# 使用示例
review_session = ChatSession(system_prompt=CODE_REVIEWER_PROMPT)
# reply = review_session.chat("请审查这段代码：\ndef add(a,b): return a+b")


# ============================================================
# 6. Few-shot 提示 —— 用示例教 AI 输出格式
# ============================================================
"""
Few-shot：在 prompt 中给出几个"输入→输出"的示例，
让 AI 学习你期望的输出格式。

这在 Agent 开发中非常重要，因为 Agent 的输出通常需要
被程序解析（如 JSON 格式），格式必须稳定。
"""

FEW_SHOT_PROMPT = """你是一个情感分析器。分析用户文本的情感，输出 JSON 格式。

示例1：
输入：今天天气真好，心情愉快！
输出：{"sentiment": "positive", "confidence": 0.95, "keywords": ["真好", "愉快"]}

示例2：
输入：这个产品太差了，非常失望。
输出：{"sentiment": "negative", "confidence": 0.90, "keywords": ["太差", "失望"]}

示例3：
输入：还行吧，一般般。
输出：{"sentiment": "neutral", "confidence": 0.60, "keywords": ["还行", "一般般"]}

现在请分析以下文本："""

# few_shot_session = ChatSession(system_prompt=FEW_SHOT_PROMPT)
# result = few_shot_session.chat("新手机用了一周，电池续航不错，但拍照效果一般。")
# print(result)  # 应该输出 JSON 格式的分析结果


# ============================================================
# 💡 练习
# ============================================================
"""
练习1：修改 ChatSession 类，添加 max_history 参数，
       当历史消息超过限制时，自动删除最早的消息（保留 system prompt）。
       
练习2：设计一个"翻译 Agent"的 System Prompt，
       要求：自动检测输入语言，翻译为目标语言，输出包含原文和译文。
       
练习3：使用 Few-shot 提示，让 AI 输出稳定的 JSON 格式，
       实现一个"文本分类器"（新闻分类：科技/体育/娱乐/财经）。
       
练习4（进阶）：实现一个简单的命令行聊天机器人，
       使用 ChatSession 类，支持用户输入 /clear 清空历史，
       支持 /system 修改 system prompt。
"""
