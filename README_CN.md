# Agently Skills

面向 coding agents 的 Agently 官方可安装 Skills 仓库。

主仓库：<https://github.com/AgentEra/Agently>  
官方文档：<https://agently.tech/docs/en/> | <https://agently.cn/docs/>

## 什么是 Agently？

Agently 是一个用于构建模型应用和工作流的框架。

它提供的原生能力面包括：

- 模型接入和 provider settings
- Prompt 组合与 prompt config
- 结构化输出与 required keys 约束
- 响应复用、metadata 读取与 streaming 消费
- tools、MCP、memory、knowledge-base 等扩展能力
- 基于 TriggerFlow 的工作流编排

## 什么是 Agently-Skills？

Agently-Skills 是面向 coding agents 的 Agently 官方 Skills 套件。

它解决的不只是 API 用法说明，还包括：

- 如何从自然语言产品诉求里识别出适合 Agently 的场景
- 如何选择正确的 skill 或 skill 组合
- 如何按 Agently 原生能力边界来组织项目
- 如何落地最佳实践目录结构、编排方案和性能优化重构
- 如何让 coding agent 避免泛泛地拼接局部能力，而是写出符合 Agently 设计哲学的完整项目

目标不是让 coding agent 只会生成零散代码片段，而是让它能写出真正符合 Agently 设计范式的项目。

例如，像 `基于本地 Ollama 服务做一个旅行计划梳理工具` 这种没有明确技术约束的自然语言请求，不应该只被理解成“一次本地模型调用”。官方 Skills 会帮助 coding agent 进一步判断模型接入方式、Prompt 组织方式、工作流形态和项目结构。

## 为什么要用官方 Skills？

- 它更擅长捕获宽泛、没有明确约束的模型应用开发诉求。
- 它沉淀的是 Agently 原生最佳实践，而不是泛用框架式的局部技巧。
- 它不仅覆盖功能调用，还覆盖目录规划、设计哲学、性能优化和编排重构。
- 它会针对真实场景表达做校验，而不是只靠少量手写示例。

## 路由心智模型

选 skill 时，先按这个顺序想：

- 如果用户请求从业务目标、产品行为、重构诉求，或者一个“还没定 owner layer”的问题出发，先走 `agently-playbook`
- 如果用户请求已经足够具体，直接命中拥有该能力面的 leaf skill
- 优先使用 Agently 原生能力，不要先发明自定义 parser、retry loop、状态机、事件总线或 orchestration 外壳

最重要的路由规则如下：

- 未定层级的产品、助手、自动化、工作流、项目重构请求 -> `agently-playbook`
- 模型接入、env vars、模型配置分离 -> `agently-model-setup`
- Prompt 结构、prompt config、YAML 化 prompt 行为、配置文件桥接 -> `agently-prompt-management`
- 稳定结构化输出、required keys、机器可消费结果 -> `agently-output-control`
- 一个响应结果需要被文本、数据、metadata、stream 多次消费 -> `agently-model-response`
- session 连续性与 restore-after-restart -> `agently-session-memory`
- tools、MCP、FastAPIHelper、`auto_func`、`KeyWaiter` -> `agently-agent-extensions`
- embeddings、索引、检索、KB-to-answer -> `agently-knowledge-base`
- 显式工作流编排、TriggerFlow、混合同异步执行、事件驱动 fan-out、流程清晰化重构、可恢复多阶段流程 -> `agently-triggerflow`
- LangChain / LangGraph 迁移 -> `agently-migration-playbook`，再进入对应迁移 leaf

## 标准项目形态

当一个 Agently 项目需要保持可维护性时，初始化或重构都应该围绕明确的能力边界来做，而不是把所有东西继续塞进一个巨大的 `app.py`。

默认建议拆成这些层：

- `SETTINGS.yaml` 或独立 settings 层，负责 provider 配置、`${ENV.xxx}` 占位、workflow/search/browse 参数和其他部署期开关
- app / integration 层，负责加载 settings、按需校验必需环境变量、调用 `Agently.set_settings(..., auto_load_env=True)`，并完成 tools 与主流程的装配
- `prompts/`，负责 YAML / JSON Prompt contract，承载 `input`、`info`、`instruct`、`output`
- `workflow/`，负责 TriggerFlow 图和 chunk 实现
- `tools/`，负责可替换的 search、browse、MCP 或其他外部适配层
- `outputs/` 和 `logs/`，负责运行产物，而不是把这些内容混进源码目录

