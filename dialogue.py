"""
Agent 对 Agent 对话系统：双大模型轮流讨论，共 4 轮对话，最后由第二 Agent 生成记录与总结。
"""
from llm_client import chat

# 第一个大模型：负责开场回答与对第二 Agent 的回复
SYSTEM_AGENT_A = """你是讨论中的「正方」Agent。请根据当前话题或对方观点，给出清晰、有深度的回答或反驳。
保持专业、有条理，每次回复控制在合理长度内。"""

# 第二个大模型：负责接续讨论与对第一 Agent 的回复，并在最后生成记录与总结
SYSTEM_AGENT_B = """你是讨论中的「反方」Agent。请针对当前话题或对方观点，提出补充、质疑或另一视角。
保持专业、有条理，每次回复控制在合理长度内。在需要时你可以负责整理对话记录并撰写总结。"""


def run_dialogue(topic: str) -> dict:
    """
    执行 4 轮对话：A -> B -> A -> B，最后由 B 生成记录与总结。
    返回包含所有轮次内容和总结的字典。
    """
    history = []  # 用于 API 的 messages 列表
    turns = []    # 用于展示与总结的轮次记录 [{"role": "A"|"B", "content": "..."}, ...]

    # 初始系统提示：给出主题
    prompt_topic = f"请就以下主题发表你的观点或开场白，开启讨论。主题：{topic}"

    # ---------- 第 1 次：第一个大模型回答 ----------
    messages_a1 = [
        {"role": "system", "content": SYSTEM_AGENT_A},
        {"role": "user", "content": prompt_topic},
    ]
    reply_a1 = chat(messages_a1)
    history.extend([
        {"role": "user", "content": prompt_topic},
        {"role": "assistant", "content": reply_a1},
    ])
    turns.append({"role": "Agent A", "content": reply_a1})
    print(f"\n【Agent A - 第1轮】\n{reply_a1}\n")

    # ---------- 第 2 次：第二个大模型接着讨论 ----------
    messages_b1 = [
        {"role": "system", "content": SYSTEM_AGENT_B},
        {"role": "user", "content": f"讨论主题：{topic}\n\n对方（Agent A）的观点：\n{reply_a1}\n\n请针对上述观点继续讨论，提出你的看法或补充。"},
    ]
    reply_b1 = chat(messages_b1)
    turns.append({"role": "Agent B", "content": reply_b1})
    print(f"【Agent B - 第2轮】\n{reply_b1}\n")

    # ---------- 第 3 次：第一个大模型回复第二 Agent ----------
    messages_a2 = [
        {"role": "system", "content": SYSTEM_AGENT_A},
        {"role": "user", "content": prompt_topic},
        {"role": "assistant", "content": reply_a1},
        {"role": "user", "content": f"对方（Agent B）的回复：\n{reply_b1}\n\n请针对上述回复继续讨论或反驳。"},
    ]
    reply_a2 = chat(messages_a2)
    turns.append({"role": "Agent A", "content": reply_a2})
    print(f"【Agent A - 第3轮】\n{reply_a2}\n")

    # ---------- 第 4 次：第二个大模型再回复 ----------
    messages_b2 = [
        {"role": "system", "content": SYSTEM_AGENT_B},
        {"role": "user", "content": f"讨论主题：{topic}\n\n对方（Agent A）的观点：\n{reply_a1}\n\n你的上一轮回复：\n{reply_b1}\n\n对方（Agent A）的最新回复：\n{reply_a2}\n\n请针对上述最新回复继续讨论或总结你的立场。"},
    ]
    reply_b2 = chat(messages_b2)
    turns.append({"role": "Agent B", "content": reply_b2})
    print(f"【Agent B - 第4轮】\n{reply_b2}\n")

    # ---------- 最后由第二个大模型生成记录与总结 ----------
    dialogue_text = "\n\n".join(
        f"{t['role']}：\n{t['content']}" for t in turns
    )
    summary_prompt = f"""讨论主题：{topic}

以下是完整对话记录：

{dialogue_text}

请以「第二个 Agent」的身份，为本次讨论撰写一份简洁的「记录与总结」：包括讨论要点、双方主要观点、以及结论或共识（若有）。直接输出总结内容即可。"""

    messages_summary = [
        {"role": "system", "content": SYSTEM_AGENT_B},
        {"role": "user", "content": summary_prompt},
    ]
    summary = chat(messages_summary)
    turns.append({"role": "Agent B（总结）", "content": summary})
    print(f"【Agent B - 记录与总结】\n{summary}\n")

    return {
        "topic": topic,
        "turns": turns,
        "summary": summary,
        "dialogue_text": dialogue_text,
    }
