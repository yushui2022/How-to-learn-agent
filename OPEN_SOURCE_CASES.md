# 开源案例库

本课程需要产学研结合：章节不能只讲概念，也要拆解真实开源项目，把工程实现、研究脉络和产业场景连起来。

## 使用方式

每个章节作者在正式写作时，至少选择一个相关开源项目作为“成熟项目讲解”的对象。观察不等于照抄实现，而是回答：

- 这个项目解决了什么真实问题？
- 它背后对应哪个研究概念或工程模式？
- 它有哪些值得学习的架构设计？
- 它有哪些不适合初学者直接照搬的复杂度？
- 本章读者能从这个项目中完成什么小任务？

正式章节中不要只放“延伸阅读链接”。成熟项目讲解必须写清楚主案例、讲解切口、对应源码 Lab 和如何迁移回本章项目任务。

## 采纳原则

引入开源案例时按三类处理：

- 源码级主案例：源码开放、维护活跃、架构和章节知识点高度相关，可以进入正式章节或源码 Lab。
- 对比案例：适合做历史、架构或产品对比，但不一定作为主线实现参考。
- 产品标杆：行业影响力强，但闭源或源码不可完整阅读，只分析公开文档和可观察行为。

课程不在正文中追逐实时 Star 数。Star 数变化快，容易造成过时信息；正式写作时只保留项目链接、协议、语言、定位和课程用途。

## 重点案例

