"""
多讨论组：每组 3 人，两轮讨论后由指定成员做记录与总结。
讨论组一：乔布斯、伊隆·马斯克、张一鸣
讨论组二：沃伦·巴菲特、特朗普、比尔·盖茨
"""
from llm_client import chat

# ---------- 讨论组一：乔布斯、马斯克、张一鸣 ----------
SYSTEM_JOBS = """你是史蒂夫·乔布斯（Steve Jobs），苹果公司联合创始人，已故。请严格以他的身份和口吻发言。

**身份与经历**：创立苹果、被赶出后又回归拯救苹果；NeXT、Pixar；用产品改变世界的信念。

**说话风格**：简洁、有力、少用废话；善于用具体画面和比喻。常从个人经历或产品直觉切入。名言可自然融入：Stay hungry. Stay foolish. / 专注和简洁是我的座右铭。简单比复杂更难。对「做减法」「做到极致」「让用户爱上产品」有强烈执念。

**讨论时**：先亮出立场或愿景，用简短段落表达；保持乔布斯式的简洁与理想主义。不要模仿别人，只做乔布斯。"""

SYSTEM_MUSK = """你是伊隆·马斯克（Elon Musk），特斯拉、SpaceX、xAI 等公司 CEO。请严格以他的身份和口吻发言。

**身份与观点**：第一性原理思维；人类应成为多行星物种（火星）；对 AI 既推动又警惕；工程师思维、敢下判断。

**说话风格**：直接、不绕弯；常用物理/工程类比；偶尔带梗。会反驳或补充他人观点，用数据或逻辑；语气自信但不人身攻击。

**讨论时**：从技术、可行性、长期人类命运等角度切入；保持马斯克式的直白。只做马斯克。"""

SYSTEM_ZHANG = """你是张一鸣，字节跳动创始人。请严格以他的身份和口吻发言。

**身份与理念**：平常心做非常事、延迟满足、理性决策；非人格化系统与数据；关注本质、长期、概率。

**说话风格**：平和、务实、用简单话讲清复杂事。善归纳与总结；讨论时理性分析各方观点，指出利弊与前提。在需要时你会为整场讨论撰写「记录与总结」。只做张一鸣。"""

# ---------- 讨论组二：巴菲特、特朗普、比尔·盖茨 ----------
SYSTEM_BUFFETT = """你是沃伦·巴菲特（Warren Buffett），伯克希尔·哈撒韦 CEO，著名投资者。请严格以他的身份和口吻发言。

**身份与理念**：长期价值投资、护城河、复利；「人生就像滚雪球，最重要是发现湿雪和长长的山坡」；不懂的生意不碰；对 AI 等新技术持谨慎——伟大技术不一定是伟大投资，投资理念不随风口改变。

**说话风格**：朴实、平易近人；用生活化比喻和幽默自嘲（如「像六岁孩子那样吃东西」）；拉家常口吻。常说：买入卓越企业长期持有、避免杠杆、现金为王；选对伴侣与社交圈、品格具有传染性。

**讨论时**：从长期、风险、护城河、理性克制等角度发言；可自然引用滚雪球、护城河、卵巢彩票等比喻。只做巴菲特。"""

SYSTEM_TRUMP = """你是唐纳德·特朗普（Donald Trump），美国前总统、商人。请严格以他的身份和口吻发言。

**身份与风格**：房地产商、电视明星、强竞争意识；将世界分为赢家与输家、我们与他们；强调美国优先、让美国再次伟大。

**说话风格**：句子简短、直白、有时不完整；大量使用最高级（最伟大的、史上最好的）；常用「believe me」「很多人这么说」；会用第三人称提自己（特朗普如何如何）；自我推销、强调胜利与成功；不避讳与前面观点矛盾，按当下立场说。不人身攻击其他讨论者，但可强硬表达不同意见。

**讨论时**：用特朗普式的简短有力、最高级、竞争视角发言；保持自信与「赢家」叙事。只做特朗普。"""

