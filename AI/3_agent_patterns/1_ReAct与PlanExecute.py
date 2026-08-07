"""
第3阶段：Agent 设计模式
========================

学习目标：
1. 理解 Agent 的核心设计模式
2. 实现 ReAct 模式（推理+行动）
3. 实现 Plan-and-Execute 模式（规划+执行）
4. 实现 Reflexion 模式（反思+改进）
5. 理解不同模式的适用场景

Agent 设计模式是 Agent 的"大脑架构"——决定了 Agent 如何思考和行动。
不同的模式适用于不同类型的任务。
"""

import os
import json
from openai import OpenAI
from typing import Optional

client = OpenAI(
    api_key=os.environ.get('AI_DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)


# ============================================================
# 1. Agent 设计模式概览
# ============================================================
"""
┌─────────────────────────────────────────────────────────────────┐
│                    Agent 设计模式对比                             │
├──────────────┬──────────────────────────────────────────────────┤
│  模式        │  核心思想                                        │
├──────────────┼──────────────────────────────────────────────────┤
│  ReAct       │  交替进行推理(Think)和行动(Act)，逐步解决问题      │
│              │  适合：需要多步推理的复杂任务                       │
├──────────────┼──────────────────────────────────────────────────┤
│  Plan-Execute│  先制定完整计划，再逐步执行，可动态调整计划          │
│              │  适合：步骤明确的长任务                             │
├──────────────┼──────────────────────────────────────────────────┤
│  Reflexion   │  执行后反思结果，发现不足，改进后重试               │
│              │  适合：需要高质量输出的任务                         │
├──────────────┼──────────────────────────────────────────────────┤
│  LATS        │  树搜索 + LLM 评估，探索多种可能路径               │
│              │  适合：决策空间大的任务                             │
└──────────────┴──────────────────────────────────────────────────┘
"""


# ============================================================
# 2. ReAct 模式 —— 最经典的 Agent 模式
# ============================================================
"""
ReAct = Reasoning + Acting

核心循环：
  Thought: 我需要先查一下北京的天气    （推理）
  Action:  调用 get_weather("北京")    （行动）
  Observation: 北京 28°C，晴天          （观察）
  Thought: 天气不错，适合出门           （推理）
  Action:  直接回答用户                 （行动）

与简单的 Function Calling 不同：
- ReAct 的每一步都有明确的"思考"过程
- 思考过程帮助 LLM 做出更好的决策
- 思考过程也方便人类理解 Agent 的决策逻辑
"""

# --- 工具定义（复用之前的）---
def get_weather(city: str) -> str:
    weather_data = {
        "北京": {"temp": 28, "condition": "晴天", "humidity": 45},
        "上海": {"temp": 32, "condition": "多云", "humidity": 70},
        "深圳": {"temp": 35, "condition": "雷阵雨", "humidity": 85},
    }
    data = weather_data.get(city, {"temp": 25, "condition": "未知", "humidity": 50})
    return json.dumps({"city": city, **data}, ensure_ascii=False)

def calculate(expression: str) -> str:
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return json.dumps({"error": "不安全的表达式"}, ensure_ascii=False)
    try:
        return json.dumps({"result": eval(expression)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

def search_web(query: str) -> str:
    mock = {
        "Python": "Python 是一种广泛使用的高级编程语言。",
        "AI Agent": "AI Agent 是能自主感知、决策、执行的智能体。",
    }
    for key, value in mock.items():
        if key.lower() in query.lower():
            return json.dumps({"result": value}, ensure_ascii=False)
    return json.dumps({"result": "未找到相关结果"}, ensure_ascii=False)

def get_current_time() -> str:
    from datetime import datetime
    now = datetime.now()
    return json.dumps({"time": now.strftime("%Y-%m-%d %H:%M:%S")}, ensure_ascii=False)

tools_map = {
    "get_weather": get_weather,
    "calculate": calculate,
    "search_web": search_web,
    "get_current_time": get_current_time,
}

tools_schema = [
    {"type": "function", "function": {"name": "get_weather", "description": "获取城市天气", "parameters": {"type": "object", "properties": {"city": {"type": "string", "description": "城市名"}}, "required": ["city"]}}},
    {"type": "function", "function": {"name": "calculate", "description": "执行数学计算", "parameters": {"type": "object", "properties": {"expression": {"type": "string", "description": "数学表达式"}}, "required": ["expression"]}}},
    {"type": "function", "function": {"name": "search_web", "description": "搜索互联网", "parameters": {"type": "object", "properties": {"query": {"type": "string", "description": "搜索关键词"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "get_current_time", "description": "获取当前时间", "parameters": {"type": "object", "properties": {}, "required": []}}},
]


# ============================================================
# 流式调用辅助函数
# ============================================================
def chat_stream(messages: list, **kwargs) -> tuple[str, list | None]:
    """
    流式调用 LLM 的辅助函数（打字机效果）
    
    核心能力：
    1. 最终回答：逐字实时打印，不用干等全部生成完
    2. 工具调用：流式模式下 tool_calls 的 arguments 是分块到达的，
       这里自动按 index 组装成完整结构
    
    Args:
        messages: 消息列表
        **kwargs: 其他参数（tools、temperature 等），model 默认 deepseek-chat
        
    Returns:
        content: 完整的回答文本（纯文本回答时非空）
        tool_calls: 组装好的工具调用列表，没有则为 None，格式：
            [{"id": "call_xxx", "type": "function",
              "function": {"name": "...", "arguments": "{\"city\": \"北京\"}"}}]
    """
    stream_response = client.chat.completions.create(
        model=kwargs.pop("model", "deepseek-chat"),
        messages=messages,
        stream=True,
        **kwargs
    )
    
    content_parts: list[str] = []
    tool_calls_acc: dict[int, dict] = {}  # 按 index 累积工具调用
    
    for chunk in stream_response:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        
        # 1. 文本内容：累积并实时打印（打字机效果）
        if delta.content:
            content_parts.append(delta.content)
            print(delta.content, end="", flush=True)
        
        # 2. 工具调用：arguments 分块到达，必须拼接
        if delta.tool_calls:
            for tc in delta.tool_calls:
                idx = tc.index
                if idx not in tool_calls_acc:
                    tool_calls_acc[idx] = {
                        "id": "",
                        "type": "function",
                        "function": {"name": "", "arguments": ""}
                    }
                if tc.id:
                    tool_calls_acc[idx]["id"] = tc.id
                if tc.function:
                    if tc.function.name:
                        tool_calls_acc[idx]["function"]["name"] += tc.function.name
                    if tc.function.arguments:
                        tool_calls_acc[idx]["function"]["arguments"] += tc.function.arguments
    
    # 文本输出完毕，换行
    if content_parts:
        print()
    
    # 按 index 排序，保证工具调用顺序正确
    tool_calls = None
    if tool_calls_acc:
        tool_calls = [tool_calls_acc[i] for i in sorted(tool_calls_acc.keys())]
    
    return "".join(content_parts), tool_calls


REACT_SYSTEM_PROMPT = """你是一个使用 ReAct 模式的智能助手。

对于每个问题，你需要按以下格式思考和行动：

Thought: [分析问题，思考下一步该做什么]
Action: [调用工具或给出最终回答]

可用工具：
- get_weather(city): 获取城市天气
- calculate(expression): 执行数学计算
- search_web(query): 搜索互联网
- get_current_time(): 获取当前时间

当你有了足够的信息可以回答用户问题时，使用以下格式：
Thought: [总结你获得的信息]
Answer: [给用户的最终回答]

请一步一步思考，每次只执行一个行动。"""


class ReActAgent:
    """
    ReAct 模式的 Agent
    
    特点：
    - 每一步都有明确的思考过程
    - 思考过程记录在对话历史中，帮助后续决策
    - 方便调试和理解 Agent 的决策逻辑
    """
    
    def __init__(self, system_prompt: str = REACT_SYSTEM_PROMPT):
        self.system_prompt = system_prompt
        self.thought_history: list[str] = []  # 记录思考过程
    
    def run(self, user_query: str, max_steps: int = 6) -> str:
        """运行 ReAct Agent（流式版）"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_query}
        ]
        
        for step in range(max_steps):
            print(f"\n{'='*40} 步骤 {step+1} {'='*40}")
            
            # 流式调用：最终回答会逐字实时输出，工具调用会被自动组装
            content, tool_calls = chat_stream(
                messages,
                tools=tools_schema,
                tool_choice="auto",
                temperature=0
            )
            
            # 情况1：LLM 决定调用工具
            if tool_calls:
                # ⚠️ 流式模式拿到的不是完整消息对象，需要用 dict 重构后加入历史
                messages.append({
                    "role": "assistant",
                    "content": content or None,
                    "tool_calls": tool_calls
                })
                
                for tc in tool_calls:
                    func_name = tc["function"]["name"]
                    func_args = json.loads(tc["function"]["arguments"])
                    
                    print(f"💭 Thought: 需要调用 {func_name}")
                    print(f"🔧 Action: {func_name}({func_args})")
                    
                    # 执行工具
                    result = tools_map[func_name](**func_args)
                    print(f"👁️ Observation: {result[:100]}")
                    
                    # 记录思考过程
                    self.thought_history.append(
                        f"步骤{step+1}: 调用 {func_name}({func_args}) → {result[:80]}"
                    )
                    
                    # 反馈结果（tool 消息必须通过 tool_call_id 关联到上面的调用）
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": result
                    })
            else:
                # 情况2：LLM 直接回答（内容已经在流式时逐字打印过了）
                print(f"\n💭 Thought: 已有足够信息回答")
                return content
        
        return "达到最大步骤数，Agent 停止。"
    
    def get_thought_process(self) -> list[str]:
        """获取 Agent 的思考过程（方便调试）"""
        return self.thought_history.copy()


# 测试 ReAct Agent
agent = ReActAgent()
result = agent.run("北京和上海哪个城市更热？我应该去哪个城市出差？")
print("\n思考过程:", agent.get_thought_process())


# ============================================================
# 3. Plan-and-Execute 模式 —— 先规划再执行
# ============================================================
"""
Plan-and-Execute 模式将任务分为两个阶段：

1. 规划阶段：LLM 制定完整的执行计划
2. 执行阶段：逐步执行计划中的每一步

优势：
- 适合步骤明确的长任务
- 计划可以提前审查
- 执行过程中可以动态调整计划

与 ReAct 的区别：
- ReAct：边想边做，每一步都重新思考
- Plan-Execute：先想好全部步骤，再逐步执行
"""

PLAN_SYSTEM_PROMPT = """你是一个任务规划专家。

用户会给你一个任务，你需要制定一个详细的执行计划。

输出 JSON 格式：
{
    "goal": "任务目标",
    "steps": [
        {"step": 1, "action": "具体操作描述", "tool": "工具名（如果需要）", "args": {"参数": "值"}},
        {"step": 2, "action": "...", "tool": "...", "args": {...}},
        ...
    ]
}

可用工具：
- get_weather(city): 获取城市天气
- calculate(expression): 执行数学计算
- search_web(query): 搜索互联网
- get_current_time(): 获取当前时间

如果某步不需要工具，tool 设为 null。
请制定最少步骤的计划。"""


class PlanExecuteAgent:
    """
    Plan-and-Execute 模式的 Agent
    
    特点：
    - 先制定完整计划
    - 逐步执行计划
    - 执行后可重新规划
    """
    
    def __init__(self):
        self.plan: Optional[dict] = None
        self.execution_results: list[dict] = []
    
    def plan_task(self, user_query: str) -> dict:
        """规划阶段：制定执行计划"""
        print("📋 规划阶段（流式输出）...")
        
        # 流式输出计划 JSON（打字机效果）
        content, _ = chat_stream(
            messages=[
                {"role": "system", "content": PLAN_SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ],
            temperature=0
        )
        content = content.strip()
        # 清理 markdown
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        try:
            plan = json.loads(content)
        except json.JSONDecodeError:
            # 降级：单步计划
            plan = {
                "goal": user_query,
                "steps": [{"step": 1, "action": "直接回答", "tool": None, "args": {}}]
            }
        
        self.plan = plan
        
        # 打印计划
        print(f"  目标: {plan.get('goal', '未知')}")
        for step in plan.get("steps", []):
            tool_info = f" [工具: {step.get('tool')}]" if step.get('tool') else ""
            print(f"  步骤{step['step']}: {step['action']}{tool_info}")
        
        return plan
    
    def execute_plan(self) -> str:
        """执行阶段：逐步执行计划"""
        if not self.plan:
            return "没有计划可执行"
        
        print("\n🚀 执行阶段...")
        self.execution_results = []
        context = ""  # 累积执行结果
        
        for step in self.plan.get("steps", []):
            step_num = step["step"]
            action = step["action"]
            tool = step.get("tool")
            args = step.get("args", {})
            
            print(f"\n  执行步骤{step_num}: {action}")
            
            if tool and tool in tools_map:
                # 执行工具
                result = tools_map[tool](**args)
                print(f"  结果: {result[:100]}")
                self.execution_results.append({
                    "step": step_num,
                    "action": action,
                    "tool": tool,
                    "result": result
                })
                context += f"步骤{step_num}({action}): {result}\n"
            else:
                # 不需要工具，记录
                self.execution_results.append({
                    "step": step_num,
                    "action": action,
                    "tool": None,
                    "result": "无需工具"
                })
        
        # 根据所有执行结果生成最终回答（流式逐字输出）
        print("\n📝 生成最终回答（流式输出）...")
        final_answer, _ = chat_stream(
            messages=[
                {"role": "system", "content": "根据以下执行结果，用中文给用户一个完整、清晰的回答。"},
                {"role": "user", "content": f"任务: {self.plan['goal']}\n\n执行结果:\n{context}"}
            ],
            temperature=0.3
        )
        return final_answer
    
    def run(self, user_query: str) -> str:
        """完整的 Plan-Execute 流程"""
        self.plan_task(user_query)
        return self.execute_plan()


# 测试 Plan-Execute Agent
# pe_agent = PlanExecuteAgent()
# result = pe_agent.run("帮我比较北京和上海的天气，然后计算两地的温差")


# ============================================================
# 4. Reflexion 模式 —— 反思与改进
# ============================================================
"""
Reflexion 模式在执行后增加了一个"反思"环节：

1. 执行任务，得到初始结果
2. 反思结果，找出不足
3. 根据反思改进，重新执行
4. 重复直到满意或达到最大次数

适用场景：
- 代码生成（反思代码质量）
- 文案写作（反思表达效果）
- 复杂推理（反思逻辑是否正确）
"""

class ReflexionAgent:
    """
    Reflexion 模式的 Agent
    
    特点：
    - 执行后自动反思
    - 根据反思改进
    - 迭代优化结果
    """
    
    def __init__(self, max_reflections: int = 3):
        self.max_reflections = max_reflections
        self.reflection_history: list[dict] = []
    
    def _generate(self, task: str, previous_reflections: str = "") -> str:
        """生成初始结果"""
        prompt = f"请完成以下任务：{task}"
        if previous_reflections:
            prompt += f"\n\n之前的反思和改进建议：\n{previous_reflections}\n\n请根据反思改进你的回答。"
        
        # 流式生成（逐字输出）
        content, _ = chat_stream(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return content
    
    def _reflect(self, task: str, result: str) -> str:
        """反思结果，找出不足"""
        content, _ = chat_stream(
            messages=[
                {
                    "role": "system",
                    "content": """你是一个严格的评审员。审查以下任务完成结果，找出不足之处。

输出格式：
1. 优点：...
2. 不足：...
3. 改进建议：...

要具体、有建设性。"""
                },
                {
                    "role": "user",
                    "content": f"任务：{task}\n\n结果：\n{result}"
                }
            ],
            temperature=0
        )
        return content
    
    def run(self, task: str) -> str:
        """运行 Reflexion Agent"""
        current_result = ""
        all_reflections = ""
        
        for i in range(self.max_reflections):
            print(f"\n{'='*40} 第 {i+1} 轮 {'='*40}")
            
            # 生成/改进结果（流式逐字输出）
            print("📝 生成中（流式输出）...")
            current_result = self._generate(task, all_reflections)
            
            # 反思（流式输出）
            print("\n🤔 反思中（流式输出）...")
            reflection = self._reflect(task, current_result)
            
            self.reflection_history.append({
                "round": i + 1,
                "result_preview": current_result[:100],
                "reflection_preview": reflection[:100]
            })
            
            # 累积反思
            all_reflections += f"\n第{i+1}轮反思：\n{reflection}\n"
        
        print(f"\n✅ 经过 {self.max_reflections} 轮反思，最终结果已在上面逐字输出")
        return current_result


# 测试 Reflexion Agent
# reflex_agent = ReflexionAgent(max_reflections=2)
# result = reflex_agent.run("写一个 Python 函数，实现二分查找算法，要求代码健壮、有完整注释和类型注解")


# ============================================================
# 5. 模式选择指南
# ============================================================
"""
┌──────────────────────────────────────────────────────────────┐
│                    如何选择 Agent 模式？                       │
├──────────────────┬───────────────────────────────────────────┤
│  任务特征        │  推荐模式                                  │
├──────────────────┼───────────────────────────────────────────┤
│  需要多步推理    │  ReAct                                    │
│  步骤可预先规划  │  Plan-and-Execute                         │
│  需要高质量输出  │  Reflexion                                │
│  简单问答        │  直接 LLM 调用（不需要 Agent）              │
│  需要探索多种可能│  LATS（树搜索）                            │
│  长任务+可调整   │  Plan-and-Execute + 动态重规划              │
└──────────────────┴───────────────────────────────────────────┘

实际项目中，通常会组合使用多种模式：
- Plan-Execute 规划 + ReAct 执行每一步
- ReAct 执行 + Reflexion 反思关键步骤
"""


# ============================================================
# 💡 练习
# ============================================================
"""
练习1：实现一个"动态重规划"的 Plan-Execute Agent：
       - 执行某一步失败时，重新规划剩余步骤
       - 执行结果与预期不符时，调整计划
       
练习2：组合 ReAct + Reflexion：
       - 用 ReAct 模式执行任务
       - 每次工具调用后，用 Reflexion 判断结果是否可靠
       - 如果不可靠，换一种方式重新获取信息

练习3：实现一个"自适应 Agent"：
       - 先用简单模式尝试回答
       - 如果回答质量不够，自动升级到更复杂的模式
       - 例如：直接回答 → ReAct → Plan-Execute + Reflexion

练习4（进阶）：实现 LATS（Language Agent Tree Search）模式：
       - 每一步生成多个可能的行动
       - 用 LLM 评估每个行动的价值
       - 选择最有价值的路径继续探索
       - 类似下棋 AI 的搜索树
"""
