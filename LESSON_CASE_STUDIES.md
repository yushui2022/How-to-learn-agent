# 每章成熟项目讲解索引

本文件把主线章节和成熟项目讲解统一起来。后续写正文时，作者不要重新随机挑项目，而应该先参考这张表，再进入对应章节和源码 Lab。

## 使用原则

- 每章至少有一个主案例，但只讲一个小切口。
- 源码 Lab 负责沉淀可复用的阅读任务，章节负责说明为什么本章需要读它。
- 同一个成熟项目可以多次出现，但每次讲解重点必须不同。
- Claude Code 这类闭源产品只能做产品行为标杆，不写成源码级案例。
- Star 数不写入正文，正式写作时只保留项目链接、定位、语言、协议和课程用途。

## 总表

| 章节 | 成熟项目主案例 | 对应 Lab | 本章讲解切口 | 迁移到项目 |
| --- | --- | --- | --- | --- |
| 00 课程准备与协作方式 | Microsoft AI Agents for Beginners, OpenClaw, mem0 | Lab 01, Lab 05 | README、目录、贡献入口、示例组织 | 统一课程仓库结构和协作规则 |
| 01 AI 项目到底在做什么 | OpenClaw, mem0 | Lab 01, Lab 05 | 产品型 AI 助手 vs 基础设施型记忆服务 | 判断项目类型和边界 |
| 02 从想法到 AI 原型 | OpenClaw, mem0 | Lab 03, Lab 05 | 从完整产品反推 MVP | 定义“AI 学习助手”第一版范围 |
| 03 第一次 LLM 调用 | LiteLLM | Lab 05 | 模型网关、统一接口、失败处理和成本记录 | 为最小调用预留可替换模型接口 |
| 04 Prompt Engineering 入门 | OpenClaw | Lab 03 | 用户意图如何转成任务目标和约束 | 让教学回答稳定、可控、可复用 |
| 05 上下文工程与结构化输出 | mem0, LangGraph | Lab 05, Lab 01 | 记忆输入输出、状态对象和结构化结果 | 输出结构化学习建议 |
| 06 AI 工作流 | LangGraph, Dify, Flowise | Lab 01, Lab 07 | 状态图、节点编排、低代码流程 | 先做可控工作流，再决定是否 Agent 化 |
| 07 RAG 基础 | Dify, OpenClaw | Lab 07 | 知识库接入、检索、引用和回答流程 | 接入课程资料或个人笔记 |
| 08 RAG 进阶与评估 | mem0, Dify | Lab 05, Lab 07 | 检索质量、回答质量、记忆质量分离 | 建立知识问答评估集 |
| 09 Tool Calling 工具调用 | OpenClaw, browser-use, SmolAgents | Lab 06, Lab 08 | 工具 Schema、参数校验、调用日志、权限 | 定义查询资料、生成练习、保存记录工具 |
| 10 Agent 到底是什么 | OpenClaw, LangGraph, SmolAgents | Lab 01, Lab 03, Lab 08 | 产品型 Agent、框架型 Agent、极简 Agent 边界 | 判断何时需要 Agent |
| 11 Agent 执行循环与 ReAct | LangGraph, OpenHands, SmolAgents | Lab 01, Lab 02, Lab 08 | observe-think-act、失败恢复、停止条件 | 做一次可追踪工具循环 |
| 12 Planning 任务拆解与计划执行 | LangGraph, AutoGen, CrewAI | Lab 01, Lab 04 | Planner、Executor、Reviewer 和重规划 | 拆解“学会 RAG”等长期任务 |
| 13 Memory 与 State | mem0, Letta, LangGraph | Lab 05, Lab 03 | 长期记忆、会话状态、检索、更新、删除 | 记住学习目标、进度和薄弱点 |
| 14 Multi-Agent 多智能体协作 | CrewAI, MetaGPT, AutoGen | Lab 04 | 角色、任务、消息交接、审阅机制 | 用研究写作 Agent 验证多角色流程 |
| 15 Agent Evaluation 评估方法 | mem0, AutoGen, LiteLLM, OpenHands | Lab 05, Lab 04, Lab 02 | 任务成功率、记忆质量、工具调用和成本 | 建立学习建议质量评估集 |
| 16 Observability 观测与调试 | LangGraph, LiteLLM, OpenClaw, OpenHands | Lab 01, Lab 02, Lab 05 | trace、日志、状态变化、失败复现 | 保存完整执行轨迹 |
| 17 Security 与 Trust | OpenClaw, browser-use, OpenHands | Lab 06, Lab 02 | 权限、沙箱、高风险动作和人工确认 | 限制记忆、资料访问和工具执行 |
| 18 Production 上线、成本与迭代 | OpenClaw, mem0, LiteLLM, LangGraph, Dify, SGLang | Lab 01, Lab 05, Lab 07 | 部署、模型网关、记忆服务、状态化执行、成本 | 形成可演示、可评估、可迭代的项目闭环 |

## 写正文时怎么用

每章正文建议使用下面的内部结构：

```text
1. 本章问题：为什么读者需要这个概念
2. 最小例子：先用自己的项目跑通一个简单版本
3. 成熟项目讲解：看真实项目如何处理同类问题
4. 项目迁移：把成熟项目里的一个小设计迁移回自己的项目
5. 学习任务：留下一个可检查的项目资产
```

成熟项目讲解不能变成项目广告，也不能变成源码逐行翻译。它应该回答：这个项目为什么这样设计，这个设计解决了什么问题，初学者应该学哪一小块，哪些复杂度现在不要照搬。
