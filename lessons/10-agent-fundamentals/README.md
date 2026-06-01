# 第 10 章：Agent 到底是什么

> 状态：planned

## 本章定位

在读者已经理解工作流、RAG 和工具调用后，再定义 Agent，避免把 Agent 讲成抽象口号。

## 承接上一章

上一章讲了工具调用，让模型具备了行动能力。本章解释什么时候这些能力组合起来才算 Agent。

## 铺垫下一章

下一章会讲 Agent 的执行循环。本章需要先明确 Agent 和 Chatbot、Workflow、RAG 应用的区别。

## 学习目标

- 能用工程语言解释什么是 Agent。
- 能区分 Chatbot、Workflow、RAG App 和 Agent。
- 能判断一个任务是否值得使用 Agent。

## 本章产出

- 一张能力阶梯图。
- 一份“是否需要 Agent”的判断清单。
- 三种实现方式的对比示例说明。

## 学习任务

- 用自己的项目分别描述普通 LLM 调用、工作流、RAG App 和 Agent 四种方案。
- 写一份“为什么现在需要或不需要 Agent”的决策说明。
- 找出项目里至少 2 个必须限制 Agent 自主性的地方。

## 项目锚点

“AI 学习助手”在本章决定是否从知识问答工具升级为 Agent。如果它只是回答问题，不需要 Agent；如果它要规划学习路径、调用工具、跟踪任务，才进入 Agent 阶段。

## 成熟项目讲解

- 主案例：OpenClaw、LangGraph。
- 对比案例：SmolAgents。
- 讲解切口：产品型 Agent、框架型 Agent 和极简 Agent 的边界。
- 对应源码 Lab：[Lab 01：通用核心框架](../../labs/01-core-frameworks/README.md)、[Lab 03：个人助手与数字分身](../../labs/03-personal-assistants/README.md)、[Lab 08：轻量入门与研究级 Agent](../../labs/08-lightweight-research/README.md)。
- 迁移到项目：判断“AI 学习助手”什么时候只是 RAG 应用，什么时候才需要 Agent。

## 开源案例观察

对比 OpenClaw 和 LangGraph：OpenClaw 更像面向用户的 Agent 产品，LangGraph 更像构建 Agent 的状态化工程框架。用它们帮助读者理解“产品”和“框架”的不同层次。

## 本章要写什么

- Agent 的工作定义。
- Chatbot、Workflow、RAG App、Agent 的区别。
- Agent 的适用场景和不适用场景。
- 自主性、工具、状态和反馈的关系。
- 为什么不要为了用 Agent 而用 Agent。

## 本章不要写什么

- 不要展开 Planning、Memory 或 Multi-Agent。
- 不要把某个框架的定义当成唯一标准。

## 小白易卡点

- 把任何会调用模型的系统都叫 Agent。
- 觉得 Agent 越自主越好。
- 不知道 Agent 的失败成本通常比普通工作流更高。

## 建议示例

对比同一个任务的三种实现：普通 LLM 调用、固定工作流、简单 Agent。

## 建议图解

画一张能力阶梯图：LLM 调用、Workflow、RAG、Tool Use、Agent。
