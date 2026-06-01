# 第 5 章：上下文工程与结构化输出

> 状态：drafting

第 4 章我们学会了把随意提问改成清楚的任务说明。

但真实项目里，只有 Prompt 还不够。模型还需要恰当的上下文，输出也要能被程序继续处理。

这一章解决两个问题：

```text
给模型什么信息？
让模型按什么结构返回？
```

本章回答三个问题：

- 上下文应该怎么选，而不是越塞越多？
- 怎样把模型输出设计成可校验的结构化对象？
- 输出不合规时，程序应该怎么处理？

学完本章，你要留下三份项目资产：

- 一份上下文包设计：[context-pack-template.md](./context-pack-template.md)
- 一份结构化输出设计：[structured-output-schema-template.md](./structured-output-schema-template.md)
- 一个可 dry-run、可本地校验的示例：[structured_output.py](../../examples/structured-output/structured_output.py)

## 先看问题

第 4 章的 AI 学习助手可以输出这样的回答：

```text
解释：RAG 是先检索资料，再基于资料回答。
常见误区：RAG 不是让模型记住所有知识。
下一步练习：找一段课程笔记，写出 3 个可检索问题。
```

这对人能读，但程序不好处理。

如果后续要把练习保存到数据库、展示到前端、交给评估脚本检查，就需要更稳定的结构：

```json
{
  "answer": {
    "explanation": "RAG 是先检索资料，再基于资料回答。",
    "misconception": "RAG 不是让模型记住所有知识。"
  },
  "exercise": {
    "task": "找一段课程笔记，写出 3 个可检索问题。",
    "duration_minutes": 10
  },
  "follow_up_needed": false,
  "follow_up_questions": []
}
```

这就是本章的目标：**让模型输出从“人能看”升级到“程序能用”**。

## 上下文不是越多越好

上下文是模型完成任务时能看到的信息。

很多初学者会把所有信息都塞进去：

```text
用户问题 + 课程大纲 + 所有历史聊天 + 项目说明 + 一堆无关规则
```

这通常会带来三个问题：

- 模型注意力被无关信息分散。
- 成本和延迟变高。
- 敏感信息更容易被误用。

更好的方式是先做一个“上下文包”。

AI 学习助手第一版的上下文包可以很小：

| 字段 | 示例 | 为什么需要 |
| --- | --- | --- |
| `user_question` | 什么是 RAG？ | 用户当前问题 |
| `learner_level` | beginner | 决定解释深度 |
| `course_stage` | 第 5 章：上下文与结构化输出 | 避免提前展开后续章节 |
| `known_terms` | LLM, Prompt | 避免重复解释已经学过的词 |
| `answer_policy` | 不假装读取外部资料 | 控制边界 |

它不是历史记录的堆积，而是一次任务真正需要的信息集合。

## 区分上下文、状态和记忆

这三个词很容易混在一起。

| 概念 | 含义 | AI 学习助手示例 |
| --- | --- | --- |
| 上下文 | 本次调用临时提供给模型的信息 | 当前问题、学习阶段、输出要求 |
| 状态 | 程序在流程中保存和传递的当前数据 | 当前处理到哪一步、校验是否通过 |
| 记忆 | 跨会话长期保存的信息 | 用户学习目标、薄弱点、已学章节 |

本章重点是上下文和结构化输出。

记忆会在第 13 章展开。现在不要把所有历史对话都叫记忆，也不要急着保存所有内容。

## 设计结构化输出

结构化输出的关键不是“让模型输出 JSON”这一句话。

你要先定义字段：

| 字段 | 类型 | 必填 | 含义 |
| --- | --- | --- | --- |
| `answer.explanation` | string | 是 | 概念解释 |
| `answer.misconception` | string | 是 | 常见误区 |
| `exercise.task` | string | 是 | 下一步练习 |
| `exercise.duration_minutes` | number | 是 | 练习预计耗时 |
| `follow_up_needed` | boolean | 是 | 是否需要先澄清 |
| `follow_up_questions` | string[] | 是 | 澄清问题列表 |

然后再把要求写进 Prompt：

```text
只输出合法 JSON，不要输出 Markdown。
必须包含 answer、exercise、follow_up_needed、follow_up_questions。
如果用户问题太大或太模糊，把 follow_up_needed 设为 true，并给出 1 到 3 个澄清问题。
```

注意：模型仍然可能输出错误格式。

所以结构化输出必须配合校验。

## 不要信任模型输出

即使 Prompt 写了“只输出 JSON”，模型也可能返回：

- JSON 前后带解释文字。
- 字段缺失。
- 字段类型错误。
- 数字变成字符串。
- 过大问题没有触发澄清。

程序应该至少做三类检查：

| 检查 | 示例 |
| --- | --- |
| 能不能解析 | `json.loads()` 是否成功 |
| 字段是否完整 | 是否包含 `answer.explanation` |
| 类型是否正确 | `follow_up_needed` 是否是 boolean |

