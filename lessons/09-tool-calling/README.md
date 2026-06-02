# 第 9 章：Tool Calling 工具调用

> 状态：drafting

第 7-8 章我们让模型使用外部资料。

现在再往前走一步：让模型请求外部能力。

比如 AI 学习助手可能需要：

- 查询课程笔记。
- 生成练习任务。
- 保存学习记录。
- 查询用户学习进度。

这些都不是“多写几句 Prompt”能解决的。模型需要通过工具和外部系统交互。

本章只讲一个原则：

```text
模型不直接执行工具，应用程序负责校验、授权、执行和记录。
```

本章回答三个问题：

- Tool Calling 和普通文本生成有什么区别？
- 一个工具定义应该包含哪些字段？
- 如何处理参数错误、权限拒绝和工具执行失败？

学完本章，你要留下三份项目资产：

- 一份工具设计表：[tool-design-template.md](./tool-design-template.md)
- 一份工具调用日志：[tool-call-log-template.md](./tool-call-log-template.md)
- 一个可本地运行示例：[tool_calling.py](../../examples/tool-calling/tool_calling.py)

## 先看工具调用流程

工具调用不是模型“自己执行代码”。

更准确的流程是：

```text
用户提出问题
-> 模型判断需要工具
-> 模型输出工具名和参数
-> 应用程序校验参数
-> 应用程序检查权限
-> 应用程序执行工具
-> 工具结果返回给模型或直接返回用户
-> 记录完整调用日志
```

模型只负责提出请求。

真正执行工具的是你的程序。

## 文本回答和工具调用的区别

| 类型 | 模型输出 | 程序要做什么 |
| --- | --- | --- |
| 普通文本生成 | 一段自然语言回答 | 展示或解析 |
| 结构化输出 | JSON 对象 | 校验字段和类型 |
| Tool Calling | 工具名 + 参数 | 校验、授权、执行、记录 |

工具调用的风险更高，因为它可能产生副作用。

例如：

| 工具 | 是否有副作用 | 风险 |
| --- | --- | --- |
| 查询课程笔记 | 否 | 低 |
| 生成练习 | 否 | 低 |
| 保存学习记录 | 是 | 中 |
| 删除学习记录 | 是 | 高 |
| 自动发消息或提交表单 | 是 | 高 |

有副作用的工具必须更严格地校验和确认。

## 一个工具定义应该写清什么

第一版工具定义不需要复杂。

至少写清 6 件事：

| 字段 | 说明 |
| --- | --- |
| 工具名 | 模型要调用的稳定名称 |
| 用途 | 工具解决什么问题 |
| 参数 Schema | 参数名、类型、是否必填 |
| 返回结果 | 工具会返回什么结构 |
| 权限 | 是否只读，是否需要人工确认 |
| 失败情况 | 参数错误、无结果、权限不足、执行失败 |

AI 学习助手的 `search_course_notes` 可以这样定义：

```json
{
  "name": "search_course_notes",
  "description": "查询课程笔记，返回相关片段",
  "arguments": {
    "query": "string",
    "top_k": "number"
  },
  "permission": "read_only"
}
```

这不是给模型看的装饰文档，而是程序校验和执行工具的依据。

## 参数必须校验

不要相信模型给出的工具参数一定正确。

模型可能输出：

```json
{
  "tool": "search_course_notes",
  "arguments": {
    "top_k": "很多"
  }
}
```

这里缺少 `query`，`top_k` 也不是数字。

程序应该拒绝执行，并记录错误：

```text
tool_call rejected: missing query; top_k must be integer
```

参数校验至少包括：

- 工具是否存在。
- 必填参数是否完整。
- 参数类型是否正确。
- 参数值是否在允许范围内。
- 是否涉及高风险动作。

## 权限边界比“会调用”更重要

工具调用一旦接入真实系统，就会有风险。

本章先按三类处理：

| 权限类型 | 示例 | 处理方式 |
| --- | --- | --- |
| 只读工具 | 查询资料、读取状态 | 可以自动执行，但要记录日志 |
| 低风险写入 | 保存学习记录 | 需要明确规则，必要时确认 |
| 高风险动作 | 删除数据、发消息、付款、提交表单 | 默认禁止或人工确认 |

模型说“调用删除工具”不代表程序可以照做。

你的程序必须有自己的权限判断。

## 成熟项目观察：OpenClaw、browser-use 和 SmolAgents

