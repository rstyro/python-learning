"""
第1阶段（续）：输出控制与结构化输出
====================================

学习目标：
1. 控制输出长度和格式（max_tokens, temperature）
2. 让 LLM 输出结构化数据（JSON Mode）
3. 理解 temperature 对创造性的影响
4. 掌握输出解析与错误处理

为什么这很重要？
Agent 的输出通常需要被程序解析和执行，所以必须控制输出格式。
如果 Agent 输出的是自然语言，程序无法理解；
如果 Agent 输出的是结构化 JSON，程序就能解析并执行。
"""

import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('AI_DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)


# ============================================================
# 1. temperature —— 控制"创造性"
# ============================================================
"""
temperature 范围：0.0 ~ 2.0（默认 1.0）

  temperature = 0   → 最确定性，总是选概率最高的词（适合代码、事实问答）
  temperature = 0.7 → 适度创造性（适合日常对话）
  temperature = 1.5 → 高创造性，输出更多样（适合创意写作）

Agent 场景：
  - 工具调用决策：temperature=0（需要确定性）
  - 创意生成：temperature=0.7~1.0
  - 代码生成：temperature=0（需要准确性）
"""

def compare_temperatures(prompt: str):
    """对比不同 temperature 的输出差异"""
    for temp in [0.0, 0.7, 1.5]:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
            max_tokens=100,  # 限制输出长度
            stream=False
        )
        print(f"temperature={temp}:")
        print(response.choices[0].message.content)
        print("-" * 40)

# compare_temperatures("用一句话描述春天")


# ============================================================
# 2. max_tokens —— 控制输出长度
# ============================================================
"""
max_tokens 限制生成的最大 token 数。

注意：
- 1 个中文字 ≈ 1-2 tokens
- max_tokens 是上限，不是必须生成这么多
- 如果输出被截断，finish_reason 会是 "length" 而不是 "stop"
"""

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "详细解释 Python 装饰器"}],
    max_tokens=50,  # 只允许 50 tokens，输出会被截断
    stream=False
)
print("【max_tokens=50 的输出】")
print(response.choices[0].message.content)
print(f"finish_reason: {response.choices[0].finish_reason}")
# finish_reason="length" 表示输出被截断，"stop" 表示正常结束


# ============================================================
# 3. JSON Mode —— 让 LLM 输出合法 JSON
# ============================================================
"""
这是 Agent 开发的关键能力！

Agent 需要输出结构化数据，让程序能解析和执行。
例如：Agent 决定调用某个工具，需要输出工具名和参数。

方法1：在 prompt 中要求输出 JSON（不保证 100% 合法）
方法2：使用 response_format={"type": "json_object"}（强制 JSON 输出）
"""

# --- 方法1：Prompt 中要求 JSON ---
prompt_based = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
            "role": "system",
            "content": """你是一个任务分析器。分析用户的请求，输出 JSON 格式。

输出格式：
{
    "intent": "意图描述",
    "entities": ["提取的实体"],
    "action": "建议的操作",
    "confidence": 0.0-1.0的置信度
}

必须输出合法的 JSON，不要输出其他内容。"""
        },
        {"role": "user", "content": "帮我查一下明天北京的天气"}
    ],
    temperature=0,
    stream=False
)
print("\n【Prompt 方式输出 JSON】")
print(prompt_based.choices[0].message.content)

# --- 方法2：JSON Mode（更可靠）---
# ⚠️ DeepSeek 可能不支持 response_format，这里展示 OpenAI 标准用法
# 如果 DeepSeek 不支持，可以用 Prompt 方式 + json.loads 解析
try:
    json_mode_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是一个任务分析器。分析用户请求，输出 JSON 格式，包含 intent、entities、action、confidence 字段。"
            },
            {"role": "user", "content": "帮我查一下明天北京的天气"}
        ],
        response_format={"type": "json_object"},  # 强制 JSON 输出
        temperature=0,
        stream=False
    )
    print("\n【JSON Mode 输出】")
    print(json_mode_response.choices[0].message.content)
except Exception as e:
    print(f"\n【JSON Mode 不支持，使用 Prompt 方式即可】错误: {e}")


# ============================================================
# 4. 输出解析与错误处理 —— Agent 必须健壮
# ============================================================
"""
Agent 的输出需要被程序解析，所以必须处理各种异常情况：
1. JSON 解析失败
2. 缺少必要字段
3. 字段类型不对
4. LLM 输出了非 JSON 内容
"""

from pydantic import BaseModel, Field
from typing import Optional

