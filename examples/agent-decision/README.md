# agent-decision

对应章节：[第 10 章：Agent 到底是什么](../../lessons/10-agent-fundamentals/README.md)

这个示例不调用真实模型，而是用一组场景练习判断：

```text
Chatbot / Workflow / RAG / Tool Calling / Agent
```

它的目的不是给需求打一个绝对分数，而是帮助你看清：

- 下一步是否固定。
- 是否需要状态。
- 是否需要根据反馈继续行动。
- 是否存在副作用和权限风险。

## 运行

从仓库根目录运行：

```powershell
python .\examples\agent-decision\agent_decision.py --list
python .\examples\agent-decision\agent_decision.py --case chat-answer
python .\examples\agent-decision\agent_decision.py --case rag-answer
python .\examples\agent-decision\agent_decision.py --case fixed-workflow
python .\examples\agent-decision\agent_decision.py --case tool-app --show-checklist
python .\examples\agent-decision\agent_decision.py --case study-agent --show-checklist
python .\examples\agent-decision\agent_decision.py --case browser-action --show-checklist
```

## 观察重点

- 能调用工具不等于 Agent。
- 固定步骤优先用 Workflow。
- 主要问题是资料不足时优先用 RAG。
- 需要动态选择下一步、维护状态、根据反馈循环时，才进入 Agent 候选。
- 有副作用的 Agent 必须设置确认、最大步数和人工接管条件。
