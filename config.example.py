# 智慧大模型（智谱 AI）API 配置
# 复制此文件为 config.py 并填入你的 API Key，或使用环境变量 ZHIPU_API_KEY
import os

ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY", "你的智谱API_KEY")
ZHIPU_API_BASE = "https://open.bigmodel.cn/api/paas/v4"
MODEL_NAME = "glm-4-flash"  # 可选: glm-4, glm-4-plus, glm-4-flash 等
