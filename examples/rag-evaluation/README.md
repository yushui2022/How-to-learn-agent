# rag-evaluation

对应章节：[第 8 章：RAG 进阶与评估](../../lessons/08-rag-evaluation/README.md)

这个示例复用第 7 章的本地知识库和检索逻辑，用固定测试集检查：

- 直接问题是否命中正确文档。
- 概念区分问题是否命中正确文档。
- 无答案问题是否不返回资料。

## 运行

从仓库根目录运行：

```powershell
python .\examples\rag-evaluation\rag_evaluation.py
```

比较不同参数：

```powershell
python .\examples\rag-evaluation\rag_evaluation.py --top-k 1
python .\examples\rag-evaluation\rag_evaluation.py --min-score 1
```

输出 JSON：

```powershell
python .\examples\rag-evaluation\rag_evaluation.py --format json
```

## 观察重点

- 哪些问题没有命中期望文档。
- 无答案问题是否返回空检索。
- 调整 `top_k` 和 `min_score` 后，检索通过率是否变化。
- 失败应该归类为文档问题、检索问题还是无答案策略问题。
