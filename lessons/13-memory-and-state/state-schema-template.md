# State Schema 模板

对应章节：[第 13 章：Memory 与 State](./README.md)

用途：定义当前任务运行时需要的状态字段。State 只服务当前任务推进，不等于长期记忆。

## 任务信息

| 项目 | 内容 |
| --- | --- |
| 项目名称 |  |
| 当前任务目标 |  |
| 任务开始条件 |  |
| 任务停止条件 |  |

## State 字段

| 字段 | 类型 | 示例值 | 谁写入 | 谁读取 | 是否持久化 |
| --- | --- | --- | --- | --- | --- |
| goal | string | 两周内学会 RAG | 用户 / Planner | Planner / Executor | 否 |
| current_step | string | generate_practice | Agent loop | Executor | 否 |
| plan_version | number | 2 | Planner | Reviewer | 否 |
| last_tool_result | object | 检索结果 | Tool runner | Reviewer | 否 |
| stop_reason | string | max_steps_reached | Reviewer | 用户 / 日志 | 可选 |

## 状态更新规则

| 事件 | 更新字段 | 更新规则 |
| --- | --- | --- |
| 工具调用成功 |  |  |
| 工具调用失败 |  |  |
| 用户修改目标 |  |  |
| 计划重规划 |  |  |
| 任务完成 |  |  |

## 不进入 State 的信息

| 信息 | 原因 | 应该放哪里 |
| --- | --- | --- |
| 完整聊天记录 | 噪声太多 | Log 或摘要 |
| 长期学习偏好 | 会影响未来任务 | Memory |
| 敏感信息 | 不应保存 | 不保存或立即脱敏 |
