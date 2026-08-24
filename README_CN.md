# Agently Skills

面向 coding agents 的 [Agently](https://github.com/AgentEra/Agently) 官方可安装
Skills 仓库。

文档：[English](https://agently.tech/docs/en/) |
[中文](https://agently.cn/docs/)

## 兼容性

默认分支发布 catalog generation `v3`，对齐 Agently `4.1.4.7` 公开版本，只包含
当前 7-skill catalog。

历史 catalog 冻结在归档分支：

- `v2`：`update/archive-v2-catalog`，最后支持 Agently `4.1.4.7`
- `v1`：`update/archive-legacy-v1-catalog`，最后支持 Agently `4.1.1`

机器可读兼容契约见
[`compatibility/support.json`](compatibility/support.json)。归档分支只用于回滚和
历史检查，不用于新项目安装。

## 当前 Catalog

- `agently` - 当模型应用、助手、内部工具、自动化、评估器或工作流的正确 owner
  layer 尚不明确时，负责入口路由与项目形态判断；低频 TaskDAG 需求也从这里开始。
- `agently-design` - 跨 owner layer 设计和审计复杂系统，覆盖请求、值与事件拓扑、
  证据、身份、生命周期、压力和可观测性。
- `agently-request` - 模型请求、Prompt、结构化输出、响应消费、session memory、
  embeddings 与检索。
- `agently-runtime` - Action Runtime、MCP、ExecutionResource、TaskWorkspace、
  RecordStore、服务适配和可选 DevTools。
- `agently-stage` - 进程内任务生命周期、同步/异步桥接、loop-neutral handle、
  stream、replay channel、事件与背压。
- `agently-triggerflow` - 显式分支、并发、暂停恢复、可重启工作流，以及可检查的
  runtime state 与事件。
- `agently-migration` - 把 LangChain、LangGraph、LlamaIndex、CrewAI 或类似系统
  映射到 Agently 原生 owner layer。

v3 不再提供独立 TaskDAG Skill。TaskDAG 是提交或模型生成的无环图数据所使用的
低频基础能力；先从 `agently` 开始，仅在跨层边界或执行 substrate 需要独立处理时
再加入 `agently-design` 或 `agently-triggerflow`。

## 安装

先选择目标 coding agent，例如：

```bash
export AGENT=codex
```

开发新 Agently 应用时安装 `app` bundle：

```bash
for skill in \
  agently \
  agently-design \
  agently-request \
  agently-runtime \
  agently-stage \
  agently-triggerflow
do
  npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill "$skill" -y
done
```

进行迁移时，先安装 `app` bundle，再补充：

```bash
npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill agently-migration -y
```

只需要最小入口时，仅安装 router：

```bash
npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill agently -y
```

查看当前公开 catalog：

```bash
npx skills add . --list
```
