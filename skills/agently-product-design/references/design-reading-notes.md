# 设计资料与应用索引

核对日期：2026-10-08，组件复用与性能资料补充于 2026-10-14。目标是为项目交互决策找到合适依据。Eleken 的[UI/UX 书单](https://www.eleken.co/blog-posts/ui-ux-books)提供发现线索；以下按任务筛选，并尽量核对作者或出版方资料，同时补入标准与成熟设计系统。书单排名不作为有效性证据。

“已查阅”仅限下表的材料范围，未获取或阅读全文的书不宣称已精读。关键点是简短转述；“落地方式”是本 Skill 综合提出的用法，需要项目验证，不是作者逐条提出的要求。

## 1. 按设计问题选阅读入口

| 设计问题 | 资料、作者与查阅范围 | 可用关键点 | 本 Skill 的落地方式与边界 |
| --- | --- | --- | --- |
| 用户总在猜入口和主次 | **Don’t Make Me Think, Revisited**，Steve Krug；[作者介绍](https://sensible.com/dont-make-me-think/)、[授权样章：第 4 章](https://sensible.com/downloads/DMMT-Revisited-sample-chapter.pdf)、[出版方视觉层级摘录](https://www.peachpit.com/articles/article.aspx?p=2209310) | 标签与视觉关系应帮助理解；选择的心智负担不能只用点击数代表 | 逐步检查“这是哪里、什么相关、下一动作意味着什么”，优化标题、归组与反馈；不删除必要的业务判断，不套数字点击公式 |
| 看见界面却不知道怎样操作 | **The Design of Everyday Things**，Don Norman；本轮使用作者专题文章[Signifiers, not affordances](https://jnd.org/signifiers-not-affordances/)，并非整本书 | 可被感知的行动线索帮助人理解可做什么 | 对照控件的外观、名称与真实操作；识别“像能点但不能点”“可展开却没有线索”；图标存在不代表用户理解 |
| 布局、导航、表单缺少可复用模式 | **Designing Interfaces, 3rd ed.**，Jenifer Tidwell、Charles Brewer、Aynne Valencia；[出版方简介与目录](https://www.oreilly.com/library/view/designing-interfaces-3rd/9781492051954/) | 从用户理解出发，用模式组织信息与任务 | 建立项目模式库，写适用/不适用条件、变体与示例；本轮未逐条阅读书中模式，具体选型需另核对可访问的一手指导 |
| 小动作没有反馈或状态混乱 | **Microinteractions**，Dan Saffer；[出版方简介与目录](https://www.oreilly.com/library/view/microinteractions/9781449342760/) | 微交互由触发、规则、反馈、循环/模式等部分构成 | 给相关组件定义触发→允许条件→反馈→后续行为；检查重复触发、关闭和再次进入，不把“微交互”简化为动画装饰 |
| 页面与组件各自好看却不协调 | **Atomic Design**，Brad Frost；[作者公开第 2 章](https://atomicdesign.bradfrost.com/chapter-2/) | 部件和整体需要往返校验，代表内容能暴露系统限制 | 同时检查组件状态图、组合页面和长内容；复用当前库，不强制原子层级命名或一次重构全站 |
| 不清楚需求是真问题还是猜测 | **Just Enough Research, 2nd ed.**，Erika Hall；[出版方介绍](https://abookapart.com/products/just-enough-research) | 用研究识别假设、减少不确定性 | 把最影响决策的未知单列，选择有针对性的观察、访谈或数据核对；未读全书，不将简介扩写成完整研究方法论 |
| 缺少实际可用性检查 | **Rocket Surgery Made Easy**，Steve Krug；[作者介绍](https://sensible.com/rocket-surgery-made-easy/) | 将可用性测试作为可执行的日常改进工作 | 选真实任务观察困难，优先修复主要障碍；Agent 模拟与真人观察分开，不把固定人数/时长当普适门槛 |
| 无法判断改动是否改善体验 | **Measuring the User Experience, 3rd ed.**，Bill Albert、Tom Tullis；[出版方简介与目录](https://www.educate.elsevier.com/book/details/9780128180808) | 为问题选择恰当指标，结合行为与主观反馈 | 按任务记录成功、错误、耗时/往返等相关指标，解释测量条件；小样本走查不声称统计显著或普遍收益 |

## 2. 将原则接到具体规范

| 一手资料 | 用途与已核对内容 | 使用边界 |
| --- | --- | --- |
| [NN/g：Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/) | 常用与次要内容分层、入口可理解；区分按需与分步展示 | 按使用场景验证收纳代价，不能隐藏当前决定必要的信息 |
| [NN/g：Aesthetic and Minimalist Design](https://www.nngroup.com/articles/aesthetic-minimalist-design/) | 无关信息会与必要信息竞争注意力；删减应服务任务清晰度 | 默认不添装饰性副标题、介绍与重复说明；保留有具体任务价值的标签、条件和恢复提示 |
| [GOV.UK Design System](https://design-system.service.gov.uk/)与[贡献标准](https://design-system.service.gov.uk/community/contribution-criteria/) | 样式、组件、任务模式的组织；新模式需要用途与验证依据 | 借鉴规范建设与复用机制，不强制其品牌或政务业务流程 |
| [GOV.UK Details](https://design-system.service.gov.uk/components/details/) | 详情展开的适用条件与使用示例 | 辅助信息可展开，多数用户都需要的内容应重新判断默认可见性 |
| [Carbon：2x Grid 指导](https://www.carbondesignsystem.com/building-blocks/foundations/2x-grid/guidelines) | 内容层级、重复布局结构以及面板对内容区的影响 | 依据内容选布局，不复制 IBM 的具体尺寸、列数与导航 |
| [WAI-ARIA APG：Disclosure](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/)与[Modal Dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) | Web 控件语义、展开状态、键盘与焦点行为 | 这是实施模式指导，不是整站合规认证；仍需真实操作与辅助技术验证 |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | 选择适用的可访问性成功准则核对 | 看原条款和例外，不用经验数字代替标准；原生应用还需其平台规范 |

同日补充核对《Don’t Make Me Think》第 3 版[出版方目录](https://www.peachpit.com/store/dont-make-me-think-revisited-a-common-sense-approach-9780321965516)中的第 5 章“Omit needless words”。这是章节主题确认，未获取第 5 章全文；本 Skill 的具体文案删减规则来自用户要求、已查资料与任务应用判断。

2026-10-14 补入组件与性能一手资料：

- [React：Thinking in React](https://react.dev/learn/thinking-in-react)：按职责、数据和界面关系划分组件；用来校准复用边界，不要求其他技术栈迁移到 React。
- [Vue：Performance](https://vuejs.org/guide/best-practices/performance.html)：依赖大小与实际构建成本、按需加载及更新性能；用来要求选型测量，不强制使用 Vue 或固定优化手段。
- [Web Vitals](https://web.dev/articles/vitals)及[渲染性能](https://web.dev/articles/rendering-performance)：加载、响应、视觉稳定性与帧预算的参考；按当前定义和实际设备核对，不替代业务就绪或服务性能。
- [Google SRE：Implementing SLOs](https://sre.google/workbook/implementing-slos/)：用户目标、测量口径和利益相关者协商；不自动套用可用性或容量承诺。
- [k6 测试类型](https://grafana.com/docs/k6/latest/testing-guides/test-types/)、[API负载模型](https://grafana.com/docs/k6/latest/testing-guides/api-load-testing/)及[指标](https://grafana.com/docs/k6/latest/using-k6/metrics/reference/)：风险驱动的测试类型与实际负载核对；不强制安装 k6，也不照抄示例流量/时长。

组件最少必要增量与公共库要求来自用户指导；[组件复用](interaction-system.md)和[性能测试方法](performance-guidance.md)是本 Skill 的应用方案，不是上述资料共同规定的一套固定流程。

## 3. 在任务中使用这些资料

文档撰写、读者走查及 ASD-STE100 资料现由[文档表达模块](../modules/document-expression.md)及其参考维护。应用布局与文档语言分别使用适用规则，STE 不作为版式标准。

先写具体问题，再找适用规则：

- 导航找不到、术语冲突：检查对象/任务模型、标签及跨页一致性；必要时安排导航结构验证。
- 信息拥挤、正文太窄：先查任务关系与内容清单，再用[展示与布局指南](progressive-disclosure-layout.md)比较候选。
- 多页行为不一致：用[项目交互规范](interaction-system.md)建立规则→共用组件→代表页面→证据的对应。
- 控件看似明确但用起来不确定：写状态转换，核对反馈、返回与数据保留。
- 无法取舍方案：将不确定性变成最小验证任务；保留失败证据，再更新规则。

适用的平台既有约定、真实使用证据和业务必要条件应参与判断。资料相互冲突时记录各自场景与限制，解释当前选择；不要靠引用数量、出版年代或作者声誉“投票”。未知的具体标准或组件行为再查最新官方资料，不让所有日常修订都承担一次完整文献研究。

## 4. 继续维护

新增资料时记录标题、作者/机构、可访问链接、查阅日期与范围、解决的决策问题及限制。只将可操作、与现有规则有明确关系的内容加入 Skill；泛泛观点留作阅读线索。

项目反馈应回流到规则和例外：哪个情境支持原规则、哪个出现反例、是否需要命名变体、哪些实现与验收要同步调整。新资料不自动使旧验证失效；规则或实现实际改变时，才按影响重新验证。
