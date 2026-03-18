"""智谱 AI 大模型 API 客户端（兼容 OpenAI 风格 chat completions）。"""
import requests
import os
from config import ZHIPU_API_KEY, ZHIPU_API_BASE, MODEL_NAME


def chat(messages: list[dict], model: str = MODEL_NAME) -> str:
    """
    调用智谱对话补全 API，返回助手回复文本。
    messages: [{"role": "user"|"assistant"|"system", "content": "..."}, ...]
    """
    url = f"{ZHIPU_API_BASE}/chat/completions"
    headers = {
        "Authorization": f"Bearer {ZHIPU_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.8,
        "max_tokens": 2048,
    }
    # 默认不使用系统代理（避免本机代理导致 403 / 连接失败）。
    # 如需显式启用环境代理，请设置：ZHIPU_USE_ENV_PROXY=1
    use_env_proxy = os.environ.get("ZHIPU_USE_ENV_PROXY", "").strip() in {"1", "true", "True", "YES", "yes"}
    s = requests.Session()
    s.trust_env = bool(use_env_proxy)
    resp = s.post(url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    choice = data.get("choices", [{}])[0]
    return (choice.get("message") or {}).get("content", "").strip()
