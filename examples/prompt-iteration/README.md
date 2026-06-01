# prompt-iteration

对应章节：[第 4 章：Prompt Engineering 入门](../../lessons/04-prompt-engineering/README.md)

这个示例对比两种 Prompt：

- `loose`：只告诉模型“你是学习助手，回答问题”。
- `structured`：明确角色、任务、约束和输出要求。

目标是让读者看到：Prompt Engineering 不是复制神奇话术，而是用固定样例比较任务说明是否更稳定。

## dry-run

从仓库根目录运行：

```powershell
python .\examples\prompt-iteration\prompt_iteration.py --dry-run --variant both
```

只查看 structured Prompt：

```powershell
python .\examples\prompt-iteration\prompt_iteration.py --dry-run --variant structured --question "帮我学会所有 AI"
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
python .\examples\prompt-iteration\prompt_iteration.py --variant both --question "什么是 RAG？"
```

## 观察重点

- loose Prompt 是否漏掉“常见误区”或“下一步练习”。
- structured Prompt 是否更稳定地包含三个部分。
- 面对“帮我学会所有 AI”这种过大请求时，模型是否先澄清。
- Prompt 变长后是否真的解决了失败点。
