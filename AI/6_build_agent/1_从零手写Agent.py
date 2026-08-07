"""
第6阶段：从零手写一个完整 Agent
================================

学习目标：
1. 不依赖任何框架，从零实现一个完整的 Agent
2. 理解 Agent 的每一个组件和它们如何协作
3. 实现完整的 Agent 循环：感知 → 推理 → 行动 → 观察
4. 添加记忆、规划、自我修复等高级能力

这是最重要的一个阶段！
用框架（LangChain）开发 Agent 很快，但理解底层原理才能：
- 遇到问题时快速定位和修复
- 根据需求定制 Agent 行为
- 评估和优化 Agent 性能
- 面试时展示深度理解
"""

import os
import json
import time
from typing import Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from openai import OpenAI


# ============================================================
# 1. Agent 核心数据结构
# ============================================================

class AgentState(Enum):
    """Agent 状态"""
    IDLE = "idle"           # 空闲，等待输入
    THINKING = "thinking"   # 正在思考
    ACTING = "acting"       # 正在执行工具
    OBSERVING = "observing" # 正在观察结果
    RESPONDING = "responding"  # 正在生成回答
    ERROR = "error"         # 出错


@dataclass
class ToolCall:
    """工具调用记录"""
    tool_name: str
    arguments: dict
    result: Optional[str] = None
    error: Optional[str] = None
    start_time: float = 0
    end_time: float = 0
    
    @property
    def duration(self) -> float:
        return self.end_time - self.start_time if self.end_time else 0


@dataclass
class AgentStep:
    """Agent 执行步骤"""
    step_number: int
    thought: str = ""           # Agent 的思考
    tool_calls: list[ToolCall] = field(default_factory=list)  # 工具调用
    observation: str = ""       # 观察结果
    state: AgentState = AgentState.IDLE


@dataclass
class AgentResult:
    """Agent 执行结果"""
    answer: str
    steps: list[AgentStep] = field(default_factory=list)
    total_time: float = 0
    total_tool_calls: int = 0
    success: bool = True
    error: Optional[str] = None


# ============================================================
# 2. 工具系统
# ============================================================

