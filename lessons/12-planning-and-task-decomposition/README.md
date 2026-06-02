# 第 12 章：Planning 任务拆解与计划执行

> 状态：drafting

第 11 章我们写了最小 Agent loop。

它适合处理短任务：

```text
查资料 -> 生成练习 -> 检查答案 -> 停止
```

但用户经常提出更长的目标：

```text
我想两周内学会 RAG。
帮我调研一个 Agent 框架。
帮我把这个代码仓库改到能运行测试。
```

这些目标不能只靠下一步动作。

它们需要先拆成可执行、可检查、可恢复的步骤。

本章只讲一个核心原则：

```text
计划不是承诺，计划是执行前的假设。
```

计划要能执行，也要能被检查和修改。

本章回答三个问题：

- 如何把一个长期目标拆成 4 到 6 个可执行步骤？
- Planner、Executor、Reviewer 分别负责什么？
- 什么时候继续执行，什么时候重新规划，什么时候停止？

学完本章，你要留下三份项目资产：

- 一份 Planning Brief：[planning-brief-template.md](./planning-brief-template.md)
- 一份计划执行记录：[plan-execution-record-template.md](./plan-execution-record-template.md)
- 一个可运行示例：[plan_and_execute.py](../../examples/plan-and-execute/plan_and_execute.py)

## 为什么需要 Planning

Agent loop 解决的是“下一步怎么走”。

Planning 解决的是“这件事整体怎么拆”。

两者关系可以这样看：

```text
用户目标
-> Planner 拆成计划
-> Executor 执行一个步骤
-> Reviewer 检查证据
-> 继续 / 重规划 / 停止
```

没有计划，Agent 容易只盯着眼前动作。

没有执行反馈，计划又会变成空话。

所以本章不教“写一个很漂亮的计划”，而是教：

```text
如何写一个能被执行和检查的计划。
```

## 计划和工作流的区别

第 6 章讲过工作流。

工作流是提前固定的流程。

Planning 是根据当前目标生成或调整的任务结构。

| 类型 | 适合场景 | 变化方式 |
| --- | --- | --- |
| 工作流 | 步骤长期稳定 | 开发者修改流程 |
| Agent loop | 短任务的动态下一步 | 根据观察选择动作 |
| Planning | 长目标的任务拆解 | 根据目标和执行结果重规划 |

例如：

```text
每天固定生成学习计划
```

适合工作流。

```text
根据我当前基础，两周内帮我学会 RAG，并根据练习结果调整安排
```

更适合 Planning。

## 三个角色：Planner、Executor、Reviewer

Planning 不一定非要做成多 Agent。

即使只有一个程序，也可以把职责分清楚。

| 角色 | 负责什么 | 不负责什么 |
| --- | --- | --- |
| Planner | 拆任务、排序、定义成功标准和重规划条件 | 不直接伪造执行结果 |
| Executor | 执行当前步骤，产出证据 | 不随意改整份计划 |
| Reviewer | 检查结果是否满足步骤标准 | 不为了继续而忽略失败 |

这三个角色可以是三个函数，也可以是三个 Agent。

初学项目先用三个函数就够。

## 一个好步骤长什么样

不要把计划写成空泛句子：

```text
学习 RAG。
理解概念。
多练习。
```

这些都不可执行。

一个可执行步骤至少要写清楚 6 件事：

| 字段 | 说明 |
| --- | --- |
| 步骤目标 | 这一小步要完成什么 |
| 输入 | 需要什么资料或状态 |
| 动作 | 调用什么工具或执行什么操作 |
| 输出 | 产出什么可见结果 |
| 通过标准 | 怎么知道这一步完成了 |
| 失败处理 | 失败后重试、换方案还是停止 |

AI 学习助手里的一个步骤可以这样写：

| 字段 | 内容 |
| --- | --- |
| 步骤目标 | 找到 RAG 基础资料 |
| 输入 | 主题：RAG |
| 动作 | `search_course_notes("RAG")` |
| 输出 | 至少 2 条相关课程片段 |
| 通过标准 | 片段包含“检索”和“回答”关系 |
| 失败处理 | 如果找不到资料，停止并要求补资料 |

