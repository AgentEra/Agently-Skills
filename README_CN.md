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

安装后你能直接获得：

- 从业务需求出发的总入口与路由能力
- 围绕单次模型请求的完整实现能力：模型配置、输入组织、输出控制、工具、MCP、Session、FastAPI、RAG
- 围绕 TriggerFlow 的完整实现能力：编排、模式、状态与资源、子流程、模型集成、中断与流式、配置、执行状态
- LangChain / LangGraph 到 Agently 的迁移 playbook

当前前提版本：

- `Agently >= 4.0.8.5`

## 安装

安装整个仓库：

```bash
npx skills add AgentEra/Agently-Skills
```

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

### 1. 顶层入口

- `agently-playbook`
  从业务目标、系统设计或产品需求出发，决定应该走单次请求、多智能体，还是 TriggerFlow。
- `agently-model-request-playbook`
  从单次模型请求角度出发，决定何时停留在一个请求内，何时升级到工具、MCP、RAG、Session、FastAPI 或 TriggerFlow。
- `agently-triggerflow-playbook`
  从工作流与编排需求出发，决定该使用 TriggerFlow 的哪一组能力。

### 2. 单次模型请求核心

- `agently-model-setup`
  模型连接、`OpenAICompatible`、Provider 切换、认证、代理、超时与 `client_options`
- `agently-input-composition`
  输入组织、prompt slots、mapping、附件、低层 `chat_history`
- `agently-output-control`
  输出结构定义、`ensure_keys`、结果消费、`instant` / `streaming_parse`

### 3. 请求增强能力

- `agently-tools`
- `agently-mcp`
- `agently-session-memo`
- `agently-prompt-config-files`
- `agently-fastapi-helper`
- `agently-embeddings`
- `agently-knowledge-base-and-rag`

### 4. 多智能体与复杂系统

- `agently-multi-agent-patterns`
  面向 planner-worker、parallel experts、reviewer-reviser 等多智能体设计模式。

### 5. TriggerFlow 能力树

- `agently-triggerflow-orchestration`
  基础信号驱动编排
- `agently-triggerflow-patterns`
  常见工作流模式，如 router、fan-out/fan-in、safe loop、ReAct loop、approval gate
- `agently-triggerflow-state-and-resources`
  `runtime_data` / `flow_data` / resources 边界
- `agently-triggerflow-subflows`
  子流程、`capture`、`write_back`
- `agently-triggerflow-model-integration`
  在 flow 中发起模型请求、消费 `delta` / `instant`
- `agently-triggerflow-config`
  工作流定义导出、导入、Mermaid、contract metadata
- `agently-triggerflow-execution-state`
  执行态保存、恢复、继续运行
- `agently-triggerflow-interrupts-and-stream`
  中断、恢复、runtime stream、交互式等待

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
  总入口，先判断应该走 LangChain 迁移还是 LangGraph 迁移
- `agently-langchain-to-agently`
  处理 `create_agent`、structured output、middleware、tools、memory、service exposure 等迁移
- `agently-langgraph-to-triggerflow`
  处理 `StateGraph`、`Send`、`Command`、threads/checkpoints、interrupts、streaming、subgraphs 等迁移

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
