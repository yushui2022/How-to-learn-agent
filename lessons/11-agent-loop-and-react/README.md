# 第 11 章：Agent 执行循环与 ReAct

> 状态：drafting

第 10 章我们先判断了什么任务值得做成 Agent。

现在开始写 Agent 的最小内部机制。

很多人第一次写 Agent，会写成这样：

```text
while true:
    把目标丢给模型
    让模型自己想办法
```

这不是工程实现，这是失控风险。

一个最小 Agent loop 应该是受控循环：

```text
目标和状态
-> 观察当前情况
-> 选择下一步动作
-> 校验并执行工具
-> 记录结果
-> 更新状态
-> 判断继续还是停止
```

本章回答三个问题：

- Agent loop 每一步到底要记录什么？
- ReAct 为什么要把“推理”和“行动”放在同一个循环里？
- 如何设置最大步数、失败退出和重复调用保护？

学完本章，你要留下三份项目资产：

- 一份 Agent loop 设计表：[agent-loop-design-template.md](./agent-loop-design-template.md)
- 一份执行轨迹记录表：[agent-loop-trace-template.md](./agent-loop-trace-template.md)
- 一个可运行最小示例：[simple_agent_loop.py](../../examples/simple-agent-loop/simple_agent_loop.py)

## Agent loop 不是无限循环

Agent loop 的核心不是“循环”，而是“带边界的循环”。

一个可靠循环至少包含 7 个环节：

| 环节 | 要回答的问题 |
| --- | --- |
| Goal | 这次任务目标是什么？ |
| State | 当前已经知道什么、做过什么？ |
| Observe | 现在看到的事实是什么？ |
| Decide | 下一步为什么选这个动作？ |
| Act | 调用哪个工具或执行哪个动作？ |
| Update | 工具结果如何改变状态？ |
| Stop | 是否完成、失败、超限或需要人工确认？ |

可以写成伪代码：

```python
state = init_state(goal)

for step in range(max_steps):
    observation = observe(state)
    decision = decide(goal, state, observation)

    if decision.should_stop:
        break

    tool_result = run_tool(decision.action)
    state = update_state(state, tool_result)
    trace.append(observation, decision, tool_result)

stop_with_reason(state)
```

注意这里有 `max_steps`。

没有最大步数的 Agent loop，迟早会在某个失败场景里反复调用同一个工具。

## ReAct 的工程意义

ReAct 可以理解成：

```text
Reason + Act
```

但在工程里，更适合把它拆成：

```text
Observation -> Decision summary -> Action -> Observation
```

也就是：

- 先看当前事实。
- 再给出可审计的决策摘要。
- 然后执行动作。
- 再看动作结果。

这里的 `Decision summary` 不是要求模型暴露完整内部思维链。

课程里记录的是给开发者调试用的决策摘要，例如：

```text
因为还没有查询课程资料，下一步先调用 search_course_notes。
```

不要把未经整理的中间推理直接展示给最终用户。

用户需要的是结论、依据和可理解的执行过程；开发者需要的是日志、状态和可复现轨迹。

## 最小循环示例

AI 学习助手的一个最小 Agent loop 可以这样设计：

```text
Goal: 帮用户完成 RAG 基础复习

Step 1:
Observe: 还没有课程资料
Decision: 先查 RAG 相关笔记
Action: search_course_notes("RAG")

Step 2:
Observe: 已找到 RAG 笔记
Decision: 生成一个练习题
Action: generate_practice("RAG")

Step 3:
Observe: 已生成练习题
Decision: 检查模拟答案并保存结果
Action: check_answer(...)

Stop:
复习任务完成，输出总结
```

这就是第 11 章要实现的级别。

它不是完整学习规划，也不是多天任务拆解。

第 12 章才会处理更长的 Planning。

## 状态要小而清楚

Agent loop 的状态不要一开始写成巨大对象。

第一版只保留能影响下一步决策的字段。

