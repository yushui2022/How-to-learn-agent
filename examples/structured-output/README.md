# structured-output

对应章节：[第 5 章：上下文工程与结构化输出](../../lessons/05-context-and-structured-output/README.md)

这个示例演示三件事：

- 如何把上下文包发送给模型。
- 如何要求模型返回 JSON。
- 如何在本地校验模型输出是否可被程序继续处理。

它使用 Python 标准库，不依赖第三方包。

## dry-run

从仓库根目录运行：

```powershell
python .\examples\structured-output\structured_output.py --dry-run
```

dry-run 会打印请求结构，不访问网络。

## 本地 mock 校验

不用 API Key 也可以先验证校验逻辑：

```powershell
python .\examples\structured-output\structured_output.py --mock good
python .\examples\structured-output\structured_output.py --mock bad
python .\examples\structured-output\structured_output.py --mock clarify
```

## 真实调用

先配置第 3 章使用过的环境变量：

```powershell
$env:LLM_API_KEY="你的 API Key"
$env:LLM_MODEL="你账号可用的模型名"
$env:LLM_BASE_URL="https://api.openai.com/v1"
```

然后运行：

```powershell
python .\examples\structured-output\structured_output.py --question "什么是 RAG？"
```

## 观察重点

- 模型是否返回合法 JSON。
- 必填字段是否完整。
- 字段类型是否正确。
- 过大问题是否触发 `follow_up_needed`。
- 校验失败时是否保存了原始输出和错误原因。
