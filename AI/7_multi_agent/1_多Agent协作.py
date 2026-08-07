"""
第7阶段：多 Agent 协作系统
============================

学习目标：
1. 理解多 Agent 系统的设计模式
2. 实现 Agent 间的通信机制
3. 实现任务分配和协调
4. 构建一个完整的多 Agent 协作系统

为什么需要多 Agent？
- 单个 Agent 的能力有限，不同 Agent 擅长不同领域
- 复杂任务需要多种能力协作（研究+写作+审查）
- 多 Agent 可以并行工作，提高效率
- 类似人类团队：项目经理+开发者+测试员+审查员
"""

import os
import json
import time
from typing import Optional
from dataclasses import dataclass, field
from enum import Enum
from openai import OpenAI


# ============================================================
# 1. 多 Agent 协作模式
# ============================================================
"""
┌──────────────────────────────────────────────────────────────┐
│                  多 Agent 协作模式                             │
├──────────────┬───────────────────────────────────────────────┤
│  模式        │  描述                                         │
├──────────────┼───────────────────────────────────────────────┤
│  主管-工人   │  一个主管 Agent 分配任务给多个工人 Agent        │
│  (Supervisor)│  适合：任务可以明确分解的场景                   │
├──────────────┼───────────────────────────────────────────────┤
│  辩论模式    │  多个 Agent 从不同角度讨论，达成共识            │
│  (Debate)    │  适合：需要多角度思考的决策                     │
├──────────────┼───────────────────────────────────────────────┤
│  流水线模式  │  Agent 按顺序处理，每个 Agent 负责一个阶段      │
│  (Pipeline)  │  适合：有明确步骤的任务（研究→写作→审查）       │
├──────────────┼───────────────────────────────────────────────┤
│  群聊模式    │  多个 Agent 自由讨论，主持人控制发言顺序        │
│  (GroupChat) │  适合：创意讨论、头脑风暴                      │
└──────────────┴───────────────────────────────────────────────┘
"""


# ============================================================
# 2. Agent 通信机制
# ============================================================

class MessageBus:
    """
    Agent 间的消息总线
    
    所有 Agent 通过消息总线通信，实现解耦。
    类似聊天室：Agent 发送消息到频道，其他 Agent 可以订阅频道。
    """
    
    def __init__(self):
        self._messages: list[dict] = []
        self._subscribers: dict[str, list[callable]] = {}
    
    def publish(self, channel: str, sender: str, content: str, metadata: dict = None):
        """发布消息到频道"""
        msg = {
            "channel": channel,
            "sender": sender,
            "content": content,
            "metadata": metadata or {},
            "timestamp": time.time()
        }
        self._messages.append(msg)
        
        # 通知订阅者
        for callback in self._subscribers.get(channel, []):
            callback(msg)
    
    def subscribe(self, channel: str, callback: callable):
        """订阅频道"""
        if channel not in self._subscribers:
            self._subscribers[channel] = []
        self._subscribers[channel].append(callback)
    
    def get_messages(self, channel: str = None, sender: str = None, limit: int = 10) -> list[dict]:
        """获取消息"""
        msgs = self._messages
        if channel:
            msgs = [m for m in msgs if m["channel"] == channel]
        if sender:
            msgs = [m for m in msgs if m["sender"] == sender]
        return msgs[-limit:]


# ============================================================
# 3. 基础 Agent 类
# ============================================================

class BaseAgent:
    """基础 Agent 类"""
    
    def __init__(self, name: str, role: str, system_prompt: str, model: str = "deepseek-chat"):
        self.name = name
        self.role = role
        self.model = model
        self.client = OpenAI(
            api_key=os.environ.get('AI_DEEPSEEK_API_KEY'),
            base_url="https://api.deepseek.com"
        )
        self.system_prompt = system_prompt
        self.message_history: list[dict] = [
            {"role": "system", "content": system_prompt}
        ]
    
    def think(self, input_text: str) -> str:
        """思考并回复"""
        self.message_history.append({"role": "user", "content": input_text})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.message_history,
            temperature=0.3,
            stream=False
        )
        
        reply = response.choices[0].message.content
        self.message_history.append({"role": "assistant", "content": reply})
        return reply
    
    def reset(self):
        """重置对话历史"""
        self.message_history = [{"role": "system", "content": self.system_prompt}]


# ============================================================
# 4. 主管-工人模式（Supervisor Pattern）
# ============================================================

