# 第 6 章：AI 工作流

> 状态：drafting

第 5 章我们已经能让模型输出一个可校验的结构化对象。

现在问题变成：

```text
这个对象接下来交给谁？
校验失败怎么办？
问题太大时要不要继续生成？
什么时候需要人工介入？
```

这就是 AI 工作流要解决的问题。

本章只讲一个判断：**很多 AI 应用应该先做成确定工作流，而不是一开始就做 Agent**。

本章回答三个问题：

- 工作流和 Agent 的区别是什么？
- 如何把模型调用、规则判断、校验和分支处理串起来？
- 成熟工作流框架和低代码平台给我们什么工程启发？

学完本章，你要留下三份项目资产：

- 一张工作流设计表：[workflow-design-template.md](./workflow-design-template.md)
- 一份运行记录：[workflow-run-log-template.md](./workflow-run-log-template.md)
- 一个可本地运行的示例：[simple_workflow.py](../../examples/simple-workflow/simple_workflow.py)

## 先看一个固定流程

AI 学习助手现在已经能返回结构化结果。

把它放进系统里，可以形成一个确定流程：

```text
接收问题
-> 构造上下文
-> 调用模型生成结构化结果
-> 校验输出
-> 如果需要澄清，就向用户追问
-> 如果校验通过，就展示回答并保存记录
-> 如果校验失败，就进入重试或人工处理
```

这个流程里，下一步基本是提前写好的。

这就是工作流。

## 工作流不是 Agent

工作流和 Agent 都可能有多个步骤，但关键差别不在“步骤多不多”。

关键差别是：

```text
下一步是谁决定的？
```

| 形态 | 下一步怎么决定 | 适合场景 |
| --- | --- | --- |
| 工作流 | 程序按预设规则决定 | 流程清楚、风险可控、需要稳定复现 |
| Agent | 系统根据目标、上下文和中间结果动态决定 | 路径不固定、需要探索、需要多次工具使用 |

AI 学习助手第一阶段适合工作流，因为我们已经知道流程：

```text
问题 -> 回答 -> 校验 -> 展示或澄清
```

它还不需要自主决定“下一步去哪里搜索、调用哪个工具、如何重新规划”。这些会在后面的 Agent 章节再讲。

## 工作流的 5 个组成部分

先掌握 5 个概念。

| 概念 | 含义 | AI 学习助手示例 |
| --- | --- | --- |
| State | 流程中不断传递的数据 | 问题、上下文、模型输出、校验错误 |
| Node | 一个处理步骤 | 构造上下文、校验输出、渲染回答 |
| Edge | 步骤之间的连接 | 校验通过后进入展示节点 |
| Condition | 分支条件 | 是否需要澄清、是否校验失败 |
| Trace | 执行轨迹 | 每一步输入、输出、耗时、错误 |

你可以把工作流想成：

```text
State 被一个个 Node 修改，Edge 决定 State 去下一个 Node。
```

## 用 State 串起流程

不要让每一步只传一段字符串。

更好的做法是维护一个状态对象：

```json
{
  "question": "什么是 RAG？",
  "context": {},
  "model_output": {},
  "validation_errors": [],
  "next_action": "",
  "trace": []
}
```

每个节点只负责修改其中一部分。

| 节点 | 读取 | 写入 |
| --- | --- | --- |
| `build_context` | `question` | `context` |
| `generate_answer` | `context` | `model_output` |
| `validate_output` | `model_output` | `validation_errors` |
| `route_next_action` | `validation_errors`, `model_output.follow_up_needed` | `next_action` |
| `render_result` | `next_action`, `model_output` | 最终展示文本 |

这样做的好处是：调试时能看到每一步到底改了什么。

## 设计分支

工作流不只是顺序执行，还要处理分支。

AI 学习助手至少有三条分支：

| 条件 | 下一步 |
| --- | --- |
| 输出合法，且不需要澄清 | 展示回答和练习 |
| 输出合法，但 `follow_up_needed=true` | 展示澄清问题 |
| 输出不合法 | 记录错误，进入重试或人工处理 |

这比“模型回答完就结束”可靠得多。

## 失败处理不是后话

工作流一开始就要设计失败处理。

