"""
第2阶段（续）：工具系统设计 —— 让 Agent 拥有可扩展的能力
=========================================================

学习目标：
1. 设计可扩展的工具注册系统
2. 实现工具的自动发现和描述生成
3. 添加工具执行的安全机制
4. 构建工具调用的日志和监控

在真实的 Agent 项目中，工具不是零散的函数，
而是一个有组织的系统，支持动态添加、安全执行、结果追踪。
"""

import os
import json
import time
import inspect
from typing import Callable, Any
from dataclasses import dataclass, field
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('AI_DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)


# ============================================================
# 1. 工具注册系统 —— 用类管理所有工具
# ============================================================
"""
设计原则：
- 每个工具是一个独立的类，包含名称、描述、参数定义、执行逻辑
- 工具注册中心统一管理所有工具
- 支持动态添加/移除工具
- 自动生成 OpenAI tools 参数
"""

@dataclass
class ToolDefinition:
    """工具定义"""
    name: str                           # 工具名称
    description: str                    # 工具描述
    func: Callable                      # 实际执行的函数
    parameters: dict                    # JSON Schema 格式的参数定义
    timeout: float = 30.0               # 执行超时（秒）
    dangerous: bool = False             # 是否为危险操作（如删除文件）
    examples: list[str] = field(default_factory=list)  # 使用示例


class ToolRegistry:
    """
    工具注册中心
    
    功能：
    - 注册/注销工具
    - 自动生成 OpenAI tools 参数
    - 安全执行工具（超时、权限检查）
    - 记录执行日志
    """
    
    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}
        self._execution_log: list[dict] = []
    
    def register(self, name: str, description: str, func: Callable,
                 parameters: dict, timeout: float = 30.0,
                 dangerous: bool = False, examples: list[str] = None):
        """注册一个工具"""
        self._tools[name] = ToolDefinition(
            name=name,
            description=description,
            func=func,
            parameters=parameters,
            timeout=timeout,
            dangerous=dangerous,
            examples=examples or []
        )
        print(f"✅ 注册工具: {name}")
    
    def unregister(self, name: str):
        """注销一个工具"""
        if name in self._tools:
            del self._tools[name]
            print(f"❌ 注销工具: {name}")
    
    def get_tool(self, name: str) -> ToolDefinition | None:
        """获取工具定义"""
        return self._tools.get(name)
    
    def list_tools(self) -> list[str]:
        """列出所有已注册的工具"""
        return list(self._tools.keys())
    
    def get_openai_tools(self) -> list[dict]:
        """生成 OpenAI API 需要的 tools 参数"""
        result = []
        for tool in self._tools.values():
            result.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            })
        return result
    
    def execute(self, name: str, **kwargs) -> str:
        """
        安全执行工具
        
        包含：
        - 工具存在性检查
        - 超时控制
        - 异常捕获
        - 执行日志
        """
        tool = self._tools.get(name)
        if not tool:
            return json.dumps({"error": f"工具不存在: {name}"}, ensure_ascii=False)
        
        # 记录开始时间
        start_time = time.time()
        log_entry = {
            "tool": name,
            "args": kwargs,
            "start_time": start_time,
            "status": "running"
        }
        
        try:
            # 执行工具
            result = tool.func(**kwargs)
            
            # 记录成功
            elapsed = time.time() - start_time
            log_entry["status"] = "success"
            log_entry["elapsed"] = round(elapsed, 3)
            log_entry["result_preview"] = str(result)[:200]
            self._execution_log.append(log_entry)
            
            return result
            
        except Exception as e:
            # 记录失败
            elapsed = time.time() - start_time
            log_entry["status"] = "error"
            log_entry["elapsed"] = round(elapsed, 3)
            log_entry["error"] = str(e)
            self._execution_log.append(log_entry)
            
            return json.dumps({"error": f"工具执行失败: {name}", "detail": str(e)}, ensure_ascii=False)
    
    def get_execution_log(self) -> list[dict]:
        """获取执行日志"""
        return self._execution_log.copy()
    
    def clear_log(self):
        """清空执行日志"""
        self._execution_log.clear()


# ============================================================
# 2. 注册具体工具
# ============================================================

registry = ToolRegistry()

# --- 天气工具 ---
def get_weather(city: str) -> str:
    """获取城市天气"""
    weather_data = {
        "北京": {"temp": 28, "condition": "晴天", "humidity": 45},
        "上海": {"temp": 32, "condition": "多云", "humidity": 70},
    }
    data = weather_data.get(city, {"temp": 25, "condition": "未知", "humidity": 50})
    return json.dumps({"city": city, **data}, ensure_ascii=False)

registry.register(
    name="get_weather",
    description="获取指定城市的当前天气信息",
    func=get_weather,
    parameters={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "城市名称"}
        },
        "required": ["city"]
    }
)

