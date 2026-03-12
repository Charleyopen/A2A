# 更新说明 (Changelog)

## [2025-03-09] 讨论组 + 网页版

### 新增

- **讨论组系统**
  - **讨论组一**：乔布斯、伊隆·马斯克、张一鸣（总结：张一鸣）
  - **讨论组二**：沃伦·巴菲特、特朗普、比尔·盖茨（总结：比尔·盖茨）
  - 每人独立 system prompt，基于真实公开言论与性格

- **网页版 (Flask)**
  - 首页输入主题、下拉选择讨论组、一键开始讨论
  - 实时展示对话与总结
  - 右侧讨论历史列表，点击可查看任意一次完整记录（含讨论组标识）

- **API**
  - `GET /api/groups`：获取所有讨论组列表
  - `POST /api/run`：提交 `topic` + `group_id` 运行讨论
  - `GET /api/history`：讨论历史列表
  - `GET /api/history/<filename>`：单条历史详情

### 变更

- **命令行 (main.py)**：启动时提示选择讨论组（1 或 2），再输入主题
- **dialogue.py**：重构为 `GROUPS` 配置 + `run_dialogue(topic, group_id)`，支持多组
- **输出 JSON**：增加 `group_id`、`group_name`、`personas`，便于前端区分讨论组
- **README**：补充两组说明及命令行/网页选择方式

### 技术

- 依赖：Flask、智谱 API（见 `requirements.txt`）
- 运行网页：`python3 app.py`，默认端口 5001
