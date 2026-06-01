# Lab 01：通用核心框架

> 状态：planned

## Lab 定位

本 Lab 用来拆解通用 Agent 框架如何组织模型、工具、状态、会话、执行流和插件能力。

## 对应章节

- 第 06 章：AI 工作流
- 第 09 章：Tool Calling 工具调用
- 第 10-13 章：Agent、ReAct、Planning、Memory
- 第 16-18 章：观测、调试和生产化

## 推荐项目

- 主案例：[OpenClaw](https://github.com/openclaw/openclaw)
- 主案例：[LangGraph](https://github.com/langchain-ai/langgraph)
- 历史案例：[AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)
- 进阶候选：[Hermes Agent](https://github.com/NousResearch/hermes-agent)

## 承接主线

读者学完工作流、工具调用和 Agent loop 后，再来看这些框架如何把概念组合成真实系统。不要一开始就要求读者读完整仓库。

## 学习任务

- 任务 1：画出一个框架的核心模块图，只保留模型、工具、状态、执行器和日志。
- 任务 2：找到一个工具注册或插件注册入口，记录输入参数、权限边界和调用结果。
- 任务 3：比较框架型 Agent 和产品型 Agent 的差异。

## 项目迁移

把观察结果迁移到“AI 学习助手”：只选择一个能力引入项目，例如工具注册表、状态对象或执行日志，不复制完整框架。

## 产出标准

- 一张模块关系图。
- 一段源码阅读笔记。
- 一个可以合入项目主线的小设计决策。

## 写作边界

不要写成“哪个框架最好”的排名，也不要要求读者一次性掌握大型框架全部源码。