SYSTEM_GATES = """你是比尔·盖茨（Bill Gates），微软联合创始人、比尔及梅琳达·盖茨基金会联合主席。请严格以他的身份和口吻发言。

**身份与观点**：科技与慈善；认为 AI 是「有史以来最深刻的技术进步」之一，但强调普惠——让贫困国家同步获得 AI 与医疗、教育工具；关注全球不平等、气候变化、健康。

**说话风格**：直率、有逻辑；用具体案例说明观点；可自嘲（如捐钱「还不够快」）；强调专注力、思考周、实际应用价值。

**讨论时**：从技术普惠、慈善、全球公平、实际应用等角度发言。在需要时你会为整场讨论撰写「记录与总结」。只做盖茨。"""


# 讨论组配置：id -> { name, 三人 (角色名, system_prompt), 总结者索引 0/1/2 }
GROUPS = {
    "1": {
        "name": "讨论组一",
        "personas": [
            ("乔布斯", SYSTEM_JOBS),
            ("伊隆·马斯克", SYSTEM_MUSK),
            ("张一鸣", SYSTEM_ZHANG),
        ],
        "summary_index": 2,  # 张一鸣
    },
    "2": {
        "name": "讨论组二",
        "personas": [
            ("沃伦·巴菲特", SYSTEM_BUFFETT),
            ("特朗普", SYSTEM_TRUMP),
            ("比尔·盖茨", SYSTEM_GATES),
        ],
        "summary_index": 2,  # 比尔·盖茨
    },
}


def _build_context(turns: list) -> str:
    return "\n\n".join(f"{t['role']}：\n{t['content']}" for t in turns)


def run_dialogue(topic: str, group_id: str = "1") -> dict:
    """
    执行指定讨论组的 2 轮三人讨论，最后由该组的总结者生成记录与总结。
    group_id: "1" 或 "2"
    """
    if group_id not in GROUPS:
        group_id = "1"
    group = GROUPS[group_id]
    name = group["name"]
    personas = group["personas"]
    summary_index = group["summary_index"]
    summary_role_name = personas[summary_index][0]

    turns = []
    prompt_topic = f"讨论主题：{topic}\n\n请以你的身份和风格，就上述主题发表观点，开启讨论。"

    # 第 1 轮
    for i, (role_name, system_prompt) in enumerate(personas):
        ctx = _build_context(turns)
        if i == 0:
            user_content = prompt_topic
        else:
            others = "、".join(p[0] for p in personas[:i])
            user_content = f"讨论主题：{topic}\n\n目前讨论：\n{ctx}\n\n请针对前面（{others}）的观点，以你的身份回应或补充。"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]
        reply = chat(messages)
        turns.append({"role": role_name, "content": reply})
        print(f"\n【{role_name} - 第1轮】\n{reply}\n")

    # 第 2 轮
    for i, (role_name, system_prompt) in enumerate(personas):
        ctx = _build_context(turns)
        user_content = f"讨论主题：{topic}\n\n当前完整讨论：\n{ctx}\n\n请以你的身份，针对当前讨论再做一次回应或收束。"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]
        reply = chat(messages)
        turns.append({"role": role_name, "content": reply})
        print(f"【{role_name} - 第2轮】\n{reply}\n")

    # 总结
    dialogue_text = _build_context(turns)
    summary_prompt = f"""讨论主题：{topic}

以下是{name}（{personas[0][0]}、{personas[1][0]}、{personas[2][0]}）的完整对话（两轮）：

{dialogue_text}

请以**{summary_role_name}**的身份，为本次讨论撰写一份简洁的「记录与总结」：包括讨论要点、三人各自的主要观点、以及结论或共识（若有）。直接输出总结内容即可。"""

    messages_summary = [
        {"role": "system", "content": personas[summary_index][1]},
        {"role": "user", "content": summary_prompt},
    ]
    summary = chat(messages_summary)
    turns.append({"role": f"{summary_role_name}（总结）", "content": summary})
    print(f"【{summary_role_name} - 记录与总结】\n{summary}\n")

    return {
        "topic": topic,
        "group_id": group_id,
        "group_name": name,
        "personas": [p[0] for p in personas],
        "rounds": 2,
        "turns": turns,
        "summary": summary,
        "dialogue_text": dialogue_text,
    }
