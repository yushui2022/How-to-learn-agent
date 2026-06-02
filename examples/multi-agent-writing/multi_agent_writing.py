from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field


@dataclass
class HandoffMessage:
    round_id: int
    sender: str
    receiver: str
    artifact_type: str
    status: str
    content: str
    evidence: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    requested_action: str = ""


@dataclass
class WorkflowResult:
    case: str
    stop_reason: str
    final_status: str
    revision_rounds: int
    messages: list[HandoffMessage]


def researcher(case: str) -> HandoffMessage:
    if case == "missing-source":
        return HandoffMessage(
            round_id=0,
            sender="Researcher",
            receiver="Writer",
            artifact_type="research_notes",
            status="blocked",
            content="没有找到足够证据支持 RAG 评估说明。",
            evidence=[],
            open_questions=["需要补充 RAG 评估资料"],
            requested_action="停止写作并请求补资料",
        )

    return HandoffMessage(
        round_id=0,
        sender="Researcher",
        receiver="Writer",
        artifact_type="research_notes",
        status="ready",
        content="RAG 评估需要拆分检索质量、回答质量和引用质量。",
        evidence=["lesson-08-rag-evaluation", "rag-evaluation-example"],
        open_questions=["是否需要加入长期记忆质量评估"],
        requested_action="基于证据写一段简短说明",
    )


def writer(notes: HandoffMessage, case: str, revision_round: int) -> HandoffMessage:
    if notes.status == "blocked":
        return HandoffMessage(
            round_id=revision_round,
            sender="Writer",
            receiver="Reviewer",
            artifact_type="draft",
            status="blocked",
            content="研究资料不足，无法写可靠草稿。",
            evidence=[],
            open_questions=notes.open_questions,
            requested_action="停止并请求补资料",
        )

    if case == "needs-revision" and revision_round == 0:
        content = "RAG 评估可以保证系统准确率显著提升。"
        evidence = ["lesson-08-rag-evaluation"]
    else:
        content = "RAG 评估应分别检查检索是否命中、回答是否基于资料、引用是否支持结论。"
        evidence = notes.evidence

    return HandoffMessage(
        round_id=revision_round,
        sender="Writer",
        receiver="Reviewer",
        artifact_type="draft",
        status="ready",
        content=content,
        evidence=evidence,
        open_questions=notes.open_questions,
        requested_action="检查结论是否被证据支持",
    )


def reviewer(draft: HandoffMessage) -> HandoffMessage:
    if draft.status == "blocked":
        return HandoffMessage(
            round_id=draft.round_id,
            sender="Reviewer",
            receiver="Supervisor",
            artifact_type="review_report",
            status="blocked",
            content="草稿无法生成，因为上游资料不足。",
            evidence=draft.evidence,
            open_questions=draft.open_questions,
            requested_action="请求用户补充资料",
        )

    unsupported_claim = "保证系统准确率显著提升" in draft.content
    has_evidence = bool(draft.evidence)

    if unsupported_claim or not has_evidence:
        return HandoffMessage(
            round_id=draft.round_id,
            sender="Reviewer",
            receiver="Writer",
            artifact_type="review_report",
            status="needs_revision",
            content="草稿包含未被证据支持的强结论，需要改成可由资料支持的表述。",
            evidence=draft.evidence,
            open_questions=["删除或弱化 unsupported claim"],
            requested_action="修订草稿并保留证据来源",
        )

    return HandoffMessage(
        round_id=draft.round_id,
        sender="Reviewer",
        receiver="Supervisor",
        artifact_type="review_report",
        status="ready",
        content="草稿通过：核心结论都有证据支持。",
        evidence=draft.evidence,
        requested_action="输出最终说明",
    )


def run(case: str, max_rounds: int) -> WorkflowResult:
    messages: list[HandoffMessage] = []
    notes = researcher(case)
    messages.append(notes)

    if notes.status == "blocked":
        draft = writer(notes, case, revision_round=0)
        review = reviewer(draft)
        messages.extend([draft, review])
        return WorkflowResult(
            case=case,
            stop_reason="blocked_missing_sources",
            final_status="blocked",
            revision_rounds=0,
            messages=messages,
        )

    revision_round = 0
    while True:
        draft = writer(notes, case, revision_round)
        review = reviewer(draft)
        messages.extend([draft, review])

        if review.status == "ready":
            return WorkflowResult(
                case=case,
                stop_reason="accepted",
                final_status="ready",
                revision_rounds=revision_round,
                messages=messages,
            )

        if revision_round >= max_rounds:
            return WorkflowResult(
                case=case,
                stop_reason="max_revision_rounds_reached",
                final_status="needs_human_review",
                revision_rounds=revision_round,
                messages=messages,
            )

        revision_round += 1


def print_text(result: WorkflowResult) -> None:
    print(f"Case: {result.case}")
    print(f"Final status: {result.final_status}")
    print(f"Stop reason: {result.stop_reason}")
    print(f"Revision rounds: {result.revision_rounds}")
    print()

    for message in result.messages:
        print(f"Round {message.round_id}: {message.sender} -> {message.receiver}")
        print(f"Artifact: {message.artifact_type}")
        print(f"Status: {message.status}")
        print(f"Content: {message.content}")
        if message.evidence:
            print(f"Evidence: {', '.join(message.evidence)}")
        if message.open_questions:
            print(f"Open questions: {', '.join(message.open_questions)}")
        print(f"Requested action: {message.requested_action}")
        print("-" * 48)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a deterministic multi-agent writing demo.")
    parser.add_argument(
        "--case",
        choices=["happy-path", "missing-source", "needs-revision"],
        default="happy-path",
        help="Choose a demo case.",
    )
    parser.add_argument("--max-rounds", type=int, default=1, help="Maximum revision rounds.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args()

    if args.max_rounds < 0:
        raise SystemExit("--max-rounds must be 0 or greater")

    result = run(args.case, args.max_rounds)

    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
        return

    print_text(result)


if __name__ == "__main__":
    main()
