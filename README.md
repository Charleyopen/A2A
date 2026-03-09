# Face2Face — Agent 对 Agent 对话系统

双大模型围绕一个主题进行 4 轮对话，最后由第二 Agent 生成记录与总结。

## 流程

1. **你**：输入一个讨论主题  
2. **第 1 轮**：第一个大模型（Agent A）就主题发表观点  
3. **第 2 轮**：第二个大模型（Agent B）针对 A 的观点继续讨论  
4. **第 3 轮**：Agent A 回复 Agent B 的评论  
5. **第 4 轮**：Agent B 再次回复  
6. **总结**：Agent B 根据完整对话生成「记录与总结」

## 环境与依赖

- Python 3.10+
- 依赖：`pip install -r requirements.txt`

## 配置

使用**智慧大模型（智谱 AI）**接口。首次使用请复制 `config.example.py` 为 `config.py` 并填入 API Key，或通过环境变量设置：

```bash
export ZHIPU_API_KEY="你的API_KEY"
```

## 运行

```bash
cd Face2Face
pip install -r requirements.txt
python3 main.py
```

按提示输入主题后，程序会依次输出每轮对话和最终总结，并将完整结果（含 `turns` 与 `summary`）保存到 `outputs/主题名.json`。