本章示例 [structured_output.py](../../examples/structured-output/structured_output.py) 会做本地校验。即使没有 API Key，你也可以先跑 mock 数据：

```powershell
python .\examples\structured-output\structured_output.py --mock good
python .\examples\structured-output\structured_output.py --mock bad
```

## 失败后怎么办

输出不合规时，不要立刻崩溃。

常见处理方式有四种：

| 方式 | 什么时候用 |
| --- | --- |
| 重试 | 解析失败、缺少字段，但任务本身清楚 |
| 修复 | 输出大体正确，只是 JSON 外面包了 Markdown |
| 澄清 | 用户问题太大或缺少关键信息 |
| 人工处理 | 高风险、反复失败、或结果会影响真实用户 |

第一版可以先做最简单的处理：

```text
解析失败 -> 打印错误 -> 保存原始输出 -> 人工查看
```

后面第 15 章和第 16 章会把这些失败记录接到评估和观测里。

## 成熟项目观察：mem0 和 LangGraph

本章的成熟项目主案例是 [mem0](https://github.com/mem0ai/mem0) 和 [LangGraph](https://github.com/langchain-ai/langgraph)。

对应源码 Lab：

- [Lab 05：记忆、推理与模型服务专项](../../labs/05-memory-reasoning/README.md)
- [Lab 01：通用核心框架](../../labs/01-core-frameworks/README.md)

这里不要求读源码细节，只观察两个工程习惯。

### mem0：不是所有上下文都应该变成记忆

记忆系统最重要的问题不是“能不能保存”，而是：

```text
什么值得保存？
什么时候检索？
什么时候更新或删除？
```

迁移到 AI 学习助手：

- 当前问题属于本次上下文。
- “用户正在学第 5 章”可以是短期状态。
- “用户长期薄弱点是上下文工程”未来才可能进入记忆。

第一版不要把所有输入输出都长期保存。

### LangGraph：状态要有结构，才能在流程中流转

工作流或 Agent 不是只传一段文本。

它们通常会传递一个状态对象，例如：

```json
{
  "question": "什么是 RAG？",
  "draft_answer": {},
  "validation_errors": [],
  "next_step": "validate"
}
```

迁移到 AI 学习助手：

```text
模型输出不是终点，而是后续保存、校验、展示、评估的输入。
```

所以本章先把回答变成结构化对象，为第 6 章工作流做准备。

## 项目锚点

AI 学习助手在本章要从“稳定回答”升级到“可解析回答”。

其他项目也可以这样拆：

| 项目 | 结构化输出 |
| --- | --- |
| 研究写作 Agent | 研究问题、搜索关键词、预期证据、优先级 |
| 客服工单 Agent | 问题类型、紧急程度、建议处理人、置信度 |
| 代码仓库助手 | 项目用途、核心目录、建议阅读顺序、未知点 |

每个项目都要回答：

```text
后续程序要用模型输出里的哪些字段？
```

## 动手任务

完成下面 4 件事：

1. 填写 [context-pack-template.md](./context-pack-template.md)。
2. 填写 [structured-output-schema-template.md](./structured-output-schema-template.md)。
3. 运行结构化输出示例的 dry-run。
4. 用 mock 数据测试本地校验逻辑。

命令：

```powershell
python .\examples\structured-output\structured_output.py --dry-run
python .\examples\structured-output\structured_output.py --mock good
python .\examples\structured-output\structured_output.py --mock bad
```

如果已经配置第 3 章的环境变量，可以真实调用：

```powershell
python .\examples\structured-output\structured_output.py --question "什么是 RAG？"
```

## 检查题

先自己判断，再看参考答案。

| 问题 | 你的判断 |
| --- | --- |
| 上下文是不是越多越好？ |  |
| 只要求“输出 JSON”是否足够？ |  |
| 为什么结构化输出还要做校验？ |  |
| 当前问题、状态、长期记忆有什么区别？ |  |

参考答案：

| 问题 | 参考判断 |
| --- | --- |
| 不是。上下文要和当前任务相关，过多会增加噪声、成本和风险 |
| 不够。还要定义字段、类型、必填项和失败处理 |
| 模型可能输出非法 JSON、缺字段或类型错误，程序不能盲信 |
| 当前问题是本次上下文；状态是流程中传递的数据；记忆是跨会话长期保存的信息 |

## 本章小结

这一章你完成了两次升级：

```text
随意上下文 -> 任务相关上下文包
自然语言回答 -> 可校验结构化对象
```

你现在应该已经有：

- 一份上下文包设计。
- 一份结构化输出字段说明。
- 一个能校验输出的最小脚本。
- 对上下文、状态、记忆的基本区分。

下一章会把这些结构化结果接入确定流程，开始学习 AI 工作流。

## 上一章 / 下一章

- 上一章：[第 4 章：Prompt Engineering 入门](../04-prompt-engineering/README.md)
- 下一章：[第 6 章：AI 工作流](../06-ai-workflows/README.md)