| 失败类型 | 示例 | 第一版处理 |
| --- | --- | --- |
| 输入太大 | “帮我学会所有 AI” | 走澄清分支 |
| 输出格式错误 | JSON 缺字段 | 记录错误，提示重试 |
| 模型服务失败 | 超时、限流、鉴权失败 | 保存错误，返回可理解提示 |
| 高风险动作 | 删除数据、发消息、扣费 | 人工确认 |

第 6 章的重点不是让系统自动解决所有失败，而是让失败有路可走。

## 成熟项目观察：LangGraph、Dify 和 Flowise

本章主案例是 [LangGraph](https://github.com/langchain-ai/langgraph)，对比案例是 [Dify](https://github.com/langgenius/dify) 和 [Flowise](https://github.com/FlowiseAI/Flowise)。

对应源码 Lab：

- [Lab 01：通用核心框架](../../labs/01-core-frameworks/README.md)
- [Lab 07：低代码与无代码 Agent 平台](../../labs/07-low-code/README.md)

### LangGraph：用状态图表达可控流程

观察 LangGraph 时，先不要急着学完整 API。

本章只看一个思想：

```text
把复杂 AI 应用拆成状态、节点、边和条件分支。
```

迁移到 AI 学习助手：

- State 保存问题、上下文、结构化输出和校验结果。
- Node 分别负责构造上下文、调用模型、校验、分支、展示。
- Edge 控制下一步去哪里。

### Dify / Flowise：低代码节点背后也是工作流

低代码平台把流程画成节点和连线。

对初学者来说，它们的价值不是“可以不写代码”，而是帮助你看清：

- 哪一步是输入。
- 哪一步调用模型。
- 哪一步做条件判断。
- 哪一步接知识库或工具。
- 哪一步输出给用户。

迁移回代码时，也要能写出同样的流程，而不是只会拖节点。

## 项目锚点

AI 学习助手在本章要形成第一个确定工作流：

```text
question
-> context
-> structured output
-> validation
-> answer / clarification / error
```

其他项目也可以这样拆：

| 项目 | 工作流 |
| --- | --- |
| 研究写作 Agent | 主题输入 -> 拆搜索问题 -> 校验问题质量 -> 输出问题清单 |
| 客服工单 Agent | 工单输入 -> 分类 -> 判断紧急程度 -> 建议处理人 -> 人工确认 |
| 代码仓库助手 | README 输入 -> 提取用途 -> 识别核心目录 -> 给出阅读顺序 |

只要流程能提前画出来，就先做工作流。

## 动手任务

完成下面 4 件事：

1. 填写 [workflow-design-template.md](./workflow-design-template.md)。
2. 运行 [simple_workflow.py](../../examples/simple-workflow/simple_workflow.py) 的三条路径。
3. 把运行结果写进 [workflow-run-log-template.md](./workflow-run-log-template.md)。
4. 回答：你的项目现在是否真的需要 Agent？

运行示例：

```powershell
python .\examples\simple-workflow\simple_workflow.py --case good --show-trace
python .\examples\simple-workflow\simple_workflow.py --case clarify --show-trace
python .\examples\simple-workflow\simple_workflow.py --case invalid --show-trace
```

## 检查题

先自己判断，再看参考答案。

| 问题 | 你的判断 |
| --- | --- |
| 多步骤流程一定是 Agent 吗？ |  |
| 工作流里为什么要有 State？ |  |
| 输出校验失败时，为什么不能直接继续展示？ |  |
| 什么时候应该先做工作流，而不是 Agent？ |  |

参考答案：

| 问题 | 参考判断 |
| --- | --- |
| 不一定。关键看下一步是否由系统动态决策 |
| State 让每个节点能读写明确字段，方便调试和恢复 |
| 因为下游程序可能依赖字段，错误输出会扩大成系统错误 |
| 当步骤清楚、风险可控、流程需要稳定复现时，优先工作流 |

## 本章小结

这一章你把 AI 学习助手从“一次模型调用”升级成了确定工作流：

```text
输入 -> 上下文 -> 模型输出 -> 校验 -> 分支 -> 展示
```

你现在应该已经有：

- 一个工作流设计表。
- 一个状态对象设计。
- 三条分支路径：回答、澄清、错误。
- 一份运行 trace。

下一章会在这个工作流里加入外部资料，开始学习 RAG。

## 上一章 / 下一章

- 上一章：[第 5 章：上下文工程与结构化输出](../05-context-and-structured-output/README.md)
- 下一章：[第 7 章：RAG 基础](../07-rag-basics/README.md)
