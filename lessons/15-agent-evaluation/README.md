# 第 15 章：Agent Evaluation 评估方法

> 状态：drafting

到这里，我们已经做过：

- RAG。
- Tool Calling。
- Agent loop。
- Planning。
- Memory。
- Multi-Agent。

这些能力一多，最危险的问题就来了：

```text
它看起来会做很多事，但到底有没有做对？
```

只看几个 demo 输出不够。

Agent 评估要同时看最终结果和执行过程。

本章只讲一个原则：

```text
评估不是问“看起来怎么样”，而是用固定任务反复检查“是否真的完成目标”。
```

本章回答三个问题：

- Agent 评估和普通回答评估有什么不同？
- 如何同时评估最终输出、工具调用、记忆写入、成本和安全？
- LLM-as-judge 能用在哪里，不能用在哪里？

学完本章，你要留下三份项目资产：

- 一份 Agent 评估集：[agent-evaluation-set-template.md](./agent-evaluation-set-template.md)
- 一份评估运行记录：[agent-evaluation-run-template.md](./agent-evaluation-run-template.md)
- 一个可运行示例：[agent_evaluation.py](../../examples/agent-evaluation/agent_evaluation.py)

## Agent 不能只评估最终回答

普通 LLM 应用经常只看：

```text
回答好不好？
```

Agent 不够。

因为 Agent 可能：

- 最终回答看起来对，但调用了错误工具。
- 回答正确，但写入了不该写的记忆。
- 任务完成了，但成本过高。
- 引用了资料，但引用不支持结论。
- 多 Agent 给出结论，但 Reviewer 没有真正检查证据。

所以 Agent 至少要看 5 层：

| 层 | 要评估什么 |
| --- | --- |
| Task | 用户目标是否完成 |
| Output | 最终输出是否正确、可用、可解释 |
| Process | 执行步骤是否合理，是否正确停止 |
| Tools / Memory | 工具调用和记忆写入是否正确 |
| Cost / Safety | 成本、延迟、权限和风险是否可接受 |

第 8 章评估的是 RAG。

本章评估的是完整 Agent 任务。

## 固定任务集是起点

不要每次随便试几个新问题。

先准备一组固定任务，每次修改 Prompt、工具、记忆策略或 Planner 后都重跑。

AI 学习助手的第一版评估集可以包含：

| 类型 | 任务 |
| --- | --- |
| 概念解释 | 解释 RAG 和普通问答的区别 |
| RAG 检索 | 基于第 7 章资料回答问题并引用来源 |
| 工具调用 | 生成练习，但不能自动保存记录 |
| Agent loop | 查询资料、生成练习、检查答案后停止 |
| Planning | 把“两周学会 RAG”拆成 4 到 6 步 |
| Memory | 记住学习偏好，但拒绝保存敏感信息 |
| Multi-Agent | 研究员、写作者、审阅者完成一段带证据说明 |
| 安全边界 | 请求删除记录时必须确认 |
| 无答案处理 | 资料不足时停止，不编造 |
| 成本限制 | 最大工具调用次数不能超过阈值 |

测试集不需要一开始很大。

先用 10 条固定任务，比 100 条随手测试更有价值。

## 每个任务都要写预期

评估任务不能只写：

```text
用户问 RAG 是什么。
```

要写清楚预期：

| 字段 | 示例 |
| --- | --- |
| task_id | `rag_no_answer_01` |
| user_input | `课程里有没有讲天气查询？` |
| expected_result | 说明资料不足，不编造 |
| expected_tools | `search_course_notes` |
| forbidden_tools | `save_learning_record` |
| expected_memory | 不写入长期记忆 |
| max_steps | 3 |
| max_cost | 0.02 |
| pass_criteria | 拒答、说明原因、没有写入记忆 |

有了这些字段，评估才不会变成主观感觉。

## 评分要分层

不要只给一个总分。

更实用的是分层评分：

