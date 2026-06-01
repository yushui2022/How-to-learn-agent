# Lab 02：编程 Agent

> 状态：planned

## Lab 定位

本 Lab 关注编程 Agent 如何理解仓库、编辑文件、运行命令、处理 Git 上下文、调试失败并保持人工可控。

## 对应章节

- 第 09 章：Tool Calling 工具调用
- 第 11 章：Agent 执行循环与 ReAct
- 第 12 章：Planning 任务拆解与计划执行
- 第 15-18 章：评估、调试、安全和生产化

## 推荐项目

- 主案例：[OpenHands](https://github.com/All-Hands-AI/OpenHands)
- 主案例：[Aider](https://github.com/paul-gauthier/aider)
- 辅助案例：[Goose](https://github.com/block/goose)
- 产品标杆：[Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)

## 承接主线

读者已经理解工具调用和 Agent loop 后，再看编程 Agent 如何把“搜索、读取、编辑、测试、提交”变成受控行动链。

## 学习任务

- 任务 1：拆解一个编程 Agent 的仓库上下文来源，例如文件树、搜索结果、Git diff 或测试输出。
- 任务 2：记录一次“计划 -> 编辑 -> 验证 -> 修正”的执行轨迹。
- 任务 3：列出高风险工具，例如文件写入、命令执行、网络访问和凭据读取，并设计确认策略。

## 项目迁移

把能力迁移到“代码仓库助手”：先实现只读问答，再考虑受控修改建议，不让初学者过早进入全自动写代码。

## 产出标准

- 一份编程 Agent 行动链图。
- 一份工具权限清单。
- 一个最小代码仓库助手任务设计。

## 写作边界

Claude Code 是闭源产品标杆，只能分析公开文档和可观察行为，不能写成源码级案例。