| 开源项目 | 适合章节 | 适合观察什么 | 课程中的用法 |
| --- | --- | --- | --- |
| [OpenClaw](https://github.com/openclaw/openclaw) | 09, 10, 11, 14, 16, 17, 18 | 个人 AI 助手、跨渠道入口、技能系统、沙箱安全、守护进程和多 Agent 协作 | 作为“AI 学习助手”走向真实产品形态的参考案例 |
| [mem0](https://github.com/mem0ai/mem0) | 05, 07, 08, 13, 15, 16, 18 | 长期记忆、用户偏好、会话摘要、记忆评估、可部署记忆服务 | 作为 Memory 与 State 章节的核心开源案例 |
| [LangGraph](https://github.com/langchain-ai/langgraph) | 05, 06, 10, 11, 12, 13, 16, 18 | 状态图、可恢复 Agent、工作流和 Agent 的边界、human-in-the-loop、持久化执行 | 作为工作流到 Agent 过渡的工程案例 |
| [AutoGen](https://github.com/microsoft/autogen) | 12, 14, 15 | 多 Agent 对话、角色协作、任务拆解、协作评估 | 作为 Multi-Agent 章节的对比案例 |
| [CrewAI](https://github.com/crewAIInc/crewAI) | 12, 14 | 角色、任务、流程编排、多 Agent 应用构建 | 作为 Multi-Agent 编排的对比案例 |
| [LiteLLM](https://github.com/BerriAI/litellm) | 03, 15, 16, 18 | 模型网关、成本、日志、限流、模型切换和生产化代理层 | 作为生产化章节的工程基础设施案例 |
| [OpenHands](https://github.com/All-Hands-AI/OpenHands) | 09, 11, 12, 15, 16, 17 | 编程 Agent、仓库上下文、命令执行、文件编辑、沙箱和人在回路 | 作为“代码仓库助手”和编程 Agent Lab 的主案例 |
| [browser-use](https://github.com/browser-use/browser-use) | 09, 11, 17 | 浏览器动作、页面状态、工具调用、安全确认和失败恢复 | 作为浏览器工具自动化 Lab 的主案例 |

## 八类案例池

这些项目按课程角色分为三档：

- 主线：应该进入正式章节。
- 重点 Lab：适合做源码阅读或项目拆解练习。
- 候选观察：适合放入延伸阅读，正式写作前需要再次核验仓库状态、协议和源码质量。
- 产品标杆：适合做行业对照，不写成源码级课程。

| 类别 | 项目 | 课程角色 | 适合放在哪里 |
| --- | --- | --- | --- |
| 通用核心框架 | OpenClaw | 主线 | 第 09-11、14、16-18 章 |
| 通用核心框架 | LangChain / LangGraph | 主线 | 第 06、10-13、16、18 章 |
| 通用核心框架 | AutoGPT | 重点 Lab | 第 10-11 章，自主 Agent 历史案例 |
| 通用核心框架 | Hermes Agent | 重点 Lab | Lab 01，团队级 Agent 底座和长期记忆、技能学习的进阶观察 |
| 编程 Agent | Claude Code | 产品标杆 | 闭源，不做源码课；适合作为第 18 章和 Lab 02 的产品行为标杆 |
| 编程 Agent | OpenHands | 重点 Lab | 第 09、11-12、15-17 章，软件工程 Agent；使用 `All-Hands-AI/OpenHands` 作为主链接 |
| 编程 Agent | Aider | 重点 Lab | 第 09、11、16 章，轻量命令行编程 Agent |
| 编程 Agent | Goose | 重点 Lab | Lab 02，企业编程 Agent、扩展工具和本地执行 |
| 个人助手 / 数字分身 | OpenClaw | 主线 | 贯穿“AI 学习助手”的产品化参考 |
| 个人助手 / 数字分身 | Letta / MemGPT | 重点 Lab | 第 13 章，长期记忆 Agent |
| 个人助手 / 数字分身 | OpenHuman | 重点 Lab | Lab 03，个人数据、记忆和数字分身边界 |
| 多智能体协作 | AutoGen | 对比案例 | 第 12、14、15 章；适合讲多 Agent 历史和架构，正式写作时注明维护状态 |
| 多智能体协作 | CrewAI | 主线 | 第 12、14 章 |
| 多智能体协作 | MetaGPT | 重点 Lab | 第 14 章，软件公司式角色协作 |
| 记忆 / 推理 / 模型服务专项 | mem0 | 主线 | 第 13、15、16、18 章 |
| 记忆 / 推理 / 模型服务专项 | Letta | 重点 Lab | 第 13 章，分层记忆和 Agent 状态 |
| 记忆 / 推理 / 模型服务专项 | LiteLLM | 重点 Lab | 第 03、15、16、18 章，模型网关、调用日志、成本和模型切换 |
| 记忆 / 推理 / 模型服务专项 | SGLang | 重点 Lab | 第 18 章，推理引擎、缓存、吞吐和成本优化 |
| 记忆 / 推理 / 模型服务专项 | EverOS | 候选观察 | Lab 05，个性化记忆系统；进入正文前需要再做源码切口核验 |
| 浏览器 / 工具自动化 | browser-use | 重点 Lab | 第 09、11、17 章，浏览器工具与安全边界 |
| 浏览器 / 工具自动化 | OpenClaw Skills / MCP | 主线 | 第 09、17 章，工具协议和权限 |
| 低代码 / 无代码 | Dify | 重点 Lab | 第 06、07、18 章，工作流、RAG 和部署 |
| 低代码 / 无代码 | Flowise | 重点 Lab | 第 06 章，低代码原型和节点式编排 |
| 轻量入门 / 研究级 | SmolAgents | 重点 Lab | 第 09-11 章，极简代码驱动 Agent |
| 轻量入门 / 研究级 | Mini-Agent | 重点 Lab | 第 09-11 章，极简 ReAct、MCP、Agent Skill 和工具链 |

## 章节映射

| 章节 | 推荐案例 | 结合方式 |
| --- | --- | --- |
| 00 课程准备与协作方式 | OpenClaw, mem0 | 观察成熟开源项目如何组织 README、文档、示例、安装方式和贡献入口 |
| 01 AI 项目到底在做什么 | OpenClaw, mem0 | 用它们说明 AI 项目既可以是产品，也可以是底层基础设施 |
| 02 从想法到 AI 原型 | OpenClaw | 反推一个个人 AI 助手从 MVP 到完整产品的范围控制 |
| 03 第一次 LLM 调用 | LiteLLM | 讨论为什么真实项目通常需要模型网关、日志和成本控制 |
| 04 Prompt Engineering 入门 | OpenClaw | 观察产品型 AI 助手如何把用户意图转成可执行任务 |
| 05 上下文工程与结构化输出 | mem0, LangGraph | 讨论上下文、状态和结构化结果如何进入后续流程 |
| 06 AI 工作流 | LangGraph | 用状态图说明工作流和 Agent 的边界 |
| 07 RAG 基础 | OpenClaw, 代码仓库助手项目 | 观察产品如何把外部资料接入回答流程 |
| 08 RAG 进阶与评估 | mem0, RAG 评估项目 | 把检索质量、回答质量和记忆质量区分开 |
| 09 Tool Calling 工具调用 | OpenClaw, LangGraph | 学习技能系统、工具定义、参数校验和调用日志 |
| 10 Agent 到底是什么 | OpenClaw, LangGraph | 对比产品型 Agent 和框架型 Agent 的边界 |
| 11 Agent 执行循环与 ReAct | LangGraph, OpenClaw | 观察 Agent loop、状态恢复和工具调用轨迹 |
| 12 Planning 任务拆解与计划执行 | LangGraph, AutoGen | 学习 Planner / Executor、多步骤任务和重新规划 |
| 13 Memory 与 State | mem0 | 作为核心案例，拆解长期记忆、偏好保存、记忆检索和清理 |
| 14 Multi-Agent 多智能体协作 | OpenClaw, AutoGen | 对比产品中的多角色协作和框架中的多 Agent 对话 |
| 15 Agent Evaluation 评估方法 | mem0, AutoGen, LiteLLM | 引入记忆评估、任务成功率、调用成本和回归测试 |
| 16 Observability 观测与调试 | OpenClaw, LangGraph, LiteLLM | 观察 trace、日志、工具调用记录和失败复现 |
| 17 Security 与 Trust | OpenClaw | 重点分析权限、沙箱、高风险工具和人工确认 |
| 18 Production 上线、成本与迭代 | OpenClaw, mem0, LiteLLM | 讨论从 demo 到服务化、部署、成本、监控和迭代 |

## 写作要求

每个开源案例都应该分成三层来写：

1. 产业场景：它解决什么真实用户或企业问题。
2. 研究概念：它对应 Agent、RAG、Memory、Planning、Multi-Agent、Evaluation 中的哪个问题。
3. 工程实现：它用什么结构、接口、日志、权限或部署方式解决问题。

这样读者不会只停留在“这个项目很厉害”，而是能知道这个项目和本章知识点的关系。
