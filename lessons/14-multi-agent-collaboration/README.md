# 第 14 章：Multi-Agent 多智能体协作

> 状态：drafting

第 13 章我们把 State、Log 和 Memory 分清楚了。

进入多 Agent 后，这个问题会更明显：

```text
谁能看哪些状态？
谁能写哪些记忆？
谁把什么结果交给谁？
谁负责最后判断质量？
```

很多人第一次做多 Agent，会写成这样：

```text
创建 5 个角色。
让它们互相聊天。
希望最后结果更好。
```

这通常只会带来更多成本、更多延迟和更多不可控输出。

本章只讲一个原则：

```text
多 Agent 不是多个名字，而是多个职责边界。
```

本章回答三个问题：

- 什么时候真的需要多个 Agent？
- 如何设计角色职责、交接消息和审阅机制？
- 如何避免多 Agent 反复讨论、重复劳动和互相放大错误？

学完本章，你要留下三份项目资产：

- 一份角色卡：[role-card-template.md](./role-card-template.md)
- 一份交接消息模板：[handoff-message-template.md](./handoff-message-template.md)
- 一个可运行示例：[multi_agent_writing.py](../../examples/multi-agent-writing/multi_agent_writing.py)

## 先判断是否需要多 Agent

多 Agent 不是默认升级方向。

如果一个任务可以由单 Agent、工作流或普通工具调用稳定完成，就不要强行拆成多个 Agent。

适合多 Agent 的情况通常有这些：

| 情况 | 为什么可能需要多 Agent |
| --- | --- |
| 任务需要明显不同的专业视角 | 研究、写作、审阅的判断标准不同 |
| 需要独立检查 | Reviewer 不应该和 Writer 混在一起 |
| 工具权限不同 | 有的角色只能读资料，有的角色能写草稿 |
| 可以并行处理 | 多个资料源或多个子任务可以同时处理 |
| 单个上下文太复杂 | 拆角色能减少上下文混乱 |

不适合多 Agent 的情况：

| 情况 | 更适合什么 |
| --- | --- |
| 一次性问答 | LLM 调用或 RAG |
| 固定步骤流程 | 工作流 |
| 三步以内的短任务 | 单 Agent loop |
| 低延迟低成本任务 | 单 Agent 或工具调用 |
| 没有明确审阅标准 | 先定义评估标准 |

判断标准很简单：

```text
多一个 Agent，是否减少了真实复杂度？
```

如果只是多一个角色名，没有减少复杂度，就不要加。

## 角色名不是职责

角色名很容易写：

```text
研究员、写作者、审阅者。
```

但这还不够。

每个角色都要写清楚：

| 字段 | 要回答的问题 |
| --- | --- |
| Responsibility | 它只负责什么？ |
| Input | 它从谁那里接收什么？ |
| Output | 它必须交付什么可检查产物？ |
| Tools | 它能用哪些工具？ |
| State Access | 它能看哪些共享状态？ |
| Memory Access | 它能读写哪些长期记忆？ |
| Stop Condition | 它什么时候停止？ |
| Forbidden Actions | 它不能做什么？ |

例如研究员：

| 字段 | 内容 |
| --- | --- |
| Responsibility | 找资料并摘出支持问题的证据 |
| Input | 研究主题和资料范围 |
| Output | 带来源的研究笔记 |
| Tools | 搜索、读取资料 |
| Forbidden Actions | 不写最终文章，不编造来源 |

这样写，Writer 才知道自己能接什么，Reviewer 才知道应该审什么。

## 交接消息要结构化

多 Agent 之间不要只传一句自然语言：

```text
我查完了，你写吧。
```

这会让后续角色不知道资料是否充分、证据在哪里、还有什么风险。

更好的交接消息应该包含：

| 字段 | 说明 |
| --- | --- |
| sender | 谁发出 |
| receiver | 发给谁 |
| task_id | 对应哪个任务 |
| artifact_type | research_notes / draft / review_report |
| content | 主要内容 |
| evidence | 支持内容的证据 |
| open_questions | 还没解决的问题 |
| status | ready / needs_revision / blocked |