| 字段 | 用途 |
| --- | --- |
| `goal` | 当前任务目标 |
| `topic` | 本次学习主题 |
| `notes` | 是否找到相关资料 |
| `practice` | 是否已经生成练习 |
| `answer_checked` | 是否已经检查答案 |
| `step_count` | 已执行步数 |
| `last_action` | 上一步动作 |
| `failures` | 失败次数和失败原因 |

如果一个字段不会影响下一步，就先不要放进状态。

状态越乱，Agent 越难调试。

## 动作必须经过工具边界

第 9 章讲过工具调用。

第 11 章把工具放进循环，但工具边界不能放松。

每次行动前都要检查：

- 工具是否存在。
- 参数是否完整。
- 工具是否只读。
- 是否涉及写入、副作用或外部提交。
- 失败后是否允许重试。

一个循环里不能因为“Agent 想做”就跳过校验。

Agent loop 只负责选择动作，应用程序仍然负责校验、授权、执行和记录。

## 停止条件要提前写

停止条件比启动条件更重要。

至少准备这些停止条件：

| 停止条件 | 例子 | 处理方式 |
| --- | --- | --- |
| 目标完成 | 已生成练习并检查答案 | 输出总结 |
| 达到最大步数 | 3 步内没有完成 | 停止并说明 |
| 资料不足 | 检索不到课程资料 | 不编造，要求补资料 |
| 工具失败 | 工具返回错误 | 记录失败，必要时重试一次 |
| 重复动作 | 连续调用同一个无效工具 | 停止或换策略 |
| 权限不足 | 需要写入或删除数据 | 请求用户确认 |

如果停止条件写不出来，说明任务边界还没设计清楚。

## 执行轨迹是调试入口

Agent 的每一步都要留下轨迹。

最小轨迹至少包括：

| 字段 | 说明 |
| --- | --- |
| `step` | 第几步 |
| `observation` | 这一步开始时看到什么 |
| `decision_summary` | 为什么选择这个动作 |
| `action` | 调用了什么工具或做了什么动作 |
| `result` | 工具返回什么 |
| `state_change` | 状态发生什么变化 |
| `stop_reason` | 如果停止，为什么停止 |

没有轨迹，就很难回答这些问题：

- Agent 为什么调用这个工具？
- 为什么重复调用？
- 是工具失败，还是决策失败？
- 哪一步状态变错了？
- 为什么最终停止？

后面第 16 章会专门讲观测和调试。

本章先养成记录轨迹的习惯。

## 成熟项目观察：LangGraph、OpenHands 和 SmolAgents

