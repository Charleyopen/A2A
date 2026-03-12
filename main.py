"""
Face2Face：多讨论组对话系统
选择讨论组，输入主题，进行 2 轮三人讨论并由指定成员总结。
"""
from dialogue import run_dialogue, GROUPS
import json
import os


def main():
    print("=" * 50)
    print("Face2Face — 讨论组")
    print("=" * 50)
    for gid, g in GROUPS.items():
        print(f"  {gid}. {g['name']}：{' / '.join(p[0] for p in g['personas'])}")
    group_id = input("请选择讨论组 (1 或 2，回车默认 1)：").strip() or "1"
    if group_id not in GROUPS:
        group_id = "1"
    print(f"已选：{GROUPS[group_id]['name']}\n")
    topic = input("请输入讨论主题：").strip()
    if not topic:
        topic = "人工智能对教育行业的影响"
        print(f"未输入主题，使用默认：{topic}")
    print(f"\n主题：{topic}\n开始 2 轮讨论…\n")

    result = run_dialogue(topic, group_id=group_id)

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
