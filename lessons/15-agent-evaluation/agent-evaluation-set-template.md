# Agent 评估集模板

对应章节：[第 15 章：Agent Evaluation 评估方法](./README.md)

用途：固定一组任务，用来比较每次 Prompt、工具、记忆或 Agent 逻辑改动后的效果。

## 评估任务

| task_id | user_input | expected_result | expected_tools | forbidden_tools | expected_memory | max_steps | max_cost | pass_criteria |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |

## 评分维度

| 维度 | 通过标准 |
| --- | --- |
| task_success |  |
| output_quality |  |
| process_quality |  |
| tool_quality |  |
| memory_quality |  |
| safety_quality |  |
| cost_quality |  |

## 失败类型

| failure_type | 定义 | 修复方向 |
| --- | --- | --- |
| retrieval_failure |  |  |
| tool_misuse |  |  |
| memory_error |  |  |
| planning_error |  |  |
| safety_violation |  |  |
| cost_overrun |  |  |
