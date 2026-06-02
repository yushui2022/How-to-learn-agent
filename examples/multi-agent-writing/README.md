# multi-agent-writing

对应章节：[第 14 章：Multi-Agent 多智能体协作](../../lessons/14-multi-agent-collaboration/README.md)

这个示例不调用真实模型，而是用规则模拟三角色协作：

```text
Researcher -> Writer -> Reviewer -> pass / revise / stop
```

它的重点是角色边界、交接消息、证据审阅和最大修订轮次。

## 运行

从仓库根目录运行：

```powershell
python .\examples\multi-agent-writing\multi_agent_writing.py --case happy-path
python .\examples\multi-agent-writing\multi_agent_writing.py --case missing-source
python .\examples\multi-agent-writing\multi_agent_writing.py --case needs-revision
python .\examples\multi-agent-writing\multi_agent_writing.py --case needs-revision --max-rounds 0
python .\examples\multi-agent-writing\multi_agent_writing.py --case needs-revision --json
```

## 观察重点

- Researcher 只交付研究笔记，不写最终文章。
- Writer 只基于研究笔记写草稿。
- Reviewer 检查结论是否有证据支持。
- 最大修订轮次会阻止无限来回。
