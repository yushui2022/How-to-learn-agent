"""Minimal local RAG example for lesson 07.

This example intentionally uses simple keyword overlap instead of embeddings.
The goal is to make the RAG pipeline visible: load, chunk, retrieve, answer,
and cite sources.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


DOCS_DIR = Path(__file__).parent / "docs"


@dataclass(frozen=True)
class Chunk:
    source: str
    chunk_id: str
    text: str


@dataclass(frozen=True)
class ScoredChunk:
    chunk: Chunk
    score: int


def load_chunks(docs_dir: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(docs_dir.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        paragraphs = [item.strip() for item in re.split(r"\n\s*\n", content) if item.strip()]
        for index, paragraph in enumerate(paragraphs, start=1):
            if paragraph.startswith("# "):
                continue
            chunks.append(
                Chunk(
                    source=path.name,
                    chunk_id=f"{path.stem}#{index}",
                    text=paragraph,
                )
            )
    return chunks


def tokenize(text: str) -> set[str]:
    lower = text.lower()
    latin_terms = set(re.findall(r"[a-z0-9]+", lower))
    cjk_runs = re.findall(r"[\u4e00-\u9fff]+", lower)
    cjk_bigrams: set[str] = set()
    for run in cjk_runs:
        for index in range(len(run) - 1):
            bigram = run[index : index + 2]
            if bigram not in {"什么", "怎么", "可以", "应该"}:
                cjk_bigrams.add(bigram)
    return latin_terms | cjk_bigrams


def score_chunk(question_terms: set[str], chunk: Chunk) -> int:
    chunk_terms = tokenize(chunk.text + " " + chunk.source)
    overlap = question_terms & chunk_terms
    score = len(overlap)
    for term in question_terms:
        if term in chunk.source.lower():
            score += 2
    return score


def retrieve(
    question: str,
    chunks: list[Chunk],
    top_k: int,
    min_score: int,
) -> list[ScoredChunk]:
    question_terms = tokenize(question)
    scored = [
        ScoredChunk(chunk=chunk, score=score_chunk(question_terms, chunk))
        for chunk in chunks
    ]
    scored = [item for item in scored if item.score >= min_score]
    scored.sort(key=lambda item: item.score, reverse=True)
    return scored[:top_k]


def build_answer(question: str, results: list[ScoredChunk]) -> str:
    if not results:
        return (
            "资料库没有找到足够依据，建议补充资料或换个问题。\n"
            f"问题：{question}"
        )

    evidence_lines = [
        f"- [{item.chunk.chunk_id}] {item.chunk.text}"
        for item in results
    ]
    sources = ", ".join(
        f"{item.chunk.source}:{item.chunk.chunk_id}" for item in results
    )

    return (
        "基于检索资料，可以这样回答：\n\n"
        + "\n".join(evidence_lines)
        + "\n\n"
        "回答要点：请只根据上面的片段组织最终回答；如果片段不足以回答，说明资料不足。\n"
        f"引用来源：{sources}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a minimal local RAG demo.")
    parser.add_argument("--question", default="RAG 是让模型记住资料吗？")
    parser.add_argument("--top-k", type=int, default=2)
    parser.add_argument("--min-score", type=int, default=2)
    parser.add_argument("--show-scores", action="store_true")
    parser.add_argument("--show-context", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    chunks = load_chunks(DOCS_DIR)
    results = retrieve(args.question, chunks, args.top_k, args.min_score)

    if args.show_scores:
        print("Scores:")
        for item in results:
            print(f"- {item.chunk.chunk_id}: {item.score}")
        if not results:
            print("- no matching chunks")
        print()

    if args.show_context:
        print("Retrieved context:")
        for item in results:
            print(f"\n[{item.chunk.chunk_id}]\n{item.chunk.text}")
        if not results:
            print("- empty")
        print()

    print(build_answer(args.question, results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