class SupervisorAgent(BaseAgent):
    """
    主管 Agent
    
    职责：
    1. 接收用户任务
    2. 分析任务，决定分配给哪个工人
    3. 汇总工人的结果
    4. 返回最终回答
    """
    
    def __init__(self, workers: dict[str, BaseAgent], **kwargs):
        super().__init__(**kwargs)
        self.workers = workers
    
    def delegate(self, task: str) -> str:
        """分配任务并汇总结果"""
        # 1. 分析任务，决定分配方案
        worker_names = ", ".join(self.workers.keys())
        delegation_prompt = f"""分析以下任务，决定分配给哪个工人处理。

可用工人：
{worker_names}

每个工人的角色：
{chr(10).join(f'- {name}: {worker.role}' for name, worker in self.workers.items())}

任务：{task}

输出 JSON 格式：
{{"assignments": [{{"worker": "工人名", "subtask": "子任务描述"}}]}}
"""
        self.message_history.append({"role": "user", "content": delegation_prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.message_history,
            temperature=0,
            stream=False
        )
        
        content = response.choices[0].message.content.strip()
        self.message_history.append({"role": "assistant", "content": content})
        
        # 解析分配方案
        try:
            # 清理 markdown
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            plan = json.loads(content)
        except json.JSONDecodeError:
            # 降级：让第一个工人处理
            plan = {"assignments": [{"worker": list(self.workers.keys())[0], "subtask": task}]}
        
        # 2. 执行分配
        results = {}
        for assignment in plan.get("assignments", []):
            worker_name = assignment["worker"]
            subtask = assignment["subtask"]
            
            if worker_name in self.workers:
                print(f"  📋 主管分配任务给 {worker_name}: {subtask}")
                result = self.workers[worker_name].think(subtask)
                results[worker_name] = result
                print(f"  ✅ {worker_name} 完成: {result[:80]}...")
        
        # 3. 汇总结果
        summary_prompt = f"""以下是各个工人的执行结果，请汇总成一个完整的回答：

{json.dumps(results, ensure_ascii=False, indent=2)}

原始任务：{task}"""
        
        final_answer = self.think(summary_prompt)
        return final_answer


# ============================================================
# 5. 流水线模式（Pipeline Pattern）
# ============================================================

class PipelineAgent:
    """
    流水线 Agent
    
    多个 Agent 按顺序处理，每个 Agent 的输出是下一个 Agent 的输入。
    
    示例：研究 Agent → 写作 Agent → 审查 Agent
    """
    
    def __init__(self, agents: list[BaseAgent], verbose: bool = True):
        self.agents = agents
        self.verbose = verbose
    
    def run(self, task: str) -> str:
        """按流水线顺序处理任务"""
        current_input = task
        
        for i, agent in enumerate(self.agents):
            if self.verbose:
                print(f"\n{'='*40}")
                print(f"🔄 流水线阶段 {i+1}: {agent.name} ({agent.role})")
                print(f"{'='*40}")
            
            current_input = agent.think(current_input)
            
            if self.verbose:
                print(f"  输出: {current_input[:150]}...")
        
        return current_input


# ============================================================
# 6. 群聊模式（GroupChat Pattern）
# ============================================================

class GroupChatAgent:
    """
    群聊 Agent
    
    多个 Agent 在一个"聊天室"中讨论，主持人控制发言顺序。
    适合头脑风暴、多角度分析。
    """
    
    def __init__(self, agents: list[BaseAgent], moderator: BaseAgent, max_rounds: int = 3):
        self.agents = agents
        self.moderator = moderator
        self.max_rounds = max_rounds
        self.chat_history: list[str] = []
    
    def discuss(self, topic: str) -> str:
        """群聊讨论"""
        self.chat_history = [f"讨论主题: {topic}"]
        
        for round_num in range(self.max_rounds):
            print(f"\n{'='*40} 第 {round_num+1} 轮讨论 {'='*40}")
            
            # 每个 Agent 发言
            for agent in self.agents:
                # 构建上下文：之前的讨论内容
                context = "\n".join(self.chat_history[-5:])  # 最近5条
                prompt = f"以下是讨论的上下文：\n{context}\n\n请发表你的观点："
                
                opinion = agent.think(prompt)
                self.chat_history.append(f"[{agent.name}]: {opinion}")
                print(f"  💬 {agent.name}: {opinion[:100]}...")
            
            # 主持人总结本轮
            round_summary = self.moderator.think(
                f"以下是本轮讨论内容：\n" + 
                "\n".join(self.chat_history[-len(self.agents):]) +
                "\n\n请总结本轮讨论的要点，指出共识和分歧。"
            )
            self.chat_history.append(f"[主持人总结]: {round_summary}")
            print(f"  📋 主持人总结: {round_summary[:100]}...")
        
        # 主持人最终总结
        final = self.moderator.think(
            f"讨论主题: {topic}\n\n完整讨论记录:\n" + 
            "\n".join(self.chat_history) +
            "\n\n请给出最终结论和建议。"
        )
        
        return final


# ============================================================
# 7. 完整示例：软件开发团队
# ============================================================

def create_dev_team():
    """创建一个模拟的软件开发团队"""
    
    # 产品经理
    pm = BaseAgent(
        name="产品经理",
        role="需求分析和任务拆解",
        system_prompt="""你是一个经验丰富的产品经理。
你的职责是：
1. 分析用户需求
2. 拆解为具体的开发任务
3. 确定优先级
4. 验收最终成果
用中文回答，简洁专业。"""
    )
    
    # 开发者
    dev = BaseAgent(
        name="开发者",
        role="代码实现",
        system_prompt="""你是一个高级 Python 开发者。
你的职责是：
1. 根据需求编写代码
2. 确保代码质量和可读性
3. 添加必要的注释和类型注解
4. 考虑边界情况和错误处理
用中文回答，代码用 Python。"""
    )
    
    # 审查员
    reviewer = BaseAgent(
        name="代码审查员",
        role="代码审查",
        system_prompt="""你是一个严格的代码审查员。
你的职责是：
1. 审查代码的正确性
2. 检查潜在的安全问题
3. 评估代码质量
4. 给出改进建议
用中文回答，指出问题时给出具体建议。"""
    )
    
    return pm, dev, reviewer


# --- 使用流水线模式 ---
# pm, dev, reviewer = create_dev_team()
# pipeline = PipelineAgent([pm, dev, reviewer])
# result = pipeline.run("实现一个 Python 的二分查找函数")

# --- 使用主管模式 ---
# pm, dev, reviewer = create_dev_team()
# supervisor = SupervisorAgent(
#     name="技术主管",
#     role="任务分配和协调",
#     system_prompt="你是一个技术主管，负责分配任务和汇总结果。",
#     workers={"产品经理": pm, "开发者": dev, "审查员": reviewer}
# )
# result = supervisor.delegate("实现一个 Python 的二分查找函数")


# ============================================================
# 8. 完整示例：研究团队
# ============================================================

def create_research_team():
    """创建一个研究团队"""
    
    researcher = BaseAgent(
        name="研究员",
        role="信息搜集和分析",
        system_prompt="你是一个研究员，擅长搜集和分析信息。给出详细、有数据支撑的分析。"
    )
    
    writer = BaseAgent(
        name="撰稿人",
        role="内容撰写",
        system_prompt="你是一个技术撰稿人，擅长将复杂概念用简洁清晰的语言表达。"
    )
    
    fact_checker = BaseAgent(
        name="事实核查员",
        role="事实核查",
        system_prompt="你是一个事实核查员，负责检查内容的准确性和逻辑一致性。指出任何不准确或可疑的表述。"
    )
    
    return researcher, writer, fact_checker


# --- 使用群聊模式 ---
# researcher, writer, fact_checker = create_research_team()
# moderator = BaseAgent(
#     name="主持人",
#     role="讨论主持和总结",
#     system_prompt="你是讨论主持人，负责总结观点、指出共识和分歧。"
# )
# group = GroupChatAgent([researcher, writer, fact_checker], moderator, max_rounds=2)
# result = group.discuss("AI Agent 的未来发展方向是什么？")


# ============================================================
# 💡 练习
# ============================================================
"""
练习1：实现一个"代码开发流水线"：
       需求分析 → 架构设计 → 编码 → 测试 → 审查
       每个阶段由不同的 Agent 负责。

练习2：实现"辩论模式"：
       - 两个 Agent 分别代表正方和反方
       - 每轮各发表观点并反驳对方
       - 主持人总结并判定胜负
       主题示例："Python 是否适合大型项目？"

练习3：实现"层级式多 Agent"：
       - 总经理 → 部门经理 → 执行员工
       - 任务从上到下分解，结果从下到上汇总
       - 每层可以有自己的决策逻辑

练习4（进阶）：实现一个"自适应团队"：
       - 根据任务类型自动选择协作模式
       - 简单任务 → 单 Agent
       - 需要多角度 → 群聊
       - 有明确步骤 → 流水线
       - 需要分配 → 主管模式
"""
