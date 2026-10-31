# Reporting examples

The following scenarios are synthetic style examples, not records of real work.
Adapt their organization to the reader; never copy their findings as evidence.

## Progress on a concrete change

这次在修复订单列表切换筛选条件后仍显示旧数据的问题，目标是让列表始终对应当前选择。已定位到旧请求晚返回覆盖新结果，修复后代表性回归通过，正在完成页面状态检查。

| 状态 | 任务 | 实际进展 |
|---|---|---|
| ✅ 已完成 | 1. 定位旧数据来源 | 已复现连续切换条件时的请求返回顺序问题 |
| ✅ 已完成 | 2. 修复结果更新逻辑 | 旧请求不再覆盖当前查询，相关回归通过 |
| 🔄 进行中 | 3. 检查页面交互 | 筛选和清空路径通过，正在检查空结果与失败重试 |
| ⬜ 未开始 | 4. 发布并复核 | 页面检查完成后按项目发布流程推进 |

本轮修复把结果更新与当前查询关联，解决了“筛选条件已改变、列表仍是旧内容”的错配。下一步完成空结果和失败重试检查，再核对发布条件。

补充：当前证据来自本机与预发布环境，生产验证安排在发布后。

The main claim is scoped and the remaining work is visible. The closing note
does not undo an exaggerated claim of complete acceptance.

## A blocker changes the next action

这次在为账单服务上线新的计算规则。候选版本的功能回归已通过，但迁移演练发现部分历史账单缺少必要字段，当前发布受阻；需要先补齐数据并重跑演练。

Follow with the complete current plan, retaining completed, pending and cancelled
items. Explain the missing data, business consequence, remediation owner and
recovery condition where the reader decides what to do next. Do not write
“ready to release” and hide this blocker in a closing disclaimer. Continue
independent authorized work while the dependency is addressed.

## A brief question during a long task

User: “这里的幂等是什么意思？”

Agent: “同一个操作重复提交，也只产生一次业务结果。例如用户重复点击付款，系统识别为同一次付款请求，避免重复扣款。”

No new plan, full taskboard, mandatory disclaimer or diagram is needed for this
answer. Preserve the existing task state and continue the authorized work.

## A decision changes a long plan

Open with the current objective and the consequence of the decision. Show the
complete current plan, including the original ID of the cancelled approach and
the new or reopened item. Explain what actually changed this round. Keep prior
decision details in the existing record; retrieve them if necessary to explain
the current choice or when the user asks for the full history. A candidate,
accepted decision and applied implementation have distinct statuses.

## Several tasks in one report

Give each task a descriptive introduction before its rows. When an actual
task/document URL is available, make that title the link; the synthetic example
below has no external source. The short titles carry the task context, so another
background paragraph is unnecessary. These are two groups of one current plan,
not newly created work records.

**任务一：修复共享资料切换时的跨端定位与恢复**

| 状态 | 事项 | 当前进展 |
|---|---|---|
| ✅ 已完成 | 1. 修复切换与恢复 | 已完成修复及本机回归 |
| 🔄 进行中 | 2. 上线后复核 | 已上线，继续验证两个账号的协作路径 |

**任务二：完善应用权限范围与审计记录**

| 状态 | 事项 | 当前进展 |
|---|---|---|
| ✅ 已完成 | 3. 修复权限范围与审计 | 已完成实现与相应回归 |
| 🔄 进行中 | 4. 核对生产权限行为 | 角色保存和审计已验，继续撤权验证 |

The reader can identify both problems without decoding IDs or inferring the
goal from implementation actions. In real reports, retain the actual task IDs,
all planned items and evidence-backed states; do not replace them with these
illustrative numbers or claim these synthetic results as observed.
