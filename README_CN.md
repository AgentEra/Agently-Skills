# Agently Skills

面向 coding agents 的 [Agently](https://github.com/AgentEra/Agently) 官方可安装
Skills 仓库。

文档：[English](https://agently.tech/docs/en/) |
[中文](https://agently.cn/docs/)

## 兼容性

当前 catalog 为 generation `v3`，对齐 Agently `4.1.4.10`，包含八个正式 Skill 和一个弃用转接入口；产品设计 Skill 不依赖 Agently 运行时。

历史 catalog 冻结在归档分支：

- `v2`：`update/archive-v2-catalog`，最后支持 Agently `4.1.4.7`
- `v1`：`update/archive-legacy-v1-catalog`，最后支持 Agently `4.1.1`

机器可读兼容契约见
[`compatibility/support.json`](compatibility/support.json)。归档分支只用于回滚和
历史检查，不用于新项目安装。

## 当前 Catalog

- `agently` - 当模型应用、助手、内部工具、自动化、评估器或工作流的正确 owner
  layer 尚不明确时，负责入口路由与项目形态判断；低频 TaskDAG 需求也从这里开始。
- `agently-agentic-design` - 跨 owner layer 设计和审计复杂系统，覆盖请求、值与事件拓扑、
  证据、身份、生命周期、压力和可观测性。
- `agently-product-design` - 应用设计方法：方案、角色行为覆盖、应用体验与文档表达，按需加载四个内部模块，可独立安装。
- `agently-design` - 已弃用，只转接 `agently-agentic-design`；下次更新检查并移除。
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
再加入 `agently-agentic-design` 或 `agently-triggerflow`。

## 设计职责与组合

`agently` 维护场景路由、跨轮进度/决策/证据状态与交接；产品 Skill 维护人的目标、界面和阅读验收；Agentic Skill 维护模型/Host/工作流契约。应用运行进度事件属于 Agentic 层，显示与理解属于产品层。混合任务共用已有清单，按实际依赖切换，不默认加载全部模块。

旧 `app-design-method` 已统一迁移为 `agently-product-design`，不提供旧名兼容。`agently-design` 单独标记弃用，不进入推荐新装清单；下次更新检查当前调用方和本机新入口，再移除旧入口，不设定时任务，不改历史证据。

## 安装

本机标准安装选择正式的 `app`、`migration` 和／或 `product-design` bundle；`design-compat` 仅供明确需要旧入口的调用方。更新前对比本地差异，保留有实际用途、明确特性／版本、能力检查及证据边界的开发补充，不把预览指导当作已发布支持。冗余本机别名在可恢复备份后退役；适用宿主不同的工作方式分别保留。Spotkit 是产品设计可选的外部插图辅助 Skill，不是 Agently 的强制依赖。

### Codex 显示语种

八个正式技能共用一份[中英 UI 词典](locales/skill-ui.json)。仓库默认分发英文显示名；技术 ID 和调用名称保持不变。Codex 读取的是静态名称，本工具在安装／更新时选择语种，不会随每轮会话语言实时切换。

在所需版本的仓库检出中执行，环境需要 Python 3.10+ 和 PyYAML：

```bash
python scripts/install.py --locale zh-CN
python scripts/install.py
python scripts/install.py --locale en --ui-only
```

第一条将八个正式技能安装／更新到 `$CODEX_HOME/skills`（未设置时为 `~/.codex/skills`），采用中文 UI；第二条沿用已保存语种；第三条只将已有技能的 UI 改为英文。独立安装可加 `--skills agently-product-design`，另选位置用 `--dest PATH`，预览修改用 `--dry-run`。

技能根目录的 `.agently-skills-ui.json` 保存语言选择和已管理文件的基线。已有策略、依赖、图标及其他 UI 字段保留。首次接管时将不同的本地文件作为补充保留；后续上游更新可覆盖未改动文件，双方同时改动时在写入前停止，等待核对。不删除未跟踪文件或旧别名。备份和回执保存在技能根目录旁的 `skill-update-backups/`。工具只安装当前检出内容，不自行拉取远端；通过其他安装器更新后，可运行 `--ui-only` 恢复已选语种。

维护者修改词典后执行 `python scripts/install.py --write-defaults`，再运行 `--check` 和 `python -m unittest discover -s validate -p test_skill_ui_install.py`。翻译界面不修改 SKILL.md 技术标识。

### 其他安装方式

先选择目标 coding agent，例如：

```bash
export AGENT=codex
```

开发新 Agently 应用时安装 `app` bundle：

```bash
for skill in \
  agently \
  agently-agentic-design \
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

产品设计可独立安装。以下命令从包含本次迁移的检出目录安装，不要求框架：

```bash
npx skills add . --agent "$AGENT" --skill agently-product-design -y
```
