"""Evaluate the local RAG retriever from lesson 07.

The evaluation checks retrieval only. It intentionally separates retrieval
quality from final answer quality so beginners can locate failures.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any


EXAMPLES_DIR = Path(__file__).resolve().parents[1]
LOCAL_RAG_PATH = EXAMPLES_DIR / "local-rag" / "local_rag.py"
DOCS_DIR = EXAMPLES_DIR / "local-rag" / "docs"


@dataclass(frozen=True)
class EvalCase:
    question: str
    expected_sources: tuple[str, ...]
    case_type: str


EVAL_CASES = [
    EvalCase(
        question="RAG 是让模型记住资料吗？",
        expected_sources=("rag-basics.md",),
        case_type="direct-hit",
    ),
    EvalCase(
        question="工作流和 Agent 的区别是什么？",
        expected_sources=("ai-workflow.md",),
        case_type="concept-diff",
    ),
    EvalCase(
        question="怎么写 Prompt？",
        expected_sources=("prompt-engineering.md",),
        case_type="direct-hit",
    ),
    EvalCase(
        question="结构化输出有什么用？",
        expected_sources=("structured-output.md",),
        case_type="cross-lesson",
    ),
    EvalCase(
        question="天气预报怎么查？",
        expected_sources=(),
        case_type="no-answer",
    ),
]


def load_local_rag() -> ModuleType:
    spec = importlib.util.spec_from_file_location("local_rag", LOCAL_RAG_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {LOCAL_RAG_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def evaluate_case(
    *,
    local_rag: ModuleType,
    case: EvalCase,
    top_k: int,
    min_score: int,
) -> dict[str, Any]:
    chunks = local_rag.load_chunks(DOCS_DIR)
    results = local_rag.retrieve(case.question, chunks, top_k, min_score)
    actual_sources = tuple(dict.fromkeys(item.chunk.source for item in results))

    if case.case_type == "no-answer":
        passed = len(actual_sources) == 0
    else:
        passed = all(source in actual_sources for source in case.expected_sources)

    return {
        "question": case.question,
        "case_type": case.case_type,
        "expected_sources": list(case.expected_sources) or ["NONE"],
        "actual_sources": list(actual_sources) or ["NONE"],
        "passed": passed,
        "top_scores": [
            {
                "source": item.chunk.source,
                "chunk_id": item.chunk.chunk_id,
                "score": item.score,
            }
            for item in results
        ],
    }


def run_eval(top_k: int, min_score: int) -> dict[str, Any]:
    local_rag = load_local_rag()
    rows = [
        evaluate_case(
            local_rag=local_rag,
            case=case,
            top_k=top_k,
            min_score=min_score,
        )
        for case in EVAL_CASES
    ]
    passed = sum(1 for row in rows if row["passed"])
    return {
        "top_k": top_k,
        "min_score": min_score,
        "passed": passed,
        "total": len(rows),
        "pass_rate": round(passed / len(rows), 3),
        "rows": rows,
    }


def print_text_report(report: dict[str, Any]) -> None:
    print(
        f"RAG retrieval evaluation: {report['passed']}/{report['total']} "
        f"passed, pass_rate={report['pass_rate']}"
    )
    print(f"Config: top_k={report['top_k']}, min_score={report['min_score']}")
    print()

    for index, row in enumerate(report["rows"], start=1):
        status = "PASS" if row["passed"] else "FAIL"
        print(f"{index}. [{status}] {row['question']}")
        print(f"   type: {row['case_type']}")
        print(f"   expected: {', '.join(row['expected_sources'])}")
        print(f"   actual: {', '.join(row['actual_sources'])}")
        if row["top_scores"]:
            scores = ", ".join(
                f"{item['chunk_id']}={item['score']}" for item in row["top_scores"]
            )
            print(f"   scores: {scores}")
        print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate local RAG retrieval.")
    parser.add_argument("--top-k", type=int, default=2)
    parser.add_argument("--min-score", type=int, default=2)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = run_eval(top_k=args.top_k, min_score=args.min_score)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text_report(report)
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
