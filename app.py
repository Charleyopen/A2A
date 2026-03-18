"""
Face2Face 网页版：可视化三人对话 + 历史记录查看
"""
import json
import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template

from dialogue import run_dialogue, GROUPS

app = Flask(__name__, static_folder="static", template_folder="templates")
OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)


def _safe_filename(topic: str) -> str:
    return "".join(c if c.isalnum() or c in " -_" else "_" for c in topic)[:50]

def _parse_int(value, default: int, min_value: int, max_value: int) -> int:
    try:
        v = int(value)
    except Exception:
        return default
    return max(min_value, min(max_value, v))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/groups", methods=["GET"])
def api_groups():
    """返回所有讨论组列表"""
    items = [
        {"id": gid, "name": g["name"], "personas": [p[0] for p in g["personas"]]}
        for gid, g in GROUPS.items()
    ]
    return jsonify({"ok": True, "groups": items})


@app.route("/api/run", methods=["POST"])
def api_run():
    """运行一次三人对话，保存到 outputs 并返回结果"""
    data = request.get_json() or {}
    topic = (data.get("topic") or "").strip()
    group_id = (data.get("group_id") or "1").strip() or "1"
    if group_id not in GROUPS:
        group_id = "1"
    rounds = _parse_int(data.get("rounds"), default=2, min_value=1, max_value=6)
    mode = (data.get("mode") or "standard").strip().lower()
    if not topic:
        return jsonify({"ok": False, "error": "请填写讨论主题"}), 400
    try:
        result = run_dialogue(topic, group_id=group_id, rounds=rounds, mode=mode)
        safe_name = _safe_filename(topic) or "topic"
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_path = os.path.join(OUTPUTS_DIR, f"{safe_name}__g{group_id}__{ts}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        result["_filename"] = os.path.basename(out_path)
        return jsonify({"ok": True, "result": result})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/history", methods=["GET"])
def api_history():
    """返回历史记录列表：文件名与主题（从 JSON 内读取 topic）"""
    items = []
    for name in sorted(os.listdir(OUTPUTS_DIR), reverse=True):
        if not name.endswith(".json"):
            continue
        path = os.path.join(OUTPUTS_DIR, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            items.append({
                "filename": name,
                "topic": data.get("topic", name.replace(".json", "").replace("_", " ")),
                "group_name": data.get("group_name", ""),
            })
        except Exception:
            items.append({"filename": name, "topic": name})
    return jsonify({"ok": True, "items": items})


@app.route("/api/history/<filename>", methods=["GET"])
def api_history_detail(filename):
    """返回单条历史记录的完整内容"""
    if ".." in filename or "/" in filename:
        return jsonify({"ok": False, "error": "invalid filename"}), 400
    path = os.path.join(OUTPUTS_DIR, filename)
    if not os.path.isfile(path):
        return jsonify({"ok": False, "error": "not found"}), 404
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify({"ok": True, "result": data})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == "__main__":
    # 使用 5001：macOS 上 5000 常被 AirPlay 占用
    app.run(host="0.0.0.0", port=5001, debug=True)
