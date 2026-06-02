# plan-and-execute

对应章节：[第 12 章：Planning 任务拆解与计划执行](../../lessons/12-planning-and-task-decomposition/README.md)

这个示例不调用真实模型，而是用规则模拟：

```text
Planner -> Executor -> Reviewer -> continue / replan / stop
```

它的重点是计划版本、执行证据、重规划原因和停止条件。

## 运行

从仓库根目录运行：

```powershell
python .\examples\plan-and-execute\plan_and_execute.py --case happy-path
python .\examples\plan-and-execute\plan_and_execute.py --case retrieval-fails
python .\examples\plan-and-execute\plan_and_execute.py --case user-change
python .\examples\plan-and-execute\plan_and_execute.py --case happy-path --max-steps 3
python .\examples\plan-and-execute\plan_and_execute.py --case user-change --json
```

## 观察重点

- 计划步骤必须有 owner、动作、输出和通过标准。
- Executor 每一步都要产出证据。
- Reviewer 根据证据决定继续、重规划或停止。
- 资料缺失和用户目标变化都应该触发重规划。
- 最大步数会阻止计划无限执行。