这样的步骤才能被执行和检查。

## 不要过度拆解

很多初学者会把计划拆得太细。

比如：

```text
打开工具。
输入关键词。
等待结果。
阅读第一行。
阅读第二行。
整理一句话。
```

这不是有效规划。

它会带来三个问题：

- 步骤太多，成本和延迟上升。
- 每一步价值太小，日志噪声变大。
- Reviewer 很难判断整体是否推进。

第一版计划建议控制在 4 到 6 步。

拆到“每一步都有可见产出”就够了。

## 什么时候需要重规划

计划执行中会出现新信息。

重规划不是失败，它是让计划继续贴近现实。

常见重规划条件：

| 条件 | 例子 | 处理方式 |
| --- | --- | --- |
| 资料缺失 | 检索不到 RAG 资料 | 改为请求用户补资料 |
| 工具失败 | 练习生成工具报错 | 重试一次或换工具 |
| 用户目标变化 | 用户改成先学 Tool Calling | 重新生成计划 |
| 通过标准不满足 | 练习太简单或不相关 | 回到 Planner 调整步骤 |
| 风险升级 | 需要写入或删除数据 | 停止并请求确认 |
| 达到预算 | 超过最大步数或成本 | 停止并说明已完成部分 |

重规划也要有限制。

不要每一步都重新规划。

建议第一版只允许 1 到 2 次重规划。

## 计划执行记录

计划执行时，每一步都要留下证据。

最小记录包括：

| 字段 | 说明 |
| --- | --- |
| plan_version | 第几版计划 |
| step_id | 当前步骤编号 |
| owner | Planner / Executor / Reviewer |
| action | 实际执行的动作 |
| expected_output | 预期产出 |
| evidence | 实际证据 |
| status | pending / done / failed / skipped |
| reviewer_decision | continue / replan / stop |
| replan_reason | 为什么重规划 |

这样你才能复盘：

- 原计划是否合理？
- 哪一步失败了？
- 失败后为什么重规划？
- 重规划后的计划是否更短、更清晰？
- 最终停止是否合理？

## 成熟项目观察：LangGraph、AutoGen 和 CrewAI

