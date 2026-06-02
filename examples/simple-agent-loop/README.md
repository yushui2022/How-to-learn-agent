# simple-agent-loop

对应章节：[第 11 章：Agent 执行循环与 ReAct](../../lessons/11-agent-loop-and-react/README.md)

这个示例不调用真实模型，而是用规则模拟一个最小 Agent loop：

```text
observe -> decision summary -> action -> result -> update state -> stop or continue
```

它的重点是执行轨迹、状态更新和停止条件。

## 运行

从仓库根目录运行：

```powershell
python .\examples\simple-agent-loop\simple_agent_loop.py --case success
python .\examples\simple-agent-loop\simple_agent_loop.py --case missing-notes
python .\examples\simple-agent-loop\simple_agent_loop.py --case tool-error
python .\examples\simple-agent-loop\simple_agent_loop.py --case looping-policy
python .\examples\simple-agent-loop\simple_agent_loop.py --case success --max-steps 2
python .\examples\simple-agent-loop\simple_agent_loop.py --case success --json
```

## 观察重点

- 每一步都从观察开始。
- 决策摘要说明为什么选择动作。
- 工具结果会更新状态。
- 达到最大步数时必须停止。
- 工具失败和资料缺失不能靠模型编造绕过去。
