# Lab 06：浏览器与工具自动化

> 状态：planned

## Lab 定位

本 Lab 关注 Agent 如何操控浏览器和外部工具，以及如何处理权限、失败恢复、页面变化和安全边界。

## 对应章节

- 第 09 章：Tool Calling 工具调用
- 第 11 章：Agent 执行循环与 ReAct
- 第 17 章：Security 与 Trust

## 推荐项目

- 主案例：[browser-use](https://github.com/browser-use/browser-use)
- 主案例：[OpenClaw](https://github.com/openclaw/openclaw)
- 协议观察：[Model Context Protocol](https://modelcontextprotocol.io/)

## 承接主线

读者理解工具调用后，再看浏览器自动化。浏览器不是普通函数调用，它有页面状态、视觉变化、登录态、表单风险和外部副作用。

## 学习任务

- 任务 1：拆解一次浏览器任务的状态：目标页面、当前页面、可点击元素、已执行动作和失败原因。
- 任务 2：列出哪些动作需要人工确认，例如提交表单、购买、删除、发送消息。
- 任务 3：把浏览器工具调用记录成可复现的 trace。

## 项目迁移

把能力迁移到“研究写作 Agent”：只允许浏览器执行搜索和资料读取，不允许自动提交表单或执行不可逆动作。

## 产出标准

- 一份浏览器动作模型。
- 一份高风险动作清单。
- 一条可复现的工具调用 trace。

## 写作边界

不要把浏览器自动化写成万能 RPA。重点是状态、权限、失败恢复和可观测性。