# --- 用 Pydantic 定义输出结构（推荐方式）---
class TaskAnalysis(BaseModel):
    """任务分析结果的数据模型"""
    intent: str = Field(description="用户意图")
    entities: list[str] = Field(default_factory=list, description="提取的实体")
    action: str = Field(description="建议的操作")
    confidence: float = Field(ge=0, le=1, description="置信度 0-1")

def parse_llm_json(content: str, model_class: type[BaseModel]) -> Optional[BaseModel]:
    """
    安全地解析 LLM 输出的 JSON
    
    Args:
        content: LLM 的输出文本
        model_class: Pydantic 模型类
        
    Returns:
        解析后的对象，失败返回 None
    """
    # 清理可能的 markdown 代码块标记
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()
    
    try:
        data = json.loads(content)
        return model_class(**data)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}")
        return None
    except Exception as e:
        print(f"数据验证失败: {e}")
        return None

# 使用示例
test_output = '{"intent": "查询天气", "entities": ["明天", "北京"], "action": "调用天气API", "confidence": 0.95}'
result = parse_llm_json(test_output, TaskAnalysis)
if result:
    print(f"\n解析成功: intent={result.intent}, action={result.action}")


# ============================================================
# 5. 完整示例：结构化输出的 Agent 工具调用决策
# ============================================================
"""
这是 Agent 的核心能力之一：根据用户输入，决定调用什么工具。

流程：
  用户输入 → LLM 分析 → 输出 JSON（工具名+参数）→ 程序解析 → 执行工具
"""

# 定义可用工具
AVAILABLE_TOOLS = {
    "search_web": "搜索互联网获取信息",
    "get_weather": "获取指定城市的天气",
    "calculate": "执行数学计算",
    "send_email": "发送电子邮件",
    "read_file": "读取本地文件",
}

TOOL_DECISION_PROMPT = f"""你是一个智能助手，可以调用以下工具：

{json.dumps(AVAILABLE_TOOLS, ensure_ascii=False, indent=2)}

根据用户请求，决定是否需要调用工具，以及调用哪个工具。

输出 JSON 格式：
{{
    "need_tool": true/false,
    "tool_name": "工具名（不需要工具时为 null）",
    "tool_args": {{"参数名": "参数值"}},
    "reasoning": "你的推理过程",
    "direct_answer": "不需要工具时的直接回答"
}}

示例：
用户：北京今天天气怎么样？
输出：{{"need_tool": true, "tool_name": "get_weather", "tool_args": {{"city": "北京"}}, "reasoning": "需要实时天气数据", "direct_answer": null}}

用户：1+1等于几？
输出：{{"need_tool": false, "tool_name": null, "tool_args": {{}}, "reasoning": "简单计算不需要工具", "direct_answer": "1+1=2"}}
"""

class ToolDecision(BaseModel):
    """工具调用决策"""
    need_tool: bool
    tool_name: Optional[str] = None
    tool_args: dict = {}
    reasoning: str = ""
    direct_answer: Optional[str] = None

def decide_tool(user_input: str) -> ToolDecision:
    """
    让 LLM 决定是否需要调用工具
    
    这是 Agent 的"大脑"—— 决策层
    """
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": TOOL_DECISION_PROMPT},
            {"role": "user", "content": user_input}
        ],
        temperature=0,  # 工具调用需要确定性
        stream=False
    )
    content = response.choices[0].message.content
    result = parse_llm_json(content, ToolDecision)
    if result:
        return result
    # 解析失败时的降级处理
    return ToolDecision(
        need_tool=False,
        reasoning="JSON 解析失败，降级为直接回答",
        direct_answer=content
    )

# 测试
# decision1 = decide_tool("帮我查一下上海的天气")
# print(f"决策: need_tool={decision1.need_tool}, tool={decision1.tool_name}, args={decision1.tool_args}")

# decision2 = decide_tool("Python 的列表怎么排序？")
# print(f"决策: need_tool={decision2.need_tool}, answer={decision2.direct_answer}")


# ============================================================
# 💡 练习
# ============================================================
"""
练习1：实现一个"意图识别器"，能识别以下意图并输出结构化 JSON：
       - 查询信息（search）
       - 执行操作（action）
       - 闲聊（chat）
       - 投诉/反馈（feedback）
       
练习2：修改 decide_tool 函数，添加重试机制：
       如果 JSON 解析失败，把错误信息反馈给 LLM，让它重新输出。
       （这是 Agent 中常用的"自我修复"模式）
       
练习3：实现一个"多工具决策器"，支持一次请求调用多个工具。
       例如："帮我查北京天气，然后发邮件告诉老板"
       应该输出两个工具调用：get_weather + send_email
"""
