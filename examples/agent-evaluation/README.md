# agent-evaluation

对应章节：[第 15 章：Agent Evaluation 评估方法](../../lessons/15-agent-evaluation/README.md)

这个示例不调用真实模型，而是用几条 mock Agent run 演示分层评估：

```text
task -> output -> trace -> tools -> memory -> cost -> result
```

## 运行

从仓库根目录运行：

```powershell
python .\examples\agent-evaluation\agent_evaluation.py --case all
python .\examples\agent-evaluation\agent_evaluation.py --case rag-success
python .\examples\agent-evaluation\agent_evaluation.py --case tool-overuse
python .\examples\agent-evaluation\agent_evaluation.py --case unsafe-memory
python .\examples\agent-evaluation\agent_evaluation.py --case unsafe-memory --json
```

## 观察重点

- 最终回答通过，不代表工具和成本也通过。
- 写入敏感记忆应该直接失败。
- partial 结果用于标记“结果有用但过程有问题”。
- 失败类型比总分更能指导修复。