| 维度 | 评分问题 |
| --- | --- |
| task_success | 任务是否完成 |
| output_quality | 最终回答是否正确、可读、基于证据 |
| process_quality | 步骤是否合理，是否按条件停止 |
| tool_quality | 工具是否调用正确，参数是否合理 |
| memory_quality | 是否正确写入、拒绝或检索记忆 |
| safety_quality | 是否拦截高风险动作 |
| cost_quality | 步数、工具调用次数、模型成本是否在限制内 |

最终可以归成三类：

| 结果 | 含义 |
| --- | --- |
| pass | 主要目标完成，关键边界通过 |
| partial | 结果有用，但有过程、工具或成本问题 |
| fail | 目标失败、越权、编造或关键证据缺失 |

partial 很重要。

很多 Agent 不是完全失败，而是“结果能用，但过程不可接受”。

## 失败分类比总分更重要

每次失败都要分类。

常见失败类型：

| 类型 | 表现 |
| --- | --- |
| retrieval_failure | 没找到应该找到的资料 |
| answer_hallucination | 资料不足仍然编造 |
| tool_misuse | 调错工具、参数错、重复调用 |
| memory_error | 写入了不该写的记忆，或该记没记 |
| planning_error | 计划步骤不可执行或过度拆解 |
| reviewer_miss | Reviewer 没发现证据不足 |
| stop_error | 没有停止，或过早停止 |
| safety_violation | 执行了需要确认的高风险动作 |
| cost_overrun | 超过工具调用、步数或成本限制 |

这比一句“效果不好”更有用。

因为不同失败需要不同修复方式。

## LLM-as-judge 怎么用

LLM-as-judge 可以用，但不能当绝对裁判。

适合让模型辅助判断：

- 回答是否覆盖用户问题。
- 文风是否清楚。
- 摘要是否保留重点。
- Reviewer 报告是否指出证据问题。

不适合完全交给模型判断：

- 工具是否真的调用了。
- 成本是否超限。
- 是否写入了敏感记忆。
- 是否访问了不该访问的权限。
- 测试是否真的通过。

这些要用日志、规则、测试或人工检查。

一个稳妥做法：

```text
规则检查硬边界
人工或 LLM-as-judge 检查内容质量
失败分类必须可追溯到执行记录
```

## 成熟项目观察：mem0、AutoGen、LiteLLM 和 OpenHands

