# tool-calling

对应章节：[第 9 章：Tool Calling 工具调用](../../lessons/09-tool-calling/README.md)

这个示例不调用真实模型，而是用 mock 的“模型工具调用请求”演示工具调用链路：

```text
tool request -> schema validation -> permission check -> execute tool -> log trace
```

## 运行

从仓库根目录运行：

```powershell
python .\examples\tool-calling\tool_calling.py --case search --show-log
python .\examples\tool-calling\tool_calling.py --case practice --show-log
python .\examples\tool-calling\tool_calling.py --case invalid-args --show-log
python .\examples\tool-calling\tool_calling.py --case unknown-tool --show-log
python .\examples\tool-calling\tool_calling.py --case save-record --show-log
python .\examples\tool-calling\tool_calling.py --case save-record --confirm --show-log
```

## 观察重点

- 模型请求只是结构化数据，不是工具执行结果。
- 程序会拒绝未知工具。
- 程序会拒绝参数错误。
- 写入类工具需要确认。
- 每次调用都应该留下 trace。