@dataclass
class Tool:
    """工具定义"""
    name: str
    description: str
    func: Callable
    parameters_schema: dict
    timeout: float = 30.0
    
    def execute(self, **kwargs) -> str:
        """执行工具"""
        try:
            result = self.func(**kwargs)
            return result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    def to_openai_schema(self) -> dict:
        """转换为 OpenAI tools 格式"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters_schema
            }
        }


class ToolManager:
    """工具管理器"""
    
    def __init__(self):
        self._tools: dict[str, Tool] = {}
    
    def register(self, tool: Tool):
        self._tools[tool.name] = tool
    
    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)
    
    def list_tools(self) -> list[str]:
        return list(self._tools.keys())
    
    def get_schemas(self) -> list[dict]:
        return [tool.to_openai_schema() for tool in self._tools.values()]
    
    def execute(self, name: str, **kwargs) -> str:
        tool = self._tools.get(name)
        if not tool:
            return json.dumps({"error": f"工具不存在: {name}"}, ensure_ascii=False)
        return tool.execute(**kwargs)


# ============================================================
# 3. 记忆系统
# ============================================================

class Memory:
    """
    Agent 的记忆系统
    
    支持三种记忆：
    1. 短期记忆：当前对话的消息历史
    2. 工作记忆：当前任务的执行步骤
    3. 长期记忆：历史对话摘要（可选）
    """
    
    def __init__(self, max_messages: int = 50):
        self.max_messages = max_messages
        self.messages: list[dict] = []       # 短期记忆
        self.steps: list[AgentStep] = []     # 工作记忆
        self.summary: str = ""               # 长期记忆（摘要）
    
    def add_message(self, role: str, content: str, **kwargs):
        """添加消息"""
        msg = {"role": role, "content": content, **kwargs}
        self.messages.append(msg)
        
        # 超过限制时，摘要旧消息
        if len(self.messages) > self.max_messages:
            self._compress_messages()
    
    def add_step(self, step: AgentStep):
        """添加执行步骤"""
        self.steps.append(step)
    
    def get_messages(self) -> list[dict]:
        """获取消息历史"""
        return self.messages.copy()
    
    def get_steps_summary(self) -> str:
        """获取执行步骤摘要"""
        if not self.steps:
            return "暂无执行步骤"
        
        lines = []
        for step in self.steps:
            line = f"步骤{step.step_number}: {step.thought}"
            for tc in step.tool_calls:
                line += f" → 调用{tc.tool_name}({tc.arguments})"
                if tc.result:
                    line += f" → 结果: {tc.result[:50]}"
            lines.append(line)
        return "\n".join(lines)
    
    def _compress_messages(self):
        """压缩消息历史（保留 system + 最近的消息）"""
        system_msgs = [m for m in self.messages if m["role"] == "system"]
        other_msgs = [m for m in self.messages if m["role"] != "system"]
        
        # 保留最近的消息
        keep_count = self.max_messages // 2
        kept = other_msgs[-keep_count:]
        
        # 对旧消息生成摘要
        old = other_msgs[:-keep_count]
        if old:
            self.summary += f"\n[历史摘要: {len(old)}条消息被压缩]"
        
        self.messages = system_msgs + [{"role": "system", "content": self.summary}] + kept
    
    def clear(self, keep_system: bool = True):
        """清空记忆"""
        if keep_system:
            self.messages = [m for m in self.messages if m["role"] == "system"]
        else:
            self.messages = []
        self.steps = []
        self.summary = ""


# ============================================================
# 4. Agent 核心 —— 决策循环
# ============================================================

class Agent:
    """
    完整的 AI Agent
    
    组件：
    - LLM：大脑，负责推理和决策
    - ToolManager：手，负责执行工具
    - Memory：记忆，负责维护上下文
    
    核心循环：
    1. 感知：接收用户输入
    2. 推理：LLM 分析问题，决定下一步
    3. 行动：执行工具调用
    4. 观察：获取工具结果
    5. 重复 2-4 直到得出最终回答
    """
    
    def __init__(
        self,
        name: str = "Assistant",
        system_prompt: str = "你是一个智能助手，可以调用工具帮助用户。用中文回答。",
        model: str = "deepseek-chat",
        max_steps: int = 8,
        verbose: bool = True
    ):
        self.name = name
        self.model = model
        self.max_steps = max_steps
        self.verbose = verbose
        
        # 初始化组件
        self.client = OpenAI(
            api_key=os.environ.get('AI_DEEPSEEK_API_KEY'),
            base_url="https://api.deepseek.com"
        )
        self.tool_manager = ToolManager()
        self.memory = Memory()
        
        # 设置 system prompt
        self.memory.add_message("system", system_prompt)
        
        # 状态
        self.state = AgentState.IDLE
        self._step_counter = 0
    
    def add_tool(self, name: str, description: str, func: Callable,
                 parameters_schema: dict, timeout: float = 30.0):
        """添加工具"""
        tool = Tool(
            name=name,
            description=description,
            func=func,
            parameters_schema=parameters_schema,
            timeout=timeout
        )
        self.tool_manager.register(tool)
        if self.verbose:
            print(f"  🔧 注册工具: {name}")
    
    def run(self, user_input: str) -> AgentResult:
        """
        运行 Agent 处理用户输入
        
        这是 Agent 的主循环！
        """
        start_time = time.time()
        self._step_counter = 0
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"🤖 Agent [{self.name}] 开始处理")
            print(f"❓ 用户: {user_input}")
            print(f"{'='*60}")
        
        # 添加用户消息到记忆
        self.memory.add_message("user", user_input)
        
        # Agent 主循环
        while self._step_counter < self.max_steps:
            self._step_counter += 1
            step = AgentStep(step_number=self._step_counter)
            
            if self.verbose:
                print(f"\n--- 步骤 {self._step_counter} ---")
            
            # 1. 推理：调用 LLM
            self.state = AgentState.THINKING
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.memory.get_messages(),
                    tools=self.tool_manager.get_schemas() if self.tool_manager.list_tools() else None,
                    tool_choice="auto" if self.tool_manager.list_tools() else None,
                    temperature=0,
                    stream=False
                )
                message = response.choices[0].message
            except Exception as e:
                self.state = AgentState.ERROR
                if self.verbose:
                    print(f"❌ LLM 调用失败: {e}")
                return AgentResult(
                    answer="抱歉，处理时出错了。",
                    steps=self.memory.steps,
                    total_time=time.time() - start_time,
                    success=False,
                    error=str(e)
                )
            
            # 2. 判断：LLM 是要调用工具还是直接回答
            if message.tool_calls:
                # 需要调用工具
                self.state = AgentState.ACTING
                # 把完整的 tool_calls 消息加入历史
                # ⚠️ 注意：message 对象本身已包含 role="assistant" 和 tool_calls，
                #    必须原样追加，不能拆成纯文本重新添加，否则会破坏对话关联
                self.memory.messages.append(message)
                
                all_observations = []
                for tool_call in message.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)
                    
                    if self.verbose:
                        print(f"  🔧 调用: {func_name}({func_args})")
                    
                    # 执行工具
                    tc = ToolCall(
                        tool_name=func_name,
                        arguments=func_args,
                        start_time=time.time()
                    )
                    
                    result = self.tool_manager.execute(func_name, **func_args)
                    tc.result = result
                    tc.end_time = time.time()
                    
                    step.tool_calls.append(tc)
                    all_observations.append(f"{func_name}: {result}")
                    
                    if self.verbose:
                        print(f"  📋 结果: {result[:80]}")
                    
                    # 把工具结果反馈给 LLM
                    self.memory.add_message(
                        "tool", result,
                        tool_call_id=tool_call.id
                    )
                
                step.observation = "\n".join(all_observations)
                step.thought = f"调用了 {len(message.tool_calls)} 个工具"
                self.state = AgentState.OBSERVING
                
            else:
                # LLM 直接回答
                self.state = AgentState.RESPONDING
                answer = message.content
                self.memory.add_message("assistant", answer)
                
                step.thought = "生成最终回答"
                self.memory.add_step(step)
                
                if self.verbose:
                    print(f"  ✅ 回答: {answer[:200]}")
                
                return AgentResult(
                    answer=answer,
                    steps=self.memory.steps + [step],
                    total_time=time.time() - start_time,
                    total_tool_calls=sum(len(s.tool_calls) for s in self.memory.steps) + len(step.tool_calls),
                    success=True
                )
            
            self.memory.add_step(step)
        
        # 达到最大步骤数
        if self.verbose:
            print(f"  ⚠️ 达到最大步骤数 {self.max_steps}")
        
        return AgentResult(
            answer="抱歉，我无法在有限的步骤内完成这个任务。",
            steps=self.memory.steps,
            total_time=time.time() - start_time,
            total_tool_calls=sum(len(s.tool_calls) for s in self.memory.steps),
            success=False,
            error="达到最大步骤数"
        )
    
    def chat(self, user_input: str) -> str:
        """简化的对话接口"""
        result = self.run(user_input)
        return result.answer
    
    def reset(self):
        """重置 Agent（保留工具和 system prompt）"""
        self.memory.clear(keep_system=True)
        self._step_counter = 0
        self.state = AgentState.IDLE


# ============================================================
# 5. 创建并运行 Agent
# ============================================================

# 创建 Agent
agent = Agent(
    name="Python助手",
    system_prompt="""你是一个智能助手，可以调用工具帮助用户。

