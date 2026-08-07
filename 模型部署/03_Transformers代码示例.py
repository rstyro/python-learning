"""
03 · Transformers 可运行代码示例
=================================

配套文档：02_HuggingFace与Transformers.md

本文件演示 transformers 部署的完整流程：
1. 环境检查（CUDA / 显存）
2. 加载模型（自动下载）
3. 基础推理
4. 流式输出
5. 4bit 量化加载
6. 完整对话封装

⚠️ 运行前：
- pip install transformers accelerate bitsandbytes safetensors sentencepiece
- 建议先设置镜像：$env:HF_ENDPOINT = "https://hf-mirror.com"
- 第一次运行会自动下载模型（数 GB），请耐心等待
- 默认用 qwen2.5-1.5b 小模型（下载快、CPU 也能跑）
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ============================================================
# 0. 环境检查
# ============================================================
print("=" * 60)
print("环境检查")
print("=" * 60)
print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"显存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")

# 模型选择：1.5B 是 CPU/小显存都能跑的平衡点
# 想体验更好的效果可换成 3b 或 7b（7b 需要 8GB+ 显存或量化）
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
print(f"\n将加载模型: {MODEL_NAME}")

# ============================================================
# 1. 加载分词器和模型
# ============================================================
print("\n加载模型（第一次会自动下载，请耐心）...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto",
)

print(f"✅ 模型加载完成，设备: {model.device}")


# ============================================================
# 2. 封装对话推理函数
# ============================================================
def chat(prompt: str, max_new_tokens: int = 512, temperature: float = 0.7) -> str:
    """
    单轮对话推理

    Args:
        prompt: 用户输入
        max_new_tokens: 最大生成 token 数
        temperature: 采样温度（0.7 适度创造性，0 为确定性）

    Returns:
        模型回答
    """
    # 使用 chat 模板格式化（Qwen 特有，自动加 <|im_start|> 等标记）
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    # 分词 → 转 tensor → 放到模型所在设备
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    # 推理
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0,       # 温度>0 用采样
            temperature=temperature if temperature > 0 else 1.0,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
        )

    # 只取新生成的部分（去掉输入的 prompt token）
    new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True)


# ============================================================
# 3. 基础推理测试
# ============================================================
print("\n" + "=" * 60)
print("测试1：基础推理")
print("=" * 60)
answer = chat("用一句话介绍什么是 Python 装饰器")
print(f"\n用户: 用一句话介绍什么是 Python 装饰器")
print(f"AI: {answer}")


# ============================================================
# 4. 流式输出（TextStreamer）
# ============================================================
print("\n" + "=" * 60)
print("测试2：流式输出（打字机效果）")
print("=" * 60)
from transformers import TextStreamer

streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

def chat_stream(prompt: str, max_new_tokens: int = 200):
    """流式对话"""
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.7,
        streamer=streamer,          # 开启流式
        pad_token_id=tokenizer.eos_token_id,
    )

print(f"用户: 写一首五言绝句")
chat_stream("写一首五言绝句")


# ============================================================
# 5. 4bit 量化加载（省显存，需 bitsandbytes）
# ============================================================
"""
如需用 4bit 量化加载（显存需求降低 75%）：

from transformers import BitsAndBytesConfig

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct",     # 7B 模型量化后约 3.5GB
    quantization_config=quant_config,
    device_map="auto",
)

⚠️ bitsandbytes 在 Windows 上可能不支持，此时建议用 GGUF（见 05 篇）
   或直接使用 Ollama 的量化推理（见 01 篇）
"""


# ============================================================
# 6. 多轮对话（维护消息历史）
# ============================================================
print("\n" + "=" * 60)
print("测试3：多轮对话")
print("=" * 60)

def chat_with_history(messages: list[dict], max_new_tokens: int = 512) -> str:
    """带历史的多轮对话"""
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id,
        )
    new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True)

history = [
    {"role": "system", "content": "你是一个 Python 导师，回答简洁。"},
    {"role": "user", "content": "Python 的列表和元组有什么区别？"},
]
r1 = chat_with_history(history)
print(f"AI第1轮: {r1[:120]}...")

# 把历史补上，继续问（模型能记住上下文）
history.append({"role": "assistant", "content": r1})
history.append({"role": "user", "content": "那元组可以修改吗？"})
r2 = chat_with_history(history)
print(f"AI第2轮: {r2[:120]}...")


# ============================================================
# 7. 保存模型到本地（下次加载秒开）
# ============================================================
"""
# 保存
model.save_pretrained("./saved_model")
tokenizer.save_pretrained("./saved_model")

# 之后直接本地加载（不再联网下载）
model = AutoModelForCausalLM.from_pretrained("./saved_model", device_map="auto")
"""


# ============================================================
# 8. 错误处理示例
# ============================================================
"""
以下展示加载和推理时的常见错误处理模式：
"""

def safe_load_model(model_name: str):
    """安全加载模型，带错误处理"""
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
        )
        return model, tokenizer
    except OSError as e:
        if "trust_remote_code" in str(e):
            print("⚠️ 此模型需要 trust_remote_code=True，请确认来源可信后添加该参数")
        elif "not a valid" in str(e):
            print("⚠️ 模型名格式错误，请使用 组织名/模型名 格式（如 Qwen/Qwen2.5-1.5B-Instruct）")
        else:
            print(f"⚠️ 模型加载失败，可能是网络问题：{e}")
            print("提示：设置镜像 $env:HF_ENDPOINT='https://hf-mirror.com' 后重试")
        raise
    except torch.cuda.OutOfMemoryError:
        print("⚠️ 显存不足！建议：")
        print("  1. 换更小模型（1.5B/3B）")
        print("  2. 开启 4bit 量化（见第5节）")
        print("  3. 减小 max_new_tokens 或上下文长度")
        raise
    except Exception as e:
        print(f"⚠️ 未知错误：{type(e).__name__}: {e}")
        raise


def safe_generate(model, tokenizer, prompt: str, **kwargs) -> str:
    """安全推理，带错误处理"""
    try:
        messages = [{"role": "user", "content": prompt}]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(text, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(**inputs, pad_token_id=tokenizer.eos_token_id, **kwargs)
        
        new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
        return tokenizer.decode(new_tokens, skip_special_tokens=True)
    
    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()
        return "[错误] 显存不足，请减小 max_new_tokens 或使用更小模型"
    except RuntimeError as e:
        if "CUDA" in str(e):
            torch.cuda.empty_cache()
        return f"[错误] 推理失败：{e}"
    except Exception as e:
        return f"[错误] 未知错误：{type(e).__name__}: {e}"


# 使用示例
print("\n" + "=" * 60)
print("测试4：错误处理演示")
print("=" * 60)
result = safe_generate(model, tokenizer, "你好", max_new_tokens=100, do_sample=True, temperature=0.7)
print(f"AI: {result}")


# ============================================================
# 💡 练习
# ============================================================
"""
练习1：把 MODEL_NAME 换成 "Qwen/Qwen2.5-3B-Instruct"，对比回答质量
       和 1.5B 的差异。

练习2：实现一个 temperature=0 的确定性模式，用于 Agent 的工具决策
       （思考：为什么 Agent 决策需要确定性？）

练习3：用 snapshot_download 提前下载模型到本地目录，
       然后从本地路径加载（离线部署）。

练习4：封装一个 ReAct 风格的 Agent：
       - 让模型输出 JSON 格式的工具调用决策
       - 解析 JSON，执行工具，把结果反馈给模型
       - 循环直到模型直接回答（参考 AI/3_agent_patterns）
"""
