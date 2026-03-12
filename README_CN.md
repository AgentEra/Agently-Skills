<img width="640" alt="image" src="https://github.com/user-attachments/assets/c645d031-c8b0-4dba-a515-9d7a4b0a6881" />

# Agently Skills 🚀

> **Agently 官方 Skills 仓库，帮助 coding agent 更准确地理解、路由并实现真实世界的 Agently 开发任务。**

[English](https://github.com/AgentEra/Agently-Skills/blob/main/README.md) | [中文](https://github.com/AgentEra/Agently-Skills/blob/main/README_CN.md)

主仓库：<https://github.com/AgentEra/Agently>  
官方文档：<https://agently.tech/docs/en/> | <https://agently.cn/docs/>

---

<p align="center">
  <b>🔥 <a href="#安装">安装</a> | 🧭 <a href="#能力总览">能力总览</a> | 🧩 <a href="#skill-结构">Skill 结构</a> | 🔄 <a href="#迁移与适配">迁移与适配</a></b>
</p>

---

## 官方可安装 Skills

这是 Agently 官方可安装 skills 仓库，用于增强 coding agent 对 Agently 的理解和实现能力。

仓库会公开完整能力树，但运行时更适合按 bundle 大小激活，而不是默认让整棵树同时参与发现。

安装后你能直接获得：

- 从业务需求出发的总入口与路由能力
- 围绕单次模型请求的完整实现能力：模型配置、输入组织、输出控制、工具、MCP、Session、FastAPI、RAG
- 围绕 TriggerFlow 的完整实现能力：编排、模式、状态与资源、子流程、模型集成、中断与流式、配置、执行状态
- LangChain / LangGraph 到 Agently 的迁移 playbook

当前前提版本：

- `Agently >= 4.0.8.5`

## 安装

推荐的激活顺序：

1. 先装一个入口 skill 或一个明确 bundle
2. 只有当问题已经收敛到对应域时，再补相邻 leaf skill
3. 只有在你明确希望整套 catalog 同时共存时，才安装整个仓库

如果当前安装工具还不能直接表达 bundle，可以按下面的安装序列执行。
客户端如果需要做激活控制，请读取公开的 `bundles/manifest.json`，默认只激活一个 bundle 大小的 skill 集合。

### 入口安装

通用 Agently 入口：

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
```

单次请求为主的入口：

```bash
npx skills add AgentEra/Agently-Skills --skill agently-model-request-playbook
```

TriggerFlow 为主的入口：

```bash
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-playbook
```

### Bundle 安装序列

`request-core`：把 active set 收敛在单次请求域内：

```bash
npx skills add AgentEra/Agently-Skills --skill agently-model-request-playbook
npx skills add AgentEra/Agently-Skills --skill agently-model-setup
npx skills add AgentEra/Agently-Skills --skill agently-input-composition
npx skills add AgentEra/Agently-Skills --skill agently-output-control
```

`request-extensions`：先从 `request-core` 开始，再只补你真正需要的扩展 leaf：

- `agently-tools`
- `agently-mcp`
- `agently-session-memo`
- `agently-prompt-config-files`
- `agently-fastapi-helper`
- `agently-embeddings`
- `agently-knowledge-base-and-rag`

`multi-agent`：把 active set 收敛在多智能体架构选择上：

```bash
npx skills add AgentEra/Agently-Skills --skill agently-multi-agent-patterns
```

`triggerflow-core`：把 active set 收敛在 TriggerFlow 工作流域内：

```bash
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-playbook
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-orchestration
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-patterns
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-state-and-resources
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-subflows
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-model-integration
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-config
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-execution-state
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-interrupts-and-stream
```

`migration`：把 active set 收敛在 LangChain / LangGraph 迁移域内：

```bash
npx skills add AgentEra/Agently-Skills --skill agently-langchain-langgraph-migration-playbook
npx skills add AgentEra/Agently-Skills --skill agently-langchain-to-agently
npx skills add AgentEra/Agently-Skills --skill agently-langgraph-to-triggerflow
```

安装整个仓库：

```bash
npx skills add AgentEra/Agently-Skills
```

即使安装了整个仓库，客户端默认也仍然应该按 `bundles/manifest.json` 只激活一个 bundle，而不是直接暴露整个 catalog。

只安装某一颗 skill：

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
```

列出仓库中可安装的 skill：

```bash
npx skills add AgentEra/Agently-Skills -l --full-depth
```

## 核心资源

- 主仓库：<https://github.com/AgentEra/Agently>
- 官方文档（中文）：<https://agently.cn/docs/>
- 官方文档（英文）：<https://agently.tech/docs/en/>
- Skills 仓库：<https://github.com/AgentEra/Agently-Skills>
- 安装命令：`npx skills add AgentEra/Agently-Skills`

## 为什么需要这个仓库？

Agently 的能力边界已经不只是“发一个模型请求”：

- 你可能要做稳定结构化输出
- 你可能要做 `instant` 结构化流式消费
- 你可能要接工具、MCP、知识库、Session
- 你可能要把能力暴露成 FastAPI 服务
- 你可能要进入 TriggerFlow 的复杂编排、并发控制、中断恢复
- 你可能还要从 LangChain / LangGraph 迁移过来

这些能力如果每次都临时解释给 coding agent，成本会很高，且容易不一致。  
这个仓库的作用，就是把这些高频知识组织成可安装、可触发、可路由的 skills。

## 能力总览

下面这些分组描述的是公开 catalog。真正推荐的运行时激活集合，以前面的 entry installs、bundle install sequences，以及公开的 `bundles/manifest.json` 为准。

### 1. 顶层入口

- `agently-playbook`
  从业务目标、系统设计或产品需求出发，决定应该走单次请求、多智能体，还是 TriggerFlow。
- `agently-model-request-playbook`
  从单次模型请求角度出发，决定何时停留在一个请求内，何时升级到工具、MCP、RAG、Session、FastAPI 或 TriggerFlow。
- `agently-triggerflow-playbook`
  从工作流与编排需求出发，决定该使用 TriggerFlow 的哪一组能力。

### 2. 单次模型请求核心

- `agently-model-setup`
  直接模型连接与请求传输配置：`OpenAICompatible`、认证、地址、代理、超时、`request_options` 与最小验证
- `agently-input-composition`
  直接输入侧 prompt 组织：prompt slots、prompt 分层、mapping、附件、低层 `chat_history`
- `agently-output-control`
  直接输出侧结构、重试、结果消费与 `instant` / `streaming_parse` 结构化流式处理

### 3. 请求增强能力

- `agently-tools`
  直接本地与内建工具注册，以及请求期 tool loop 控制
- `agently-mcp`
  直接把 MCP Server 注册为 Agently 工具，处理 transport 与 schema 映射
- `agently-session-memo`
  Session 驱动的会话连续性、memo、裁剪、序列化与恢复
- `agently-prompt-config-files`
  直接 YAML/JSON prompt 模板配置、mapping、`.alias` 与 roundtrip 导出
- `agently-fastapi-helper`
  通过 `FastAPIHelper` 直接暴露 HTTP、SSE 与 WebSocket
- `agently-embeddings`
  直接 embeddings 请求配置、批处理、向量消费与 embedding-agent handoff
- `agently-knowledge-base-and-rag`
  直接基于 Chroma 的知识库索引、检索与 retrieval-to-answer 流程

### 4. 多智能体与复杂系统

- `agently-multi-agent-patterns`
  在已确定需要多智能体后，选择 pattern 与 handoff contract 的设计层技能。

### 5. TriggerFlow 能力树

- `agently-triggerflow-orchestration`
  底层 TriggerFlow 原语、执行入口、contract 与结果语义
- `agently-triggerflow-patterns`
  可复用工作流形态，如 router、fan-out/fan-in、safe loop、ReAct loop、approval gate
- `agently-triggerflow-state-and-resources`
  状态放置与运行时资源边界，如 `runtime_data` / `flow_data` / `data.set_resource(...)`
- `agently-triggerflow-subflows`
  显式子流程边界：`to_sub_flow(...)`、`capture`、`write_back`
- `agently-triggerflow-model-integration`
  在 flow 中执行模型请求，包括 request 创建、并发控制、`delta` / `instant`
- `agently-triggerflow-config`
  TriggerFlow 定义导出、导入、blueprint copy、Mermaid 与 contract metadata
- `agently-triggerflow-execution-state`
  运行中 execution 的保存、恢复、继续运行与 runtime resource reinjection
- `agently-triggerflow-interrupts-and-stream`
  等待、恢复、runtime stream 生命周期与实时交互

## Skill 结构

仓库中的公开 skill 只放在 `skills/` 下。每颗 skill 至少包含：

- `SKILL.md`
- `references/`

典型结构如下：

```text
skills/
  agently-playbook/
    SKILL.md
    references/
  agently-model-request-playbook/
    SKILL.md
    references/
  agently-model-setup/
    SKILL.md
    references/
    scripts/
  ...
```

`spec/` 目录只服务于本仓库内部撰写、验证与增量维护，不属于公开 skill payload。

## 迁移与适配

如果你的系统原来基于 LangChain 或 LangGraph，可以直接从迁移 skills 开始：

- `agently-langchain-langgraph-migration-playbook`
  只在迁移入口还未收敛时使用，先判断应该走 LangChain 迁移还是 LangGraph 迁移
- `agently-langchain-to-agently`
  作为 LangChain agent 侧的 direct migration leaf，处理 `create_agent`、structured output、middleware、tools、memory、service exposure 等迁移
- `agently-langgraph-to-triggerflow`
  作为 LangGraph orchestration 侧的 direct migration leaf，处理 `StateGraph`、`Send`、`Command`、threads/checkpoints、interrupts、streaming、subgraphs 等迁移

这些迁移 skill 的目标不是做“逐行替换”，而是把原有能力翻译并重组到 Agently 当前的能力树上。

## 推荐阅读顺序

如果你是第一次接触这个仓库，建议按这个顺序看：

1. `agently-playbook`
2. `agently-model-request-playbook`
3. `agently-model-setup`
4. `agently-input-composition`
5. `agently-output-control`
6. 再根据实际需求进入 tools / MCP / session / FastAPI / RAG
7. 当问题变成多步、异步、可恢复流程时，再进入 `agently-triggerflow-playbook`

## 发布状态

当前仓库已经完成：

- 全量 `skills-ref validate`
- 全量 author-side validator
- 远程 `npx skills add AgentEra/Agently-Skills` 发现与安装烟测

如果你在使用中发现某颗 skill 的边界、命中或路由不够准确，欢迎直接提 issue 或 PR。

## 框架能力反馈

如果实际使用中发现问题不只是 skill 路由或文档表达，而是 Agently 框架能力本身不足，可以直接通过反馈 API 提交脱敏后的能力反馈。

适用场景包括：

- 当前行为与合理预期不符
- 你认为该场景下框架本应支持，但目前没有支持
- 已经进入明确实现路径后，仍然因为框架能力限制而效果明显不达预期

反馈接口：

- `POST https://api.agently.cn/feedback/api/feedbacks`

Body 样例：

```json
{
  "who_are_you": "Acme team PM",
  "request_context": "Building an internal workflow tool",
  "agently_issue": "Unclear how to combine TriggerFlow with existing FastAPI routes",
  "expected_support": "Need example code and better documentation"
}
```

注意：

- 提交前务必做脱敏
- 不要携带密钥、token、内部 URL、客户数据或其他敏感信息

为了让反馈更可处理，建议在脱敏后至少提供以下一种信息：

- 你实际使用 Agently 的代码
- 你认为有问题的框架代码文件路径与行号
- 能复现问题或体现预期落差的最小代码块
