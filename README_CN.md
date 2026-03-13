# Agently Skills V2

面向 coding agents 的 Agently 官方可安装 Skills。

主仓库：<https://github.com/AgentEra/Agently>  
官方文档：<https://agently.tech/docs/en/> | <https://agently.cn/docs/>

## V2 的核心变化

V2 只保留一个公开路由入口，并按 Agently 原生能力面重构 catalog，同时同时验证“Skill 命中是否正确”和“方案是否真的使用了 Agently 原生能力”。

核心规则：

- 未定层级的产品、助手、工作流请求，一律先走 `agently-playbook`
- 结构化输出优先 `.output(...)` 与 `ensure_keys`
- 一个结果需要多次消费时优先 `get_response()`
- 显式多阶段质量流程和可恢复工作流优先 `TriggerFlow`

## V2 公开 Catalog

- `agently-playbook`
  未定层级请求的总入口。
- `agently-model-setup`
  模型连接、dotenv 配置与 OpenAI-compatible 传输设置。
- `agently-prompt-management`
  Prompt 组合、prompt config、mappings 与可复用 prompt 结构。
- `agently-output-control`
  输出 schema、字段顺序、required keys 与结构化输出可靠性。
- `agently-model-response`
  `get_response()`、结果复用、metadata 与 streaming 消费。
- `agently-session-memory`
  Session 连续性、memo、restore 与会话状态。
- `agently-agent-extensions`
  tools、MCP、FastAPIHelper、`auto_func` 与 `KeyWaiter`。
- `agently-knowledge-base`
  embeddings、Chroma 索引、检索与 retrieval-to-answer。
- `agently-triggerflow`
  TriggerFlow 编排、状态、runtime stream、sub flow、工作流内模型执行、事件驱动 fan-out 与混合同异步编排。
- `agently-migration-playbook`
  LangChain / LangGraph 迁移总入口。
- `agently-langchain-to-agently`
  LangChain agent 侧迁移。
- `agently-langgraph-to-triggerflow`
  LangGraph orchestration 侧迁移。

## 安装

推荐先安装：

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
```

`request-core`

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-model-setup
npx skills add AgentEra/Agently-Skills --skill agently-prompt-management
npx skills add AgentEra/Agently-Skills --skill agently-output-control
npx skills add AgentEra/Agently-Skills --skill agently-model-response
```

`request-extensions`

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-agent-extensions
npx skills add AgentEra/Agently-Skills --skill agently-session-memory
npx skills add AgentEra/Agently-Skills --skill agently-knowledge-base
```

`workflow-core`

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow
npx skills add AgentEra/Agently-Skills --skill agently-output-control
npx skills add AgentEra/Agently-Skills --skill agently-model-response
npx skills add AgentEra/Agently-Skills --skill agently-session-memory
```

`migration`

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-migration-playbook
npx skills add AgentEra/Agently-Skills --skill agently-langchain-to-agently
npx skills add AgentEra/Agently-Skills --skill agently-langgraph-to-triggerflow
```

## 验证

V2 只保留 5 类验证：

- `validate/validate_catalog.py`
- `validate/validate_bundle_manifest.py`
- `validate/validate_trigger_paths.py`
- `validate/validate_native_usage.py`
- `validate/validate_live_scenarios.py`

route fixtures 采用意图驱动检查。每个高价值场景都应该补充接近真实用户表达的自然语言输入，并验证它们是否命中期望的入口 skill 或技能组合。

live 验证会自动寻找 `.env`，并默认使用：

- `DEEPSEEK_BASE_URL`
- `DEEPSEEK_DEFAULT_MODEL`
- `DEEPSEEK_API_KEY`

## 仓库结构

- `skills/`
  V2 公开 skill。
- `validate/`
  共享的 V2 validators 与 fixtures。
- `spec/`
  本地作者工作区，忽略且不发布。