多 Agent 协作的核心不是“聊天”，而是“交付物交接”。

## 三种基础协作模式

初学阶段先掌握三种模式就够。

### 1. Pipeline

按顺序交接：

```text
Researcher -> Writer -> Reviewer -> Final
```

适合研究写作、报告生成、课程总结。

优点是结构清楚。

风险是前面错了，后面会继承错误。

### 2. Supervisor / Worker

一个 Supervisor 分配任务，多个 Worker 执行：

```text
Supervisor
-> Worker A
-> Worker B
-> Reviewer
```

适合可以拆分成多个独立子任务的场景。

风险是 Supervisor 需要清楚知道每个 Worker 的输入、输出和停止条件。

### 3. Reviewer Gate

Reviewer 作为质量闸门：

```text
Writer -> Reviewer
Reviewer -> pass / revise / stop
```

适合引用检查、事实检查、代码审查、测试结果审查。

风险是没有最大修订次数时，会反复来回。

第一版多 Agent 建议从 Pipeline + Reviewer Gate 开始。

## 共享状态和私有记忆

第 13 章讲过 State 和 Memory。

多 Agent 里要额外写清楚：

| 信息 | 谁能看 | 谁能写 |
| --- | --- | --- |
| 任务目标 | 所有角色 | Supervisor 或 Planner |
| 研究资料 | Researcher、Writer、Reviewer | Researcher |
| 草稿 | Writer、Reviewer | Writer |
| 审阅意见 | Writer、Supervisor | Reviewer |
| 用户长期偏好 | 需要时检索 | 记忆管理模块 |
| 工具执行日志 | 开发者、Reviewer | Tool runner |

不要让所有角色都读写所有东西。

权限越模糊，问题越难排查。

## 多 Agent 的常见失败

| 失败 | 表现 | 处理方式 |
| --- | --- | --- |
| 角色重叠 | Researcher 也写草稿，Writer 也查资料 | 写清角色边界 |
| 消息太散 | 后续角色不知道证据在哪里 | 使用交接消息模板 |
| 没有 Reviewer | 错误从上游传到最终输出 | 设置审阅闸门 |
| 无限讨论 | 反复要求修改，没有终止条件 | 设置最大轮次 |
| 成本失控 | 多个 Agent 都调用模型和工具 | 限制角色数量和工具 |
| 错误放大 | 一个错误来源被多个角色重复引用 | Reviewer 检查证据 |

多 Agent 的质量不是靠“人多”保证的。

质量来自清楚的输入、输出、审阅标准和退出条件。

## 成熟项目观察：CrewAI、MetaGPT 和 AutoGen

