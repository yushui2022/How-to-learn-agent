from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field


@dataclass
class SessionState:
    goal: str = ""
    current_topic: str = ""
    current_step: str = "idle"
    last_event: str = ""
    stop_reason: str = ""


@dataclass
class MemoryItem:
    memory_id: str
    memory_type: str
    content: str
    source: str
    scope: str
    confidence: float
    user_visible: bool = True
    deletable: bool = True


@dataclass
class MemoryDecision:
    action: str
    reason: str
    requires_confirmation: bool = False
    candidate: MemoryItem | None = None


@dataclass
class RunResult:
    case: str
    state: SessionState
    decision: MemoryDecision
    memories: list[MemoryItem]
    retrieved_context: list[MemoryItem] = field(default_factory=list)
    audit_log: list[str] = field(default_factory=list)


class MemoryStore:
    def __init__(self) -> None:
        self._items: dict[str, MemoryItem] = {}

    def add(self, item: MemoryItem) -> None:
        self._items[item.memory_id] = item

    def delete(self, memory_id: str) -> bool:
        return self._items.pop(memory_id, None) is not None

    def list_items(self) -> list[MemoryItem]:
        return list(self._items.values())

    def search(self, keyword: str) -> list[MemoryItem]:
        lowered = keyword.lower()
        return [
            item
            for item in self._items.values()
            if lowered in item.content.lower() or lowered in item.memory_type.lower()
        ]


def seed_store() -> MemoryStore:
    store = MemoryStore()
    store.add(
        MemoryItem(
            memory_id="pref_project_based",
            memory_type="preference",
            content="用户更喜欢项目驱动学习",
            source="user_confirmed",
            scope="ai-learning-assistant",
            confidence=1.0,
        )
    )
    store.add(
        MemoryItem(
            memory_id="weak_rag_no_answer",
            memory_type="weak_point",
            content="用户在 RAG 无答案处理上容易出错",
            source="exercise_result",
            scope="ai-learning-assistant",
            confidence=0.8,
        )
    )
    return store


def decide_memory(case: str, state: SessionState) -> MemoryDecision:
    if case == "learning-goal":
        return MemoryDecision(
            action="propose_write",
            reason="长期学习目标会影响后续学习安排，但需要用户确认",
            requires_confirmation=True,
            candidate=MemoryItem(
                memory_id="goal_learn_rag_two_weeks",
                memory_type="learning_goal",
                content="用户想两周内学会 RAG",
                source="user_confirmed",
                scope="ai-learning-assistant",
                confidence=1.0,
            ),
        )

    if case == "weak-point":
        return MemoryDecision(
            action="propose_write",
            reason="练习结果暴露了稳定薄弱点，可以保存，但要允许用户查看和删除",
            requires_confirmation=True,
            candidate=MemoryItem(
                memory_id="weak_rag_no_answer",
                memory_type="weak_point",
                content="用户在 RAG 无答案处理上容易出错",
                source="exercise_result",
                scope="ai-learning-assistant",
                confidence=0.8,
            ),
        )

    if case == "sensitive":
        return MemoryDecision(
            action="skip",
            reason="输入包含敏感信息，不写入长期记忆",
        )

    if case == "delete-memory":
        return MemoryDecision(
            action="delete",
            reason="用户请求删除指定记忆",
        )

    return MemoryDecision(
        action="retrieve",
        reason="当前任务需要检索相关长期记忆",
    )


def apply_case(case: str, confirm_memory: bool) -> RunResult:
    store = seed_store()
    state = SessionState(last_event=case)
    audit_log: list[str] = []
    retrieved_context: list[MemoryItem] = []

    if case == "learning-goal":
        state.goal = "两周内学会 RAG"
        state.current_topic = "RAG"
        state.current_step = "planning"

    elif case == "weak-point":
        state.goal = "复盘 RAG 练习"
        state.current_topic = "RAG"
        state.current_step = "review_exercise"

    elif case == "sensitive":
        state.current_step = "redact_input"
        state.stop_reason = "sensitive_input_not_saved"

    elif case == "retrieve":
        state.goal = "继续学习 RAG"
        state.current_topic = "RAG"
        state.current_step = "retrieve_relevant_memory"

    elif case == "delete-memory":
        state.current_step = "delete_memory"

    decision = decide_memory(case, state)

    if decision.action == "propose_write":
        if confirm_memory and decision.candidate:
            store.add(decision.candidate)
            audit_log.append(f"memory_saved:{decision.candidate.memory_id}")
        else:
            audit_log.append("memory_not_saved:confirmation_required")

    elif decision.action == "skip":
        audit_log.append("memory_skipped:sensitive")

    elif decision.action == "retrieve":
        retrieved_context = store.search(state.current_topic)
        audit_log.append(f"memory_retrieved:{len(retrieved_context)}")

    elif decision.action == "delete":
        deleted = store.delete("weak_rag_no_answer")
        audit_log.append(f"memory_deleted:{deleted}")

    return RunResult(
        case=case,
        state=state,
        decision=decision,
        memories=store.list_items(),
        retrieved_context=retrieved_context,
        audit_log=audit_log,
    )


def print_text(result: RunResult) -> None:
    print(f"Case: {result.case}")
    print("State:")
    print(json.dumps(asdict(result.state), ensure_ascii=False, indent=2))
    print()
    print("Memory decision:")
    print(json.dumps(asdict(result.decision), ensure_ascii=False, indent=2))
    print()
    if result.retrieved_context:
        print("Retrieved context:")
        for item in result.retrieved_context:
            print(f"- {item.memory_id}: {item.content}")
        print()
    print("Memory store:")
    for item in result.memories:
        print(f"- {item.memory_id} [{item.memory_type}]: {item.content}")
    print()
    print("Audit log:")
    for line in result.audit_log:
        print(f"- {line}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Demonstrate the difference between State and Memory.")
    parser.add_argument(
        "--case",
        choices=["learning-goal", "weak-point", "sensitive", "retrieve", "delete-memory"],
        default="retrieve",
        help="Choose a demo case.",
    )
    parser.add_argument("--confirm-memory", action="store_true", help="Allow memory write when confirmation is required.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args()

    result = apply_case(args.case, args.confirm_memory)

    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
        return

    print_text(result)


if __name__ == "__main__":
    main()