规则：
1. 一步一步思考问题
2. 需要外部信息时调用工具
3. 基于工具返回的结果回答
4. 用中文回答
""",
    max_steps=6,
    verbose=True
)

# 注册工具
def get_weather(city: str) -> str:
    weather_data = {
        "北京": {"temp": 28, "condition": "晴天"},
        "上海": {"temp": 32, "condition": "多云"},
        "深圳": {"temp": 35, "condition": "雷阵雨"},
    }
    data = weather_data.get(city, {"temp": 25, "condition": "未知"})
    return json.dumps({"city": city, **data}, ensure_ascii=False)

agent.add_tool(
    name="get_weather",
    description="获取指定城市的天气信息",
    func=get_weather,
    parameters_schema={
        "type": "object",
        "properties": {"city": {"type": "string", "description": "城市名称"}},
        "required": ["city"]
    }
)

def calculate(expression: str) -> str:
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return json.dumps({"error": "不安全的表达式"}, ensure_ascii=False)
    try:
        return json.dumps({"result": eval(expression)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

agent.add_tool(
    name="calculate",
    description="执行数学计算",
    func=calculate,
    parameters_schema={
        "type": "object",
        "properties": {"expression": {"type": "string", "description": "数学表达式"}},
        "required": ["expression"]
    }
)

def get_current_time() -> str:
    from datetime import datetime
    now = datetime.now()
    return json.dumps({"time": now.strftime("%Y-%m-%d %H:%M:%S")}, ensure_ascii=False)

agent.add_tool(
    name="get_current_time",
    description="获取当前时间",
    func=get_current_time,
    parameters_schema={"type": "object", "properties": {}, "required": []}
)

# 运行 Agent
result = agent.run("北京和上海哪个更热？温差是多少？")
print(f"\n最终回答: {result.answer}")
print(f"总步骤: {len(result.steps)}, 工具调用: {result.total_tool_calls}, 耗时: {result.total_time:.2f}s")

# 多轮对话
rs = agent.chat("现在几点了？")
print(f"\n回答: {rs}")
rs = agent.chat("北京天气怎么样？")  # Agent 记得之前的对话
print(f"\n回答: {rs}")

# ============================================================
# 6. Agent 的自我修复能力
# ============================================================

class SelfHealingAgent(Agent):
    """
    带自我修复能力的 Agent
    
    当工具调用失败或 LLM 输出异常时，自动尝试修复：
    1. 工具调用失败 → 反馈错误给 LLM，让它换一种方式
    2. JSON 解析失败 → 反馈格式错误，让 LLM 重新输出
    3. 达到最大步骤 → 尝试总结已有信息给出部分回答
    """
    
    def run(self, user_input: str) -> AgentResult:
        """带自我修复的 Agent 循环"""
        start_time = time.time()
        self._step_counter = 0
        
        self.memory.add_message("user", user_input)
        
        consecutive_errors = 0
        max_errors = 3
        
        while self._step_counter < self.max_steps:
            self._step_counter += 1
            
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.memory.get_messages(),
                    tools=self.tool_manager.get_schemas() if self.tool_manager.list_tools() else None,
                    tool_choice="auto" if self.tool_manager.list_tools() else None,
                    temperature=0,
                    stream=False
                )
                message = response.choices[0].message
                consecutive_errors = 0  # 重置错误计数
                
            except Exception as e:
                consecutive_errors += 1
                if consecutive_errors >= max_errors:
                    return AgentResult(
                        answer="抱歉，服务暂时不可用，请稍后重试。",
                        steps=self.memory.steps,
                        total_time=time.time() - start_time,
                        success=False,
                        error=str(e)
                    )
                # 等待后重试
                time.sleep(2 ** consecutive_errors)
                continue
            
            if message.tool_calls:
                self.memory.messages.append(message)
                
                for tool_call in message.tool_calls:
                    func_name = tool_call.function.name
                    func_args_str = tool_call.function.arguments
                    
                    # 自我修复：JSON 解析失败时
                    try:
                        func_args = json.loads(func_args_str)
                    except json.JSONDecodeError:
                        # 反馈给 LLM，让它重新输出
                        self.memory.add_message(
                            "tool",
                            json.dumps({"error": f"参数 JSON 解析失败: {func_args_str}，请重新输出正确的 JSON 格式"}, ensure_ascii=False),
                            tool_call_id=tool_call.id
                        )
                        continue
                    
                    # 执行工具
                    result = self.tool_manager.execute(func_name, **func_args)
                    
                    # 自我修复：工具执行失败时
                    try:
                        result_data = json.loads(result)
                        if "error" in result_data:
                            # 反馈错误给 LLM
                            self.memory.add_message(
                                "tool",
                                json.dumps({
                                    "error": f"工具 {func_name} 执行失败: {result_data['error']}",
                                    "suggestion": "请尝试其他方式完成任务"
                                }, ensure_ascii=False),
                                tool_call_id=tool_call.id
                            )
                            continue
                    except json.JSONDecodeError:
                        pass
                    
                    self.memory.add_message("tool", result, tool_call_id=tool_call.id)
            else:
                answer = message.content
                self.memory.add_message("assistant", answer)
                return AgentResult(
                    answer=answer,
                    steps=self.memory.steps,
                    total_time=time.time() - start_time,
                    success=True
                )
        
        # 自我修复：达到最大步骤时，尝试总结
        self.memory.add_message("user", "请根据目前获得的信息，给出你能做到的最佳回答。")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.memory.get_messages(),
                temperature=0.3,
                stream=False
            )
            answer = response.choices[0].message.content
        except:
            answer = "抱歉，我无法完成这个任务。"
        
        return AgentResult(
            answer=answer,
            steps=self.memory.steps,
            total_time=time.time() - start_time,
            success=False,
            error="达到最大步骤数，但给出了部分回答"
        )


# ============================================================
# 💡 练习
# ============================================================
"""
练习1：为 Agent 添加"计划"能力：
       - 在执行前先让 LLM 制定计划
       - 按计划逐步执行
       - 执行过程中可以调整计划

练习2：实现 Agent 的"并行工具调用"：
       - 当 LLM 返回多个 tool_calls 时，并行执行
       - 使用 asyncio 或 ThreadPoolExecutor
       - 注意：并行执行时要注意工具间的依赖关系

练习3：实现 Agent 的"工具学习"能力：
       - Agent 遇到无法完成的任务时，可以"学习"新工具
       - 用户可以动态添加工具
       - Agent 自动理解新工具的用途

练习4（进阶）：实现一个"元认知 Agent"：
       - Agent 能评估自己的能力边界
       - 对于超出能力的问题，主动说明
       - 能建议用户如何分解问题
"""