本章主案例是 OpenClaw，对比案例是 [browser-use](https://github.com/browser-use/browser-use) 和 [SmolAgents](https://github.com/huggingface/smolagents)。

对应源码 Lab：

- [Lab 06：浏览器与工具自动化](../../labs/06-browser-tools/README.md)
- [Lab 08：轻量入门与研究级 Agent](../../labs/08-lightweight-research/README.md)

### OpenClaw：技能系统的关键不是“功能多”

观察个人助手的技能系统时，不要只数它有多少工具。

要看：

- 技能如何命名。
- 输入参数如何定义。
- 工具结果如何返回。
- 哪些动作需要权限控制。
- 调用过程如何记录。

迁移到 AI 学习助手：

```text
先定义 2 到 3 个受控工具，不要一开始开放所有能力。
```

### browser-use：浏览器工具风险更高

浏览器工具不是普通函数。

它可能点击按钮、填写表单、提交数据、触发真实业务动作。

所以浏览器类工具要额外关注：

- 当前页面状态。
- 动作是否可逆。
- 是否涉及登录态或隐私。
- 是否需要人工确认。

本章不做浏览器自动化，只提前建立安全意识。

### SmolAgents：轻量实现适合看清工具调用原理

轻量 Agent 项目的价值在于：你能看清工具列表、参数、执行结果和循环逻辑。

本章只迁移工具调用部分，不进入完整 Agent loop。

第 10-11 章再讨论 Agent。

## 项目锚点

AI 学习助手在本章可以先定义三个工具：

| 工具 | 用途 | 权限 |
| --- | --- | --- |
| `search_course_notes` | 查询课程笔记 | 只读 |
| `generate_practice` | 生成练习任务 | 只读 |
| `save_learning_record` | 保存学习记录 | 低风险写入，需要确认 |

其他项目也可以这样拆：

| 项目 | 工具 |
| --- | --- |
| 研究写作 Agent | 搜索资料、读取网页、保存摘要 |
| 客服工单 Agent | 查询订单、查询 FAQ、更新工单备注 |
| 代码仓库助手 | 搜索文件、读取文件、运行测试 |

每个工具都要先回答：

```text
这个工具是否有副作用？失败后怎么处理？需要谁确认？
```

## 动手任务

完成下面 4 件事：

1. 填写 [tool-design-template.md](./tool-design-template.md)。
2. 运行 [tool_calling.py](../../examples/tool-calling/tool_calling.py) 的正常路径、参数错误路径和权限拒绝路径。
3. 把运行结果写进 [tool-call-log-template.md](./tool-call-log-template.md)。
4. 为你的项目列出至少一个禁止自动执行的高风险工具。

运行示例：

```powershell
python .\examples\tool-calling\tool_calling.py --case search --show-log
python .\examples\tool-calling\tool_calling.py --case invalid-args --show-log
python .\examples\tool-calling\tool_calling.py --case save-record --show-log
python .\examples\tool-calling\tool_calling.py --case save-record --confirm --show-log
python .\examples\tool-calling\tool_calling.py --case unknown-tool --show-log
```

## 检查题

先自己判断，再看参考答案。

| 问题 | 你的判断 |
| --- | --- |
| 工具是模型执行的，还是应用程序执行的？ |  |
| 为什么工具参数必须校验？ |  |
| 只读工具和写入工具的权限要求一样吗？ |  |
| Tool Calling 是否已经等于 Agent？ |  |

参考答案：

| 问题 | 参考判断 |
| --- | --- |
| 应用程序执行。模型只提出工具调用请求 |
| 模型可能给错工具名、漏参数、传错类型或请求高风险动作 |
| 不一样。写入工具有副作用，通常需要更严格控制或确认 |
| 不等于。Tool Calling 是 Agent 的能力之一，但还没有自主循环和动态规划 |

## 本章小结

这一章你学会了受控工具调用的基本结构：

```text
工具定义 -> 模型请求 -> 参数校验 -> 权限判断 -> 程序执行 -> 调用日志
```

你现在应该已经有：

- 至少两个工具定义。
- 一份参数 Schema。
- 一条正常工具调用日志。
- 一条参数错误或权限拒绝日志。
- 一份高风险工具清单。

下一章会回答：当系统能使用工具后，什么情况下它才真正变成 Agent？

## 上一章 / 下一章

- 上一章：[第 8 章：RAG 进阶与评估](../08-rag-evaluation/README.md)
- 下一章：[第 10 章：Agent 到底是什么](../10-agent-fundamentals/README.md)
