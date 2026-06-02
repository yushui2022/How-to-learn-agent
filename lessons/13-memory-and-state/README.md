# 第 13 章：Memory 与 State

> 状态：drafting

第 12 章我们把长期目标拆成了计划，并记录了执行证据。

下一步会遇到一个问题：

```text
这些信息到底应该放在哪里？
```

比如 AI 学习助手会看到：

- 用户当前目标：两周内学会 RAG。
- 当前计划：先学第 7 章，再做第 8 章评估。
- 本轮工具结果：检索到了 3 段资料。
- 用户偏好：喜欢项目驱动学习。
- 用户薄弱点：无答案处理容易做错。
- 用户随口说的一句话：今天有点累。

这些信息不能都塞进 Prompt，也不能都存成长期记忆。

本章只讲一个原则：

```text
State 用来推进当前任务，Memory 用来影响未来任务。
```

本章回答三个问题：

- State、Log、Memory 到底有什么区别？
- 什么信息可以写入长期记忆，什么信息不应该保存？
- 如何设计可查看、可更新、可删除的记忆流程？

学完本章，你要留下三份项目资产：

- 一份 State Schema：[state-schema-template.md](./state-schema-template.md)
- 一份 Memory Policy：[memory-policy-template.md](./memory-policy-template.md)
- 一个可运行示例：[memory_state.py](../../examples/memory-state/memory_state.py)

## 先区分三件事

很多 Agent 项目混乱，是因为把三类数据混在一起。

| 类型 | 作用 | 生命周期 | 例子 |
| --- | --- | --- | --- |
| State | 推进当前任务 | 当前任务或会话内 | 当前步骤、计划版本、工具结果 |
| Log | 复盘发生过什么 | 运行后保留，通常只给开发者或系统 | 工具调用记录、错误、耗时 |
| Memory | 影响未来任务 | 跨会话保留，可检索、更新、删除 | 学习偏好、长期目标、薄弱点 |

一句话判断：

```text
这条信息是否应该影响未来的新任务？
```

如果答案是否，它通常不是长期记忆。

## State 是当前任务的控制面板

State 不是聊天记录。

State 是 Agent 决策下一步时需要读取的结构化信息。

第 12 章的计划执行可以有这样的 State：

```json
{
  "goal": "两周内学会 RAG",
  "plan_version": 2,
  "current_step": "generate_practice",
  "completed_steps": ["confirm_goal", "retrieve_notes", "explain_concept"],
  "last_tool_result": "generated practice",
  "replan_count": 1,
  "stop_reason": null
}
```

这些字段服务于当前任务：

- 下一步该执行哪个步骤？
- 是否已经重规划过？
- 上一步工具返回什么？
- 是否应该停止？

任务结束后，这些字段不一定都要进入长期记忆。

例如 `last_tool_result` 很可能只是短期状态。

## Memory 是被筛选过的长期信息

长期记忆应该少而准。

AI 学习助手可以考虑保存：

| 信息 | 是否适合长期记忆 | 原因 |
| --- | --- | --- |
| 用户想两周内学会 RAG | 适合 | 会影响后续学习安排 |
| 用户喜欢项目驱动学习 | 适合 | 会影响教学方式 |
| 用户第 8 章无答案处理做错 | 适合，但要可修改 | 会影响复习重点 |
| 本轮检索返回第 3 个 chunk | 不适合 | 只是一次工具结果 |
| 用户说今天很累 | 通常不适合 | 临时状态，不应默认长期保存 |
| 用户身份证、密码、私密信息 | 不适合 | 敏感信息，不应保存 |

记忆不是“把所有历史都存下来”。

记忆是经过策略筛选、带来源和边界的长期信息。

## 什么不能默认写入记忆

下面这些信息默认不要写入长期记忆：

- 密码、密钥、身份证、银行卡、联系方式等敏感信息。
- 用户没有明确希望保存的隐私内容。
- 一次性情绪、临时抱怨、随口说法。
- 未验证的推测，例如“用户一定不懂数学”。
- 工具返回的原始片段。
- 完整聊天记录。
- 模型自己编出来的用户画像。

