"""
第2阶段：Function Calling / Tool Use（Agent 的核心）
=====================================================

学习目标：
1. 理解 Function Calling 的工作原理
2. 定义工具函数的 JSON Schema
3. 实现 LLM → 工具调用 → 结果反馈的完整循环
4. 构建一个能真正调用工具的 Agent

这是 Agent 开发最关键的一步！
没有 Function Calling，LLM 只能"说话"；有了它，LLM 能"做事"。

核心流程：
  用户提问 → LLM 决定调用工具 → 返回工具名+参数 → 程序执行工具 → 结果返回 LLM → LLM 生成最终回答
"""

import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('AI_DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)


# ============================================================
# 1. 什么是 Function Calling？
# ============================================================
"""
传统方式：LLM 只能输出文本，无法执行任何操作
Function Calling：LLM 能"告诉"程序要调用什么函数，程序执行后把结果反馈给 LLM

┌──────────────────────────────────────────────────────────────┐
│                    Function Calling 流程                      │
│                                                              │
│  用户: "北京今天多少度？"                                      │
│    │                                                         │
│    ▼                                                         │
│  LLM: 我需要调用 get_weather(city="北京")                     │
│    │                                                         │
│    ▼                                                         │
│  程序: 执行 get_weather("北京") → 返回 {"temp": 28, "..."}    │
│    │                                                         │
│    ▼                                                         │
│  LLM: 根据工具返回结果，生成自然语言回答                        │
│    │                                                         │
│    ▼                                                         │
│  用户: "北京今天28°C，晴天"                                    │
└──────────────────────────────────────────────────────────────┘

关键理解：
- LLM 本身不执行函数！它只是输出"应该调用什么函数+什么参数"
- 你的程序负责实际执行函数
- 执行结果需要反馈给 LLM，它才能生成最终回答
"""


# ============================================================
# 2. 定义工具函数
# ============================================================
"""
首先，我们需要定义一些 Agent 可以调用的工具函数。
这些函数就是 Agent 的"手"——让它能与外部世界交互。
"""

# --- 工具1：获取天气 ---
def get_weather(city: str) -> str:
    """获取指定城市的天气（模拟数据）"""
    # 实际项目中，这里会调用真实的天气 API
    weather_data = {
        "北京": {"temp": 28, "condition": "晴天", "humidity": 45},
        "上海": {"temp": 32, "condition": "多云", "humidity": 70},
        "深圳": {"temp": 35, "condition": "雷阵雨", "humidity": 85},
        "成都": {"temp": 26, "condition": "阴天", "humidity": 60},
    }
    if city in weather_data:
        data = weather_data[city]
        return json.dumps({
            "city": city,
            "temperature": f"{data['temp']}°C",
            "condition": data["condition"],
            "humidity": f"{data['humidity']}%"
        }, ensure_ascii=False)
    return json.dumps({"error": f"未找到城市: {city}"}, ensure_ascii=False)


# --- 工具2：计算器 ---
def calculate(expression: str) -> str:
    """执行数学计算（安全版本）"""
    # ⚠️ 实际项目中不要用 eval()，这里仅作演示
    # 生产环境建议用 ast.literal_eval 或专门的数学解析库
    try:
        # 只允许数字和基本运算符
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return json.dumps({"error": "不安全的表达式"}, ensure_ascii=False)
        result = eval(expression)
        return json.dumps({"expression": expression, "result": result}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# --- 工具3：搜索（模拟）---
def search_web(query: str) -> str:
    """搜索互联网（模拟）"""
    # 实际项目中，这里会调用搜索 API（如 Google、Bing、Tavily）
    mock_results = {
        "Python": "Python 是一种广泛使用的高级编程语言，由 Guido van Rossum 于1991年发布。",
        "AI Agent": "AI Agent 是能够自主感知环境、做出决策并执行动作的智能体。",
        "LangChain": "LangChain 是一个用于开发 LLM 驱动应用的开源框架。",
    }
    for key, value in mock_results.items():
        if key.lower() in query.lower():
            return json.dumps({"query": query, "result": value}, ensure_ascii=False)
    return json.dumps({"query": query, "result": "未找到相关结果"}, ensure_ascii=False)


# --- 工具4：获取当前时间 ---
def get_current_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    now = datetime.now()
    return json.dumps({
        "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][now.weekday()]
    }, ensure_ascii=False)


# ============================================================
# 3. 定义工具的 JSON Schema —— 告诉 LLM 有哪些工具可用
# ============================================================
"""
tools 参数是一个列表，每个工具需要定义：
- name: 函数名（LLM 会输出这个名字）
- description: 功能描述（LLM 根据描述决定是否调用）
- parameters: 参数的 JSON Schema（LLM 根据这个生成参数）

⚠️ description 非常重要！写得好，LLM 才能正确选择工具。
"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的当前天气信息，包括温度、天气状况和湿度",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京、上海、深圳"
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
            "description": "执行数学计算，支持加减乘除和括号运算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如：2+3*4、(10+5)/3"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "搜索互联网获取信息，当需要查找最新资讯或不确定的知识时使用",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的日期、时间和星期",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

# 工具名 → 实际函数的映射
tool_functions = {
    "get_weather": get_weather,
    "calculate": calculate,
    "search_web": search_web,
    "get_current_time": get_current_time,
}


# ============================================================
# 4. 完整的 Function Calling 循环
# ============================================================
"""
这是 Agent 的核心循环！

流程：
1. 用户提问
2. LLM 决定是否调用工具
3. 如果需要调用工具 → 执行工具 → 把结果反馈给 LLM → 回到步骤2
4. 如果不需要调用工具 → LLM 生成最终回答

这个循环可能执行多次（LLM 可能需要连续调用多个工具）
"""

def run_agent(user_query: str, max_steps: int = 5) -> str:
    """
    运行一个简单的 Agent
    
    Args:
        user_query: 用户的问题
        max_steps: 最大工具调用次数（防止无限循环）
        
    Returns:
        Agent 的最终回答
    """
    messages = [
        {
            "role": "system",
            "content": "你是一个智能助手，可以调用工具来帮助用户。请用中文回答。"
        },
        {
            "role": "user",
            "content": user_query
        }
    ]
    
    step = 0
    while step < max_steps:
        step += 1
        print(f"\n--- 步骤 {step} ---")
        
        # 调用 LLM
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools,  # 传入可用工具
            tool_choice="auto",  # LLM 自动决定是否调用工具
            stream=False
        )
        
        message = response.choices[0].message
        
        # 情况1：LLM 决定调用工具
        if message.tool_calls:
            # 把 LLM 的消息（包含工具调用请求）加入历史
            messages.append(message)
            
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"🔧 调用工具: {function_name}({function_args})")
                
                # 执行工具
                if function_name in tool_functions:
                    result = tool_functions[function_name](**function_args)
                else:
                    result = json.dumps({"error": f"未知工具: {function_name}"}, ensure_ascii=False)
                
                print(f"📋 工具结果: {result[:100]}")
                
                # 把工具执行结果反馈给 LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        
        # 情况2：LLM 直接回答（不需要工具）
        else:
            print(f"💬 最终回答: {message.content}")
            return message.content
    
    return "达到最大步骤数，Agent 停止。"


# ============================================================
# 5. 测试 Agent
# ============================================================

# 测试1：需要调用工具的问题
print("=" * 60)
print("测试1：天气查询")
print("=" * 60)
# result1 = run_agent("北京今天天气怎么样？")

# 测试2：需要计算的问题
print("\n" + "=" * 60)
print("测试2：数学计算")
print("=" * 60)
# result2 = run_agent("(15 + 27) * 3 等于多少？")

# 测试3：需要搜索的问题
print("\n" + "=" * 60)
print("测试3：搜索信息")
print("=" * 60)
# result3 = run_agent("什么是 AI Agent？")

# 测试4：不需要工具的问题
print("\n" + "=" * 60)
print("测试4：直接回答")
print("=" * 60)
# result4 = run_agent("你好，请介绍一下你自己")

# 测试5：多步骤问题（需要调用多个工具）
print("\n" + "=" * 60)
print("测试5：多步骤问题")
print("=" * 60)
result5 = run_agent("现在几点了？北京天气怎么样？适合出门吗？")


# ============================================================
# 6. 手动实现 Function Calling（不使用 tools 参数）
# ============================================================
"""
有些 LLM 不支持原生的 Function Calling（tools 参数），
我们可以用 Prompt 方式手动实现同样的效果。

原理：
1. 在 System Prompt 中列出所有工具的描述和参数
2. 要求 LLM 输出 JSON 格式的工具调用请求
3. 程序解析 JSON，执行工具，把结果反馈给 LLM

这种方式更通用，适用于所有 LLM！
"""

MANUAL_TOOLS_DESCRIPTION = f"""你是一个智能助手，可以调用以下工具来帮助用户：

可用工具：
1. get_weather(city: str) - 获取城市天气
2. calculate(expression: str) - 执行数学计算
3. search_web(query: str) - 搜索互联网
4. get_current_time() - 获取当前时间

当你需要调用工具时，请输出以下 JSON 格式：
{{"tool_call": true, "name": "工具名", "args": {{"参数名": "参数值"}}}}

当你不需要调用工具，可以直接回答时，请输出：
{{"tool_call": false, "answer": "你的回答"}}

每次只调用一个工具。"""

def run_manual_agent(user_query: str, max_steps: int = 5) -> str:
    """
    手动实现 Function Calling 的 Agent
    
    适用于不支持原生 tools 参数的 LLM
    """
    messages = [
        {"role": "system", "content": MANUAL_TOOLS_DESCRIPTION},
        {"role": "user", "content": user_query}
    ]
    
    step = 0
    while step < max_steps:
        step += 1
        print(f"\n--- 步骤 {step} ---")
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0,
            stream=False
        )
        
        content = response.choices[0].message.content.strip()
        
        # 清理可能的 markdown 标记
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        try:
            decision = json.loads(content)
        except json.JSONDecodeError:
            # 不是 JSON，当作直接回答
            print(f"💬 直接回答: {content}")
            return content
        
        if decision.get("tool_call"):
            # 需要调用工具
            func_name = decision["name"]
            func_args = decision.get("args", {})
            
            print(f"🔧 调用工具: {func_name}({func_args})")
            
            # 执行工具
            if func_name in tool_functions:
                result = tool_functions[func_name](**func_args)
            else:
                result = json.dumps({"error": f"未知工具: {func_name}"}, ensure_ascii=False)
            
            print(f"📋 工具结果: {result[:100]}")
            
            # 把工具结果加入对话
            messages.append({"role": "assistant", "content": content})
            messages.append({
                "role": "user",
                "content": f"工具 {func_name} 的执行结果是：{result}\n\n请根据结果继续回答用户的问题。如果需要调用更多工具，请继续输出 JSON。"
            })
        else:
            # 直接回答
            answer = decision.get("answer", content)
            print(f"💬 最终回答: {answer}")
            return answer
    
    return "达到最大步骤数，Agent 停止。"


# ============================================================
# 💡 练习
# ============================================================
"""
练习1：添加更多工具函数：
       - send_email(to, subject, body): 发送邮件
       - read_file(path): 读取文件内容
       - list_directory(path): 列出目录内容
       并更新 tools 定义和 tool_functions 映射。

练习2：实现一个"代码执行工具"，让 Agent 能运行 Python 代码：
       - 使用 subprocess 安全执行
       - 捕获 stdout 和 stderr
       - 设置超时限制
       ⚠️ 注意安全风险，思考如何防止恶意代码执行

练习3：修改 run_agent 函数，添加对话历史管理：
       - 当历史消息超过一定长度时，自动摘要旧消息
       - 记录所有工具调用和结果，方便调试

练习4（进阶）：实现一个"工具组合"功能，
       让 Agent 能一次请求中调用多个工具（并行调用）。
"""