本章主案例是 [CrewAI](https://github.com/crewAIInc/crewAI) 和 [MetaGPT](https://github.com/geekan/MetaGPT)，对比案例是 [AutoGen](https://github.com/microsoft/autogen)。

对应源码 Lab：

- [Lab 04：多智能体协作](../../labs/04-multi-agent/README.md)

### CrewAI：角色必须绑定任务和产出

CrewAI 适合观察角色、任务和流程如何组织。

本章只迁移一个点：

```text
每个角色都必须有交付物。
```

不要只写：

```text
你是研究员。
```

要写：

```text
你负责输出带来源的研究笔记，不能写最终文章。
```

### MetaGPT：角色协作要靠文档交接

MetaGPT 适合观察软件公司式角色协作。

本章不要求读者复制完整复杂度，只看一个切口：

```text
不同角色之间用什么文档或产物交接？
```

迁移到研究写作 Agent：

- Researcher 交付研究笔记。
- Writer 交付带引用的草稿。
- Reviewer 交付审阅报告。

### AutoGen：多 Agent 对话需要边界

AutoGen 适合作为多 Agent 对话和协作模式的历史与架构案例。

观察它时要记住：

```text
Agent 能对话，不代表协作就可靠。
```

你仍然需要：

- 任务边界。
- 消息格式。
- 工具权限。
- 最大轮次。
- 人工接管条件。

## 项目锚点

本章主项目用“研究写作 Agent”。

目标：

```text
写一段关于 RAG 评估的简短研究说明。
```

第一版三角色：

| 角色 | 输入 | 输出 | 停止条件 |
| --- | --- | --- | --- |
| Researcher | 主题 | 带来源的研究笔记 | 找到足够证据或资料不足 |
| Writer | 研究笔记 | 带引用的草稿 | 草稿覆盖核心问题 |
| Reviewer | 草稿和研究笔记 | pass / revise / stop | 引用支持结论或达到最大修订次数 |

AI 学习助手也可以做多 Agent，但不要一开始就拆太多。

适合拆的情况：

- Planner 生成学习计划。
- Exercise Designer 生成练习。
- Reviewer 检查练习是否真的覆盖薄弱点。

不适合拆的情况：

- 解释一个概念。
- 查询一个课程问题。
- 生成一次练习。

这些用单 Agent 或工作流就够。

## 运行示例

第 14 章示例不调用真实模型。

它用规则模拟 Researcher、Writer、Reviewer 的交接。

从仓库根目录运行：

```powershell
python .\examples\multi-agent-writing\multi_agent_writing.py --case happy-path
python .\examples\multi-agent-writing\multi_agent_writing.py --case missing-source
python .\examples\multi-agent-writing\multi_agent_writing.py --case needs-revision
python .\examples\multi-agent-writing\multi_agent_writing.py --case needs-revision --max-rounds 0
python .\examples\multi-agent-writing\multi_agent_writing.py --case needs-revision --json
```

你要观察：

- `happy-path` 如何通过 Reviewer。
- `missing-source` 如何在资料不足时停止。
- `needs-revision` 如何由 Reviewer 要求 Writer 修订。
- `--max-rounds 0` 如何防止反复修订。

## 动手任务

完成下面 4 件事：

1. 填写 [role-card-template.md](./role-card-template.md)。
2. 填写 [handoff-message-template.md](./handoff-message-template.md)。
3. 运行 [multi_agent_writing.py](../../examples/multi-agent-writing/multi_agent_writing.py) 的三个场景。
4. 为你的项目写出一个“不需要多 Agent”的任务，并说明原因。

## 检查题

先自己判断，再看参考答案。

| 问题 | 你的判断 |
| --- | --- |
| 多 Agent 是否一定比单 Agent 更强？ |  |
| 角色卡至少要写清哪些内容？ |  |
| 为什么要用结构化交接消息？ |  |
| Reviewer 的作用是什么？ |  |
| 多 Agent 为什么需要最大轮次？ |  |

参考答案：

| 问题 | 参考判断 |
| --- | --- |
| 不一定。多 Agent 会增加成本、延迟和协调复杂度，只有职责边界清楚时才有价值 |
| 至少写清职责、输入、输出、工具、状态和记忆访问、停止条件、禁止动作 |
| 因为后续角色需要知道证据、状态、未解决问题和交付物类型 |
| 作为质量闸门，检查证据是否支持结论，并决定通过、修订或停止 |
| 防止 Writer 和 Reviewer 反复来回，造成成本失控和无限讨论 |

## 本章小结

这一章你学会了多 Agent 的基本判断：

```text
先有职责边界，再有多个 Agent。
```

你现在应该已经有：

- 一份角色卡。
- 一份交接消息模板。
- 一个三角色研究写作流程。
- 一个 Reviewer Gate。
- 一个最大修订轮次。
- 一个“不该多 Agent 化”的反例。

下一章会进入 Agent Evaluation，开始评估单 Agent 和多 Agent 到底有没有把任务做得更好。

## 上一章 / 下一章

- 上一章：[第 13 章：Memory 与 State](../13-memory-and-state/README.md)
- 下一章：[第 15 章：Agent Evaluation 评估方法](../15-agent-evaluation/README.md)