这里有两个需要明确写进规范的源码级细节：

- Configure Prompt 支持对 prompt 的 key 和 value 做递归 placeholder 注入。像 `${topic}`、`${language}`、`${column_title}` 这类变量，应保留在 prompt 文件里，再通过 `load_yaml_prompt(..., mappings={...})` 或 `load_json_prompt(...)` 注入。
- 模型配置可以直接保留 `${ENV.NAME}` 占位，并让 `Agently.set_settings(..., auto_load_env=True)` 在运行时自动查找并加载本地 `.env` 后完成替换。

`Agently-Daily-News-Collector` 用的就是这个模式：settings 留在 `SETTINGS.yaml`，prompt contract 留在 `prompts/`，流程构造留在 `workflow/`，而 app 层负责 `.env` 加载和 Agently wiring。

项目初始化不建议拆成单独的 public skill。它应该属于 `agently-playbook` 的重要执行步骤：先决定 owner layers 和 skeleton，再把具体实现分发给对应 leaf skills。

更完整的公开规范可以看 [`skills/agently-playbook/references/project-framework.md`](skills/agently-playbook/references/project-framework.md)。

## 公开 Catalog

当前公开 catalog 一共 12 个 skills。

### 入口

- `agently-playbook`
  未定层级的模型应用、助手、内部工具、自动化、评估器、工作流、项目结构重构请求的统一入口。

### Request Side

- `agently-model-setup`
  模型连接、dotenv 配置、传输层设置，以及基于 settings 文件的模型配置分离。
- `agently-prompt-management`
  Prompt 组合、prompt config、YAML 化 prompt 行为、mappings 与可复用请求侧 prompt 结构。
- `agently-output-control`
  输出 schema、字段顺序、required keys 与结构化输出可靠性。
- `agently-model-response`
  `get_response()`、结果复用、metadata、streaming 消费与响应生命周期。
- `agently-session-memory`
  Session 连续性、memo、restore 与请求侧会话状态。

### Request Extensions

- `agently-agent-extensions`
  tools、MCP、FastAPIHelper、`auto_func` 与 `KeyWaiter`。
- `agently-knowledge-base`
  embeddings、Chroma 索引、检索与 retrieval-to-answer。

### Workflow

- `agently-triggerflow`
  TriggerFlow 编排、运行时状态、runtime stream、工作流内模型执行、事件驱动 fan-out、流程清晰化重构与混合同异步编排。

### Migration

- `agently-migration-playbook`
  LangChain / LangGraph 迁移总入口。
- `agently-langchain-to-agently`
  LangChain agent 侧迁移。
- `agently-langgraph-to-triggerflow`
  LangGraph orchestration 侧迁移。

## 安装

你可以先直接安装整套官方 Skills：

```bash
npx skills add AgentEra/Agently-Skills
```

也可以直接让你的 coding agent 安装 `AgentEra/Agently-Skills`。

如果你想更窄一点地安装，先装 `agently-playbook`：

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
```

`request-core`  
适合明确留在 request side，需要模型接入、prompt 组织、结构化输出和响应复用的场景。

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-model-setup
npx skills add AgentEra/Agently-Skills --skill agently-prompt-management
npx skills add AgentEra/Agently-Skills --skill agently-output-control
npx skills add AgentEra/Agently-Skills --skill agently-model-response
```

`request-extensions`  
适合 request side 还需要 tools、MCP、session continuity 或知识库的场景。

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-agent-extensions
npx skills add AgentEra/Agently-Skills --skill agently-session-memory
npx skills add AgentEra/Agently-Skills --skill agently-knowledge-base
```

`workflow-core`  
适合 owner layer 明确在工作流编排侧，尤其是事件驱动 fan-out、性能重构、可恢复流程、混合同异步执行等场景。

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow
npx skills add AgentEra/Agently-Skills --skill agently-output-control
npx skills add AgentEra/Agently-Skills --skill agently-model-response
npx skills add AgentEra/Agently-Skills --skill agently-session-memory
```

`migration`  
适合明确要把已有 LangChain 或 LangGraph 系统迁移到 Agently 的场景。

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-migration-playbook
npx skills add AgentEra/Agently-Skills --skill agently-langchain-to-agently
npx skills add AgentEra/Agently-Skills --skill agently-langgraph-to-triggerflow
```
