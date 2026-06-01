# Lab 04：多智能体协作

> 状态：planned

## Lab 定位

本 Lab 关注多个 Agent 如何分工、通信、交接任务、汇总结果和避免互相放大错误。

## 对应章节

- 第 12 章：Planning 任务拆解与计划执行
- 第 14 章：Multi-Agent 多智能体协作
- 第 15 章：Agent Evaluation 评估方法

## 推荐项目

- 主案例：[CrewAI](https://github.com/crewAIInc/crewAI)
- 主案例：[MetaGPT](https://github.com/geekan/MetaGPT)
- 历史与架构案例：[AutoGen](https://github.com/microsoft/autogen)

## 承接主线

读者先学会单 Agent 的计划和执行，再进入多 Agent。多 Agent 不是“多几个角色名”，而是任务边界、消息协议和结果评估。

## 学习任务

- 任务 1：把一个复杂任务拆成 2-3 个角色，说明每个角色的输入、输出和停止条件。
- 任务 2：观察一个多 Agent 框架如何表达任务、角色和上下文传递。
- 任务 3：设计一个防止错误传递的检查点，例如人工确认、独立评审或自动测试。

## 项目迁移

把能力迁移到“研究写作 Agent”：研究员负责检索，写作者负责组织内容，审阅者负责发现引用和事实问题。

## 产出标准

- 一张角色分工表。
- 一张消息流或任务流图。
- 一份多 Agent 评估清单。

## 写作边界

不要为了展示多 Agent 而强行多 Agent。小任务应该先用单 Agent 或工作流解决。

