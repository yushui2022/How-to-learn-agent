# local-rag

对应章节：[第 7 章：RAG 基础](../../lessons/07-rag-basics/README.md)

这个示例用本地 Markdown 文档跑通最小 RAG 链路：

```text
load docs -> split chunks -> retrieve -> build grounded answer with citations
```

它不依赖向量数据库，也不调用外部模型。目标是先看懂 RAG 流程。

## 运行

从仓库根目录运行：

```powershell
python .\examples\local-rag\local_rag.py --question "RAG 是让模型记住资料吗？" --show-scores
python .\examples\local-rag\local_rag.py --question "工作流和 Agent 的区别是什么？" --show-scores
python .\examples\local-rag\local_rag.py --question "怎么写 Prompt？" --show-scores
```

查看检索上下文：

```powershell
python .\examples\local-rag\local_rag.py --question "结构化输出有什么用？" --show-context
```

默认会过滤低于 `--min-score 2` 的弱相关片段。你可以调低阈值观察结果数量如何变化：

```powershell
python .\examples\local-rag\local_rag.py --question "结构化输出有什么用？" --min-score 1 --show-scores
```

## 观察重点

- 问题命中了哪些文档。
- 回答是否保留引用来源。
- 检索不到资料时，系统是否拒绝编造。
- 本地关键词检索有什么局限。
