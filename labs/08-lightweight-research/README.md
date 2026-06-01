# Lab 08：轻量入门与研究级 Agent

> 状态：planned

## Lab 定位

本 Lab 用小型、可读性强的项目帮助读者理解 Agent 的最小实现，而不是直接进入大型框架。

## 对应章节

- 第 09 章：Tool Calling 工具调用
- 第 10 章：Agent 到底是什么
- 第 11 章：Agent 执行循环与 ReAct

## 推荐项目

- 主案例：[SmolAgents](https://github.com/huggingface/smolagents)
- 主案例：[Mini-Agent](https://github.com/MiniMax-AI/Mini-Agent)

## 承接主线

读者刚进入 Agent 时，需要一个能看懂的最小实现。本 Lab 用轻量项目解释工具调用、代码执行、ReAct 循环和错误恢复。

## 学习任务

- 任务 1：找到一个最小 Agent loop，标出 observe、think、act、verify。
- 任务 2：写出工具调用的参数 schema 和返回结果格式。
- 任务 3：让“AI 学习助手”完成一个两步任务，例如检索资料后生成学习计划。

## 项目迁移

把能力迁移到“AI 学习助手”：先实现一个可读、可调试的 Agent loop，再考虑引入大型框架。

## 产出标准

- 一张 Agent loop 图。
- 一个最小工具调用示例。
- 一份失败复盘记录。

## 写作边界

不要因为项目轻量就忽略评估、日志和安全。轻量实现更适合展示原理，但不能默认生产可用。