本章主案例是 [LangGraph](https://github.com/langchain-ai/langgraph)，对比案例是 [OpenHands](https://github.com/OpenHands/OpenHands) 和 [SmolAgents](https://github.com/huggingface/smolagents)。

对应源码 Lab：

- [Lab 01：通用核心框架](../../labs/01-core-frameworks/README.md)
- [Lab 02：编程 Agent](../../labs/02-coding-agents/README.md)
- [Lab 08：轻量入门与研究级 Agent](../../labs/08-lightweight-research/README.md)

### LangGraph：把循环变成显式状态图

LangGraph 适合观察一个问题：

```text
如何让 Agent loop 不是一段看不见边界的 while 循环？
```

你可以重点看：

- 状态对象如何定义。
- 节点如何执行动作。
- 条件边如何决定下一步。
- 什么时候进入结束节点。
- 人工确认如何插入流程。

迁移到 AI 学习助手：

```text
把“查资料、出练习、检查答案、停止”看成几个明确节点，而不是一个混在 Prompt 里的大任务。
```

### OpenHands：编程 Agent 的循环更容易暴露风险

编程 Agent 的动作通常更危险。

它可能读取文件、编辑代码、运行命令、看测试结果，再继续修改。

所以观察 OpenHands 这类项目时，本章只看一个切口：

```text
一次行动后，系统如何把命令输出、文件变化或测试失败变成下一步观察？
```

迁移到代码仓库助手：

- 先允许只读搜索和读取文件。
- 再允许生成修改建议。
- 真正写文件和运行命令时要加入确认、沙箱和日志。

### SmolAgents：轻量实现适合看清 ReAct 骨架

轻量项目适合观察：

- 工具如何注册。
- 模型如何选择动作。
- 观察结果如何返回循环。
- 循环如何停止。

迁移到 AI 学习助手：

```text
先写一个最多 3 步的透明循环，把每一步打印出来。
```

## 项目锚点

AI 学习助手在本章实现一个小任务：

```text
根据用户目标完成一次 RAG 复习。
```

第一版只允许 3 个工具：

| 工具 | 权限 | 用途 |
| --- | --- | --- |
| `search_course_notes` | 只读 | 查询 RAG 课程资料 |
| `generate_practice` | 只读 | 生成练习题 |
| `check_answer` | 只读 | 检查模拟答案 |

第一版不做：

- 长期学习计划。
- 多天任务拆解。
- 自动写入长期记忆。
- 调用外部浏览器。
- 多 Agent 协作。

这样读者可以先看清 Agent loop，再进入后续章节。

## 运行示例

第 11 章示例不调用真实模型。

它用规则模拟一个 Agent 的决策过程，重点展示循环结构和执行轨迹。

从仓库根目录运行：

```powershell
python .\examples\simple-agent-loop\simple_agent_loop.py --case success
python .\examples\simple-agent-loop\simple_agent_loop.py --case missing-notes
python .\examples\simple-agent-loop\simple_agent_loop.py --case tool-error
python .\examples\simple-agent-loop\simple_agent_loop.py --case looping-policy
python .\examples\simple-agent-loop\simple_agent_loop.py --case success --max-steps 2
```

你要观察：

- 成功路径如何停止。
- 资料缺失时是否拒绝编造。
- 工具失败时是否记录失败。
- 错误策略反复调用时，最大步数如何拦住循环。

## 动手任务

完成下面 4 件事：

1. 填写 [agent-loop-design-template.md](./agent-loop-design-template.md)。
2. 运行 [simple_agent_loop.py](../../examples/simple-agent-loop/simple_agent_loop.py) 的四个场景。
3. 把其中一个场景的轨迹写进 [agent-loop-trace-template.md](./agent-loop-trace-template.md)。
4. 修改一次 `--max-steps`，观察 Agent 是否会提前停止。

## 检查题

先自己判断，再看参考答案。

| 问题 | 你的判断 |
| --- | --- |
| Agent loop 为什么不能写成无限循环？ |  |
| ReAct 里的行动结果为什么要回到下一步观察？ |  |
| 执行轨迹至少要记录哪些字段？ |  |
| 工具失败时应该继续猜答案，还是停止或重试？ |  |
| 为什么不要把未经整理的内部推理直接展示给用户？ |  |

参考答案：

| 问题 | 参考判断 |
| --- | --- |
| 因为失败场景可能导致重复调用、成本失控和错误动作连续发生 |
| 因为下一步决策必须基于真实结果，而不是基于上一轮的假设 |
| 至少记录 step、observation、decision_summary、action、result、state_change、stop_reason |
| 先记录失败，再按规则重试或停止，不能编造工具结果 |
| 用户需要可理解结论和依据；完整内部推理可能冗长、混乱，也不适合作为产品输出 |

## 本章小结

这一章你把 Agent 从“概念判断”推进到了“最小可运行循环”。

你现在应该已经有：

- 一个最多执行几步的 Agent loop。
- 一组工具动作。
- 一份状态对象。
- 一份执行轨迹。
- 至少三个停止条件。
- 一个失败场景复盘。

下一章会在这个循环基础上，继续讲任务拆解、计划执行和重规划。

## 上一章 / 下一章

- 上一章：[第 10 章：Agent 到底是什么](../10-agent-fundamentals/README.md)
- 下一章：[第 12 章：Planning 任务拆解与计划执行](../12-planning-and-task-decomposition/README.md)
