# simple-workflow

对应章节：[第 6 章：AI 工作流](../../lessons/06-ai-workflows/README.md)

这个示例演示一个不依赖外部 API 的 AI 学习助手工作流。模型输出用 mock 数据模拟，重点是看清工作流结构：

```text
build_context -> generate_answer -> validate_output -> route_next_action -> render_result
```

## 运行三条路径

从仓库根目录运行：

```powershell
python .\examples\simple-workflow\simple_workflow.py --case good --show-trace
python .\examples\simple-workflow\simple_workflow.py --case clarify --show-trace
python .\examples\simple-workflow\simple_workflow.py --case invalid --show-trace
```

## 三条路径分别说明什么

| case | 含义 |
| --- | --- |
| good | 模型输出合法，直接展示回答和练习 |
| clarify | 用户问题太大，进入澄清分支 |
| invalid | 模型输出不合规，进入错误分支 |

## 观察重点

- State 在每个节点之间怎样变化。
- Trace 如何记录节点执行过程。
- 分支是由规则决定的，不是由 Agent 自主规划的。
- 工作流能覆盖稳定路径和失败路径。