本章主案例是 [mem0](https://github.com/mem0ai/mem0)，对比案例是 [AutoGen](https://github.com/microsoft/autogen)、[LiteLLM](https://github.com/BerriAI/litellm) 和 [OpenHands](https://github.com/OpenHands/OpenHands)。

对应源码 Lab：

- [Lab 05：记忆、推理与模型服务专项](../../labs/05-memory-reasoning/README.md)
- [Lab 04：多智能体协作](../../labs/04-multi-agent/README.md)
- [Lab 02：编程 Agent](../../labs/02-coding-agents/README.md)

### mem0：看记忆质量

记忆系统不只要评估“有没有记住”。

还要评估：

- 是否记住了应该保存的信息。
- 是否拒绝了不该保存的信息。
- 检索出来的记忆是否相关。
- 旧记忆是否会误导新任务。
- 用户能否查看和删除记忆。

迁移到 AI 学习助手：

```text
记忆评估至少包含：偏好保存、薄弱点保存、敏感信息拒绝、删除后不再检索。
```

### AutoGen：看多 Agent 任务结果

多 Agent 评估不能只看最终答案。

还要看：

- 角色是否按职责工作。
- 交接消息是否包含证据。
- Reviewer 是否发现问题。
- 最大轮次是否生效。

迁移到研究写作 Agent：

```text
草稿通过不代表协作成功，Reviewer 必须证明结论有证据支持。
```

### LiteLLM：看调用日志和成本

模型网关类项目适合观察调用记录、模型切换、成本和失败处理。

本章只迁移一个点：

```text
评估结果里要有成本和调用次数。
```

生产使用任何模型网关前，都要核验当前版本、安全公告和部署配置。

### OpenHands：看可执行任务的外部验证

编程 Agent 的评估更直接：

- 测试是否通过。
- 文件修改是否符合需求。
- 命令是否在沙箱里运行。
- 失败后是否停止或请求用户。

迁移到代码仓库助手：

```text
最终回答不是证据，测试结果、diff 和命令日志才是证据。
```

## 项目锚点

AI 学习助手在本章建立第一版评估集。

先做 10 个固定任务：

| 类型 | 评估重点 |
| --- | --- |
| 概念解释 | 回答是否清楚 |
| RAG 问答 | 是否引用正确资料 |
| 无答案问题 | 是否拒绝编造 |
| 工具调用 | 是否只调用允许工具 |
| 写入确认 | 是否拦截未确认写入 |
| Agent loop | 是否按最大步数停止 |
| Planning | 计划是否可执行 |
| Memory | 是否正确保存或拒绝记忆 |
| Multi-Agent | Reviewer 是否发现证据问题 |
| 成本限制 | 工具调用次数是否超限 |

每次改系统后都跑同一组任务。

这样才知道系统是真的变好，还是只是某几个 demo 变好。

## 运行示例

第 15 章示例不调用真实模型。

它用几条 mock Agent run 演示如何按规则评分和分类失败。

从仓库根目录运行：

```powershell
python .\examples\agent-evaluation\agent_evaluation.py --case all
python .\examples\agent-evaluation\agent_evaluation.py --case rag-success
python .\examples\agent-evaluation\agent_evaluation.py --case tool-overuse
python .\examples\agent-evaluation\agent_evaluation.py --case unsafe-memory
python .\examples\agent-evaluation\agent_evaluation.py --case unsafe-memory --json
```

你要观察：

- `rag-success` 为什么通过。
- `tool-overuse` 为什么最终回答有用但只能算 partial。
- `unsafe-memory` 为什么直接 fail。
- 评估输出如何给出失败类型。

## 动手任务

完成下面 4 件事：

1. 填写 [agent-evaluation-set-template.md](./agent-evaluation-set-template.md)。
2. 运行 [agent_evaluation.py](../../examples/agent-evaluation/agent_evaluation.py)。
3. 把一次运行结果记录到 [agent-evaluation-run-template.md](./agent-evaluation-run-template.md)。
4. 为你的项目写出至少 5 个失败类型。

## 检查题

先自己判断，再看参考答案。

| 问题 | 你的判断 |
| --- | --- |
| Agent 为什么不能只评估最终回答？ |  |
| 固定评估集有什么作用？ |  |
| LLM-as-judge 适合评估什么，不适合评估什么？ |  |
| partial 结果为什么重要？ |  |
| 失败分类为什么比总分更有用？ |  |

参考答案：

| 问题 | 参考判断 |
| --- | --- |
| Agent 为什么不能只评估最终回答？ | 因为 Agent 的工具、记忆、计划、成本和权限过程都可能出问题 |
| 固定评估集有什么作用？ | 让每次改动可以比较，避免只凭新 demo 感觉判断 |
| LLM-as-judge 适合评估什么，不适合评估什么？ | 适合辅助评估内容质量；不适合判断真实工具调用、成本、权限和测试结果 |
| partial 结果为什么重要？ | 因为很多结果表面可用，但过程、工具或安全边界有问题 |
| 失败分类为什么比总分更有用？ | 因为不同失败类型对应不同修复方式 |

## 本章小结

这一章你把 Agent 从“能跑”推进到“能评估”。

你现在应该已经有：

- 一组固定 Agent 评估任务。
- 每个任务的预期工具、记忆和停止条件。
- 一套分层评分方式。
- 一张失败类型表。
- 一份评估运行记录。

下一章会继续讲 Observability：评估告诉我们有没有问题，观测和调试帮助我们找到问题在哪里。

## 上一章 / 下一章

- 上一章：[第 14 章：Multi-Agent 多智能体协作](../14-multi-agent-collaboration/README.md)
- 下一章：[第 16 章：Observability 观测与调试](../16-observability-and-debugging/README.md)
