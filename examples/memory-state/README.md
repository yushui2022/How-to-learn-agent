# memory-state

对应章节：[第 13 章：Memory 与 State](../../lessons/13-memory-and-state/README.md)

这个示例不调用真实模型，也不写入磁盘。它用一个内存里的 Memory Store 演示：

```text
state update -> memory decision -> optional confirmation -> write / skip / retrieve / delete
```

## 运行

从仓库根目录运行：

```powershell
python .\examples\memory-state\memory_state.py --case learning-goal
python .\examples\memory-state\memory_state.py --case learning-goal --confirm-memory
python .\examples\memory-state\memory_state.py --case weak-point --confirm-memory
python .\examples\memory-state\memory_state.py --case sensitive
python .\examples\memory-state\memory_state.py --case retrieve
python .\examples\memory-state\memory_state.py --case delete-memory
python .\examples\memory-state\memory_state.py --case retrieve --json
```

## 观察重点

- State 只服务当前任务。
- Memory 会影响未来任务，所以写入要克制。
- 需要确认的记忆不能自动保存。
- 敏感信息默认拒绝写入。
- 用户应该能查看和删除记忆。