如果确实需要保存，也要让用户知道：

```text
我要记住：你更喜欢项目驱动学习。
是否保存？
```

用户应该能查看、修改、删除和关闭记忆。

## 记忆生命周期

一个可靠的记忆流程至少有 6 步：

```text
发现候选信息
-> 判断是否值得保存
-> 判断是否敏感
-> 必要时请求确认
-> 写入带来源的结构化记忆
-> 后续检索、更新或删除
```

可以写成表：

| 阶段 | 要做什么 |
| --- | --- |
| Capture | 从用户输入、任务结果或评估结果里发现候选信息 |
| Classify | 判断是偏好、目标、进度、薄弱点还是敏感信息 |
| Consent | 对用户偏好、长期目标等信息请求确认 |
| Write | 写入结构化字段，带来源和时间 |
| Retrieve | 只在相关任务里取出相关记忆 |
| Update/Delete | 允许修正、过期和删除 |

没有删除能力的记忆系统，很难让用户信任。

## 记忆记录应该长什么样

不要只存一句话。

至少保留这些字段：

| 字段 | 说明 |
| --- | --- |
| `id` | 稳定标识 |
| `type` | preference / goal / progress / weak_point |
| `content` | 记忆内容 |
| `source` | 来自用户确认、练习结果还是系统判断 |
| `scope` | 只用于学习助手，还是用于所有项目 |
| `confidence` | 可信程度 |
| `created_at` | 写入时间 |
| `expires_at` | 是否过期 |
| `user_visible` | 用户是否可查看 |
| `deletable` | 是否允许删除 |

AI 学习助手的一条记忆可以是：

```json
{
  "id": "pref_project_based_learning",
  "type": "preference",
  "content": "用户更喜欢项目驱动学习",
  "source": "user_confirmed",
  "scope": "ai-learning-assistant",
  "confidence": 1.0,
  "user_visible": true,
  "deletable": true
}
```

## 检索记忆也要克制

不要每次都把所有记忆塞进 Prompt。

记忆检索要回答：

- 当前任务需要哪些记忆？
- 这些记忆是否仍然有效？
- 是否可能把用户带偏？
- 是否有敏感信息不该进入上下文？

比如用户问：

```text
今天继续学 RAG。
```

可以检索：

- 学习目标。
- 已完成章节。
- RAG 相关薄弱点。
- 教学偏好。

不应该检索：

- 与 RAG 无关的旧任务。
- 原始聊天记录。
- 敏感信息。

## 成熟项目观察：mem0、Letta 和 LangGraph

