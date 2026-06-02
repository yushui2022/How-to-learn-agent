# Memory Policy 模板

对应章节：[第 13 章：Memory 与 State](./README.md)

用途：定义什么信息可以写入长期记忆、是否需要确认、如何检索、如何更新和删除。

## 可保存记忆类型

| 类型 | 示例 | 来源 | 是否需要用户确认 | 过期或更新规则 |
| --- | --- | --- | --- | --- |
| learning_goal | 两周内学会 RAG | 用户明确表达 | 是 | 用户修改目标时更新 |
| preference | 喜欢项目驱动学习 | 用户确认 | 是 | 用户修改偏好时更新 |
| progress | 已完成第 7 章 | 任务执行结果 | 可选 | 学习进度变化时更新 |
| weak_point | 无答案处理容易错 | 练习结果 | 可选 | 后续练习通过后降低权重 |

## 禁止默认保存

| 信息 | 处理方式 |
| --- | --- |
| 密码、密钥、身份证、银行卡 | 不保存，必要时提醒用户不要提供 |
| 完整聊天记录 | 不作为长期记忆保存 |
| 未验证用户画像 | 不保存 |
| 一次性工具结果 | 放入 State 或 Log，不放入 Memory |
| 用户未确认的隐私内容 | 不保存 |

## 记忆记录字段

| 字段 | 说明 |
| --- | --- |
| id | 稳定标识 |
| type | preference / goal / progress / weak_point |
| content | 记忆内容 |
| source | user_confirmed / task_result / exercise_result |
| scope | 适用范围 |
| confidence | 可信度 |
| created_at | 创建时间 |
| expires_at | 过期时间 |
| user_visible | 是否对用户可见 |
| deletable | 是否允许删除 |

## 用户控制

| 能力 | 是否支持 | 说明 |
| --- | --- | --- |
| 查看记忆 |  |  |
| 删除记忆 |  |  |
| 修改记忆 |  |  |
| 关闭记忆 |  |  |
| 导出记忆 |  |  |