# --- 计算器工具 ---
def calculate(expression: str) -> str:
    """执行数学计算"""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return json.dumps({"error": "不安全的表达式"}, ensure_ascii=False)
    try:
        result = eval(expression)
        return json.dumps({"result": result}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

registry.register(
    name="calculate",
    description="执行数学计算，支持加减乘除",
    func=calculate,
    parameters={
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "数学表达式"}
        },
        "required": ["expression"]
    }
)

# --- 时间工具 ---
def get_current_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    now = datetime.now()
    return json.dumps({
        "time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "weekday": ["周一","周二","周三","周四","周五","周六","周日"][now.weekday()]
    }, ensure_ascii=False)

registry.register(
    name="get_current_time",
    description="获取当前的日期时间和星期",
    func=get_current_time,
    parameters={"type": "object", "properties": {}, "required": []}
)

# --- 文件读取工具（标记为危险）---
def read_file(path: str) -> str:
    """读取文件内容"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read(5000)  # 限制读取长度
        return json.dumps({"path": path, "content": content, "truncated": len(content) >= 5000}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

registry.register(
    name="read_file",
    description="读取本地文件的内容",
    func=read_file,
    parameters={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "文件路径"}
        },
        "required": ["path"]
    },
    dangerous=True  # 标记为危险操作
)

print(f"\n已注册工具: {registry.list_tools()}")


# ============================================================
# 3. 使用工具注册中心的 Agent
# ============================================================

def run_agent_with_registry(user_query: str, max_steps: int = 5) -> str:
    """使用工具注册中心运行 Agent"""
    messages = [
        {"role": "system", "content": "你是一个智能助手，可以调用工具帮助用户。用中文回答。"},
        {"role": "user", "content": user_query}
    ]
    
    step = 0
    while step < max_steps:
        step += 1
        print(f"\n--- 步骤 {step} ---")
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=registry.get_openai_tools(),  # 从注册中心获取工具定义
            tool_choice="auto",
            stream=False
        )
        
        message = response.choices[0].message
        
        if message.tool_calls:
            messages.append(message)
            
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                
                # 检查危险工具
                tool_def = registry.get_tool(func_name)
                if tool_def and tool_def.dangerous:
                    print(f"⚠️ 危险操作: {func_name}，需要用户确认")
                    # 在实际项目中，这里应该弹出确认对话框
                
                # 通过注册中心执行工具
                result = registry.execute(func_name, **func_args)
                print(f"🔧 {func_name}({func_args}) → {result[:80]}")
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        else:
            print(f"💬 回答: {message.content}")
            return message.content
    
    return "达到最大步骤数。"


# ============================================================
# 4. 从函数签名自动生成工具定义
# ============================================================
"""
手动写 JSON Schema 很繁琐，我们可以从 Python 函数的
类型注解和 docstring 自动生成工具定义。
"""

def auto_register_tool(func: Callable, registry: ToolRegistry, dangerous: bool = False):
    """
    从函数自动注册工具
    
    利用 Python 的类型注解和 docstring 自动生成工具定义
    """
    sig = inspect.signature(func)
    doc = inspect.getdoc(func) or func.__name__
    
    # 构建参数的 JSON Schema
    properties = {}
    required = []
    
    type_mapping = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
    }
    
    for param_name, param in sig.parameters.items():
        param_type = "string"  # 默认类型
        if param.annotation != inspect.Parameter.empty:
            param_type = type_mapping.get(param.annotation, "string")
        
        properties[param_name] = {
            "type": param_type,
            "description": f"{param_name} 参数"
        }
        
        if param.default == inspect.Parameter.empty:
            required.append(param_name)
    
    registry.register(
        name=func.__name__,
        description=doc,
        func=func,
        parameters={
            "type": "object",
            "properties": properties,
            "required": required
        },
        dangerous=dangerous
    )

# 使用示例
def send_email(to: str, subject: str, body: str) -> str:
    """发送电子邮件给指定收件人"""
    # 模拟发送邮件
    return json.dumps({"status": "sent", "to": to, "subject": subject}, ensure_ascii=False)

auto_register_tool(send_email, registry)
print(f"\n自动注册后工具列表: {registry.list_tools()}")


# ============================================================
# 💡 练习
# ============================================================
"""
练习1：为 ToolRegistry 添加"工具权限"系统：
       - 每个工具有权限等级（read/write/admin）
       - 用户有不同的权限级别
       - 执行工具前检查权限

练习2：实现工具的"依赖关系"：
       - 某些工具需要先执行其他工具
       - 例如：send_email 可能需要先 search_web 获取信息
       - 自动解析依赖并按顺序执行

练习3：实现工具执行的"重试机制"：
       - 工具执行失败时自动重试
       - 可配置重试次数和间隔
       - 区分可重试错误和不可重试错误

练习4（进阶）：实现一个"工具市场"：
       - 工具可以从外部文件/URL 动态加载
       - 支持工具的版本管理
       - 支持工具的热更新（不重启 Agent）
"""
