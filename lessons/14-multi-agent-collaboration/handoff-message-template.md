# 交接消息模板

对应章节：[第 14 章：Multi-Agent 多智能体协作](./README.md)

用途：定义 Agent 之间传递交付物的消息格式，避免只靠模糊对话协作。

## 消息字段

| 字段 | 内容 |
| --- | --- |
| task_id |  |
| sender |  |
| receiver |  |
| artifact_type | research_notes / draft / review_report |
| status | ready / needs_revision / blocked |
| content |  |
| evidence |  |
| open_questions |  |
| requested_action |  |

## 示例

```json
{
  "task_id": "rag-eval-brief",
  "sender": "Researcher",
  "receiver": "Writer",
  "artifact_type": "research_notes",
  "status": "ready",
  "content": "RAG 评估需要拆分检索质量、回答质量和引用质量。",
  "evidence": ["lesson-08-rag-evaluation"],
  "open_questions": ["是否需要加入记忆质量评估"],
  "requested_action": "基于证据写一段简短说明"
}
```

## Reviewer 检查项

| 检查项 | 通过标准 |
| --- | --- |
| 是否有明确 evidence |  |
| content 是否回答任务 |  |
| open_questions 是否被保留 |  |
| requested_action 是否明确 |  |
| 是否需要修订 |  |