本章主案例是 [mem0](https://github.com/mem0ai/mem0)，对比案例是 [Letta](https://github.com/letta-ai/letta) 和 [LangGraph](https://github.com/langchain-ai/langgraph)。

对应源码 Lab：

- [Lab 05：记忆、推理与模型服务专项](../../labs/05-memory-reasoning/README.md)
- [Lab 03：个人助手与数字分身](../../labs/03-personal-assistants/README.md)
- [Lab 01：通用核心框架](../../labs/01-core-frameworks/README.md)

### mem0：看记忆的生命周期

观察 mem0 这类记忆项目时，不要只看“能不能记住”。

要看：

- 记忆如何写入。
- 记忆如何检索。
- 记忆如何更新。
- 记忆如何删除。
- 记忆质量如何评估。

迁移到 AI 学习助手：

```text
先做少量高价值记忆：学习目标、偏好、已学章节、薄弱点。
```

### Letta：看短期上下文和长期记忆如何分层

Letta 适合观察 Agent 如何把当前上下文和长期记忆分层处理。

本章只迁移一个点：

```text
长期记忆不是完整上下文，它只是未来任务需要召回的关键信息。
```

迁移到个人助手：

- 当前任务上下文用于完成眼前任务。
- 长期记忆用于跨会话个性化。
- 用户应该知道系统记住了什么。

### LangGraph：看 State 如何驱动执行

LangGraph 适合观察 State。

它提醒我们：

```text
状态是执行控制的一部分，不是记忆系统的替代品。
```

迁移到 AI 学习助手：

- `current_step`、`plan_version`、`tool_result` 属于 State。
- `preferred_learning_style`、`weak_points` 属于 Memory。
- 执行日志属于 Log。

## 项目锚点

AI 学习助手第一版可以设计三层数据：

| 层 | 保存什么 | 示例 |
| --- | --- | --- |
| State | 当前任务进度 | 当前步骤、计划版本、工具结果 |
| Memory | 跨会话高价值信息 | 学习目标、偏好、薄弱点 |
| Log | 执行过程和调试证据 | 工具调用、错误、停止原因 |

建议第一版长期记忆只保存四类：

| 类型 | 示例 | 写入规则 |
| --- | --- | --- |
| learning_goal | 两周内学会 RAG | 用户确认后保存 |
| preference | 喜欢项目驱动学习 | 用户确认后保存 |
| progress | 已完成第 7 章 | 来自明确任务结果 |
| weak_point | 无答案处理容易错 | 来自练习结果，允许修改和删除 |

不要保存：

- 用户完整聊天记录。
- 敏感身份信息。
- 未确认的心理画像。
- 一次性工具结果。

## 运行示例

第 13 章示例不调用真实模型，也不写入磁盘。

它用一个内存里的 Memory Store 演示写入、拒绝写入、检索和删除。

从仓库根目录运行：

```powershell
python .\examples\memory-state\memory_state.py --case learning-goal
python .\examples\memory-state\memory_state.py --case learning-goal --confirm-memory
python .\examples\memory-state\memory_state.py --case weak-point --confirm-memory
python .\examples\memory-state\memory_state.py --case sensitive
python .\examples\memory-state\memory_state.py --case retrieve
python .\examples\memory-state\memory_state.py --case delete-memory
python .\examples\memory-state\memory_state.py --case retrieve --json
```

你要观察：

- 没有确认时，学习目标不会直接写入长期记忆。
- 用户确认后，偏好或目标才保存。
- 敏感信息会被拒绝写入。
- 检索只返回和当前任务相关的记忆。
- 用户可以删除记忆。

## 动手任务

完成下面 4 件事：

1. 填写 [state-schema-template.md](./state-schema-template.md)。
2. 填写 [memory-policy-template.md](./memory-policy-template.md)。
3. 运行 [memory_state.py](../../examples/memory-state/memory_state.py) 的写入、拒绝、检索和删除场景。
4. 为你的项目列出 3 条“绝不默认保存”的信息。

## 检查题

先自己判断，再看参考答案。

| 问题 | 你的判断 |
| --- | --- |
| State 和 Memory 的核心区别是什么？ |  |
| 为什么不能把所有聊天记录都当成长期记忆？ |  |
| 一条长期记忆至少应该包含哪些字段？ |  |
| 什么信息不应该默认保存？ |  |
| 为什么用户必须能查看和删除记忆？ |  |

参考答案：

| 问题 | 参考判断 |
| --- | --- |
| State 推进当前任务，Memory 影响未来任务 |
| 因为聊天记录里有大量临时、无关、敏感或未验证信息，会增加风险和噪声 |
| 至少包含 id、type、content、source、scope、confidence、created_at、user_visible、deletable |
| 敏感信息、完整聊天记录、未验证推测、一次性工具结果、用户未确认的隐私内容 |
| 因为长期记忆会影响未来回答，用户需要控制系统记住了什么 |

## 本章小结

这一章你把 Agent 的信息管理分成了三层：

```text
State：当前任务怎么继续
Log：发生过什么
Memory：未来任务应该记住什么
```

你现在应该已经有：

- 一份 State Schema。
- 一份 Memory Policy。
- 至少四类可保存记忆。
- 至少三类禁止保存信息。
- 一条查看和删除记忆的路径。

下一章会进入 Multi-Agent，多 Agent 协作时更需要明确哪些状态共享、哪些记忆私有、哪些信息只能通过交接文档传递。

## 上一章 / 下一章

- 上一章：[第 12 章：Planning 任务拆解与计划执行](../12-planning-and-task-decomposition/README.md)
- 下一章：[第 14 章：Multi-Agent 多智能体协作](../14-multi-agent-collaboration/README.md)
