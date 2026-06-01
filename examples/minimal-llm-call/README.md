# minimal-llm-call

对应章节：[第 3 章：第一次 LLM 调用](../../lessons/03-first-llm-call/README.md)

这个示例用 Python 标准库完成一次 OpenAI-compatible Chat Completions 调用，不依赖第三方包。它的目标不是封装生产级 SDK，而是让读者看清一次模型调用的基本结构。

## 先 dry-run

从仓库根目录运行：

```powershell
python .\examples\minimal-llm-call\minimal_llm_call.py --dry-run
```

dry-run 只打印请求，不会访问网络，也不需要 API Key。

## 配置环境变量

PowerShell 示例：

```powershell
$env:LLM_API_KEY="你的 API Key"
$env:LLM_MODEL="你账号可用的模型名"
$env:LLM_BASE_URL="https://api.openai.com/v1"
```

也可以复制 `.env.example` 到本地 `.env` 做记录，但本脚本不会自动读取 `.env`。不要把真实 API Key 提交到仓库。

## 真实调用

```powershell
python .\examples\minimal-llm-call\minimal_llm_call.py --question "什么是 RAG？"
```

调整参数：

```powershell
python .\examples\minimal-llm-call\minimal_llm_call.py --question "什么是 RAG？" --temperature 0.8 --max-tokens 600
```

## 你应该观察什么

- 请求里有哪些 messages。
- temperature 改变后输出是否更发散。
- max tokens 是否影响输出完整性。
- 服务是否返回 usage 信息。
- 调用失败时错误发生在配置、网络、鉴权、额度还是请求格式。
