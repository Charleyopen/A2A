"""
Face2Face：Agent 对 Agent 对话系统
输入一个主题，由两个大模型进行 4 轮对话，最后由第二 Agent 生成记录与总结。
"""
from dialogue import run_dialogue
import json
import os


def main():
    print("=" * 50)
    print("Face2Face — Agent 对 Agent 对话系统")
    print("=" * 50)
    topic = input("请输入讨论主题：").strip()
    if not topic:
        topic = "人工智能对教育行业的影响"
        print(f"未输入主题，使用默认：{topic}")
    print(f"\n主题：{topic}\n开始 4 轮对话…\n")

    result = run_dialogue(topic)

    # 可选：将结果写入文件
    out_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(out_dir, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in " -_" else "_" for c in topic)[:50]
    out_path = os.path.join(out_dir, f"{safe_name}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"对话与总结已保存到：{out_path}")


if __name__ == "__main__":
    main()
