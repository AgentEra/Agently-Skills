# Agently Skills

面向 coding agents 的 Agently 官方可安装 Skills 仓库。

主仓库：<https://github.com/AgentEra/Agently>  
官方文档：<https://agently.tech/docs/en/> | <https://agently.cn/docs/>

## 兼容性

默认公开 catalog 是当前 Agently-Skills generation `v2`，已为 Agently 4.1.4.5
开发线和新的 7-skill 结构完成准备。

机器可读兼容声明位于 `compatibility/support.json`。默认分支只保留当前公开
catalog，避免 coding-agent 的 Skill 检索命中已退役的历史 Skills。

历史 catalog generation 通过专门的归档分支保留，而不是放在默认分支文件树里。
冻结的 V1 catalog 已归档在 `update/archive-legacy-v1-catalog`，最后支持 Agently
`4.1.1`。

## 什么是 Agently？

Agently 是一个用于构建模型应用和工作流的框架。它提供模型请求、provider
settings、Prompt 组合、结构化输出、Action Runtime、MCP、knowledge-base flow、
TriggerFlow 编排、Dynamic Task DAG 执行等原生能力面。

## 什么是 Agently-Skills？

Agently-Skills 是面向 coding agents 的 Agently 官方 Skills 套件。

它和 Agently 框架运行时里的 `SkillLibrary`、`TaskContext` 以及
AgentExecution Skill 路径不是一回事：

- `Agently-Skills` - 给 Codex、Claude Code 等 coding agent 用的指导型 skill 包
- Agently `SkillLibrary` - 不可变 Skill revision 的安装与存储边界；
  `TaskContext` 与 `ContextReader` 提供任务级上下文，AgentExecution 负责
  Skill 绑定、路由选择与执行生命周期

单个 skill 目录是标准 `SKILL.md` 包，可按需带 references、examples、outputs 和
scripts。详细 API 指导应放在这些 skill 包和一层 reference 文件里，不应堆在仓库
README 中。

## 当前 Catalog

默认 catalog 一共 7 个公开 skills：

- `agently` - 未定层级的模型应用、助手、内部工具、自动化、评估器、工作流、
  项目结构重构请求的统一入口。
- `agently-design` - 跨请求、runtime、工作流与证据边界的系统设计、评审、优化和
  请求链审计，覆盖 ModelRequest 契约、身份与证据、生命周期、压力和可观测性。
- `agently-request` - 请求侧模型接入、provider settings、Prompt 管理、结构化
  输出、响应复用、streaming 消费、session memory、embeddings、knowledge-base
  索引、检索与 retrieval-backed answers。
- `agently-runtime` - Action Runtime、内置 action packages、tool 兼容入口、
  MCP、ExecutionResource 生命周期、服务暴露、auto-function helpers、
  以及 `KeyWaiter`。
- `agently-dynamic-task` - Dynamic Task DAG 规划、`TaskDAG` 校验、resolver
  handlers，以及通过 `Agently.create_dynamic_task(...)` 使用 `TaskDAGExecutor`
  执行。
- `agently-triggerflow` - 显式工作流编排、分支、并发、审批、等待和恢复、
  runtime stream、可重启执行、混合同异步函数或模块编排，以及便于图调试的
  工作流定义。
- `agently-migration` - 从 LangChain、LangGraph、LlamaIndex、CrewAI 或类似系统
  迁移到 Agently 原生 request/runtime 或 TriggerFlow 层。

默认检索面应使用当前 `skills/` 目录。不要把归档 catalog 分支、历史目录或已退役
Skill 文件夹加入 coding agent 的常规搜索路径。

## 安装

先明确目标 agent。推荐把一个 bundle 安装到一个 agent 对应的 skills 目录里，例如
Codex：

```bash
export AGENT=codex
```

如果目标是 Claude、Cursor 或其他受支持 agent，把 `AGENT` 换成对应名称。

`app`
开发新 Agently 应用的默认 bundle：

```bash
for skill in \
  agently \
  agently-design \
  agently-request \
  agently-runtime \
  agently-dynamic-task \
  agently-triggerflow
do
  npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill "$skill" -y
done
```

`migration`
从 LangChain、LangGraph、LlamaIndex、CrewAI 或类似系统迁移到 Agently 的 bundle。
先安装 `app` bundle，再补充迁移 skill：

```bash
npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill agently-migration -y
```

如果只想最小化安装入口 router：

```bash
npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill agently -y
```

查看默认公开 catalog：

```bash
npx skills add . --list
```

默认列表和常规安装路径只暴露当前 7-skill catalog。