本章主案例是 [LangGraph](https://github.com/langchain-ai/langgraph)，对比案例是 [AutoGen](https://github.com/microsoft/autogen) 和 [CrewAI](https://github.com/crewAIInc/crewAI)。

对应源码 Lab：

- [Lab 01：通用核心框架](../../labs/01-core-frameworks/README.md)
- [Lab 04：多智能体协作](../../labs/04-multi-agent/README.md)

### LangGraph：把计划执行放进状态图

LangGraph 适合观察：

- 计划如何进入状态。
- 执行节点如何读取当前步骤。
- Reviewer 如何决定继续、重试或结束。
- 重规划如何更新状态。

迁移到 AI 学习助手：

```text
把“当前计划、当前步骤、执行证据、重规划次数”放进状态对象。
```

第 13 章会继续讲 Memory 与 State。

### AutoGen：角色对话不等于职责清晰

AutoGen 适合观察多角色对话和协作。

但本章要先建立一个判断：

```text
角色名字不能代替职责边界。
```

如果 Planner 也在执行，Executor 也在改计划，Reviewer 又不检查证据，那么多角色只会让问题更难调试。

迁移到研究写作 Agent：

- 研究员负责找资料。
- 写作者负责组织内容。
- 审阅者负责检查引用是否支持结论。

每个角色都要有输入、输出和停止条件。

### CrewAI：任务和角色要绑定产出

CrewAI 适合观察任务、角色和流程编排。

本章只迁移一个点：

```text
不要只写角色，要写每个角色交付什么。
```

迁移到 AI 学习助手：

- Planner 交付学习任务列表。
- Executor 交付练习和答案检查结果。
- Reviewer 交付通过、重规划或停止判断。

## 项目锚点

AI 学习助手在本章处理这个目标：

```text
我想两周内学会 RAG。
```

第一版不要真的规划 14 天。

先拆出一条可执行的学习链：

| Step | Owner | 目标 | 输出 |
| --- | --- | --- | --- |
| 1 | Planner | 确认目标和当前基础 | 学习目标摘要 |
| 2 | Executor | 查询 RAG 课程资料 | 相关资料片段 |
| 3 | Executor | 解释核心概念 | 概念说明 |
| 4 | Executor | 生成练习 | 练习题 |
| 5 | Reviewer | 检查是否满足学习目标 | 继续 / 重规划 / 停止 |

可选项目也可以这样拆：

| 项目 | 长目标 | 第一版计划 |
| --- | --- | --- |
| 研究写作 Agent | 调研一个 Agent 框架 | 搜索资料、筛选来源、写提纲、审阅引用 |
| 客服工单 Agent | 处理复杂售后问题 | 查订单、查规则、生成回复、请求人工确认 |
| 代码仓库助手 | 修复一个测试失败 | 定位失败、读相关文件、提出修改、运行测试、复盘 |

## 运行示例

第 12 章示例不调用真实模型。

它用规则模拟 Planner、Executor、Reviewer。

从仓库根目录运行：

```powershell
python .\examples\plan-and-execute\plan_and_execute.py --case happy-path
python .\examples\plan-and-execute\plan_and_execute.py --case retrieval-fails
python .\examples\plan-and-execute\plan_and_execute.py --case user-change
python .\examples\plan-and-execute\plan_and_execute.py --case happy-path --max-steps 3
python .\examples\plan-and-execute\plan_and_execute.py --case user-change --json
```

你要观察：

- `happy-path` 如何按计划完成。
- `retrieval-fails` 如何因为资料缺失触发重规划。
- `user-change` 如何因为用户目标变化重建计划。
- `--max-steps 3` 如何让未完成任务提前停止。

## 动手任务

完成下面 4 件事：

1. 填写 [planning-brief-template.md](./planning-brief-template.md)。
2. 运行 [plan_and_execute.py](../../examples/plan-and-execute/plan_and_execute.py) 的三个场景。
3. 把其中一个场景写进 [plan-execution-record-template.md](./plan-execution-record-template.md)。
4. 为你的项目写出至少 2 个重规划条件。

## 检查题

先自己判断，再看参考答案。

| 问题 | 你的判断 |
| --- | --- |
| 为什么说计划不是承诺？ |  |
| Planner、Executor、Reviewer 的职责分别是什么？ |  |
| 一个可执行步骤至少要写清楚哪些字段？ |  |
| 什么情况下应该重规划？ |  |
| 为什么不要把计划拆得过细？ |  |

参考答案：

| 问题 | 参考判断 |
| --- | --- |
| 因为计划是基于当前信息生成的假设，执行中遇到新证据时需要调整 |
| Planner 负责拆解和排序，Executor 负责执行当前步骤，Reviewer 负责检查证据并决定继续、重规划或停止 |
| 至少写清目标、输入、动作、输出、通过标准和失败处理 |
| 资料缺失、工具失败、用户目标变化、通过标准不满足、风险升级或达到预算时 |
| 过细会增加成本、延迟和日志噪声，让 Reviewer 难以判断是否真正推进 |

## 本章小结

这一章你把 Agent 从短循环推进到长任务执行。

你现在应该已经有：

- 一份 Planning Brief。
- 一份 4 到 6 步计划。
- 一份计划执行记录。
- 至少一个重规划场景。
- 一个停止条件和最大步数限制。

下一章会继续处理这些计划、进度和执行结果如何进入 Memory 与 State。

## 上一章 / 下一章

- 上一章：[第 11 章：Agent 执行循环与 ReAct](../11-agent-loop-and-react/README.md)
- 下一章：[第 13 章：Memory 与 State](../13-memory-and-state/README.md)
