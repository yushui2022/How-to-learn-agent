from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field, replace


COURSE_NOTES = {
    "RAG": "RAG = retrieve relevant course notes, then answer with citations.",
    "Tool Calling": "Tool calling lets a model request external capabilities; the app validates and executes.",
}


@dataclass
class AgentState:
    goal: str
    topic: str
    case: str
    notes: str | None = None
    practice: str | None = None
    answer_checked: bool = False
    failures: list[str] = field(default_factory=list)
    done: bool = False


@dataclass(frozen=True)
class Decision:
    summary: str
    action: str
    args: dict[str, str]
    should_stop: bool = False
    stop_reason: str = ""


@dataclass(frozen=True)
class ToolResult:
    ok: bool
    message: str
    data: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class TraceStep:
    step: int
    observation: str
    decision_summary: str
    action: str
    result: str
    state_change: str
    stop_reason: str = ""


def observe(state: AgentState) -> str:
    facts = [
        f"goal={state.goal}",
        f"topic={state.topic}",
        f"has_notes={state.notes is not None}",
        f"has_practice={state.practice is not None}",
        f"answer_checked={state.answer_checked}",
        f"failures={len(state.failures)}",
    ]
    return "; ".join(facts)


def decide(state: AgentState) -> Decision:
    if state.done:
        return Decision(
            summary="目标已经完成，停止循环。",
            action="finish",
            args={},
            should_stop=True,
            stop_reason="goal_complete",
        )

    if state.case == "looping-policy":
        return Decision(
            summary="错误策略示例：忽略已有结果，反复查询同一主题。",
            action="search_course_notes",
            args={"topic": state.topic},
        )

    if state.failures:
        return Decision(
            summary="已经出现工具失败，先停止并交给用户或开发者复盘。",
            action="stop",
            args={},
            should_stop=True,
            stop_reason="tool_failed",
        )

    if state.notes is None:
        return Decision(
            summary="还没有课程资料，先查询课程笔记。",
            action="search_course_notes",
            args={"topic": state.topic},
        )

    if state.notes == "":
        return Decision(
            summary="没有找到可靠资料，停止，避免编造答案。",
            action="stop",
            args={},
            should_stop=True,
            stop_reason="missing_notes",
        )

    if state.practice is None:
        return Decision(
            summary="已经找到资料，下一步生成练习题。",
            action="generate_practice",
            args={"topic": state.topic},
        )

    if not state.answer_checked:
        return Decision(
            summary="已经生成练习，下一步检查模拟答案。",
            action="check_answer",
            args={"topic": state.topic, "answer": "RAG 是检索资料后再回答。"},
        )

    return Decision(
        summary="练习已经检查完成，停止循环。",
        action="finish",
        args={},
        should_stop=True,
        stop_reason="goal_complete",
    )


def run_tool(action: str, args: dict[str, str], state: AgentState) -> ToolResult:
    if action == "search_course_notes":
        topic = args["topic"]
        if state.case == "missing-notes":
            return ToolResult(ok=True, message=f"no notes found for {topic}", data={"notes": ""})
        return ToolResult(
            ok=True,
            message=f"found notes for {topic}",
            data={"notes": COURSE_NOTES.get(topic, "")},
        )

    if action == "generate_practice":
        if state.case == "tool-error":
            return ToolResult(ok=False, message="practice generator failed")
        topic = args["topic"]
        return ToolResult(
            ok=True,
            message=f"generated practice for {topic}",
            data={"practice": f"用一句话解释 {topic} 的输入、处理和输出。"},
        )

    if action == "check_answer":
        return ToolResult(
            ok=True,
            message="answer accepted",
            data={"answer_checked": "true"},
        )

    return ToolResult(ok=False, message=f"unknown action: {action}")


def apply_result(state: AgentState, decision: Decision, result: ToolResult) -> str:
    if not result.ok:
        state.failures.append(result.message)
        return f"failures += {result.message}"

    if decision.action == "search_course_notes":
        state.notes = result.data.get("notes", "")
        return f"notes set; found={bool(state.notes)}"

    if decision.action == "generate_practice":
        state.practice = result.data["practice"]
        return "practice created"

    if decision.action == "check_answer":
        state.answer_checked = result.data.get("answer_checked") == "true"
        state.done = state.answer_checked
        return "answer_checked=true; done=true"

    return "no state change"


def run_agent(case: str, max_steps: int) -> tuple[AgentState, list[TraceStep], str]:
    topic = "Unknown Topic" if case == "missing-notes" else "RAG"
    state = AgentState(goal="完成一次 RAG 复习", topic=topic, case=case)
    trace: list[TraceStep] = []

    for step in range(1, max_steps + 1):
        observation = observe(state)
        decision = decide(state)

        if decision.should_stop:
            trace.append(
                TraceStep(
                    step=step,
                    observation=observation,
                    decision_summary=decision.summary,
                    action=decision.action,
                    result="not executed",
                    state_change="none",
                    stop_reason=decision.stop_reason,
                )
            )
            return state, trace, decision.stop_reason

        result = run_tool(decision.action, decision.args, state)
        state_change = apply_result(state, decision, result)
        stop_reason = "goal_complete" if state.done else ""
        trace.append(
            TraceStep(
                step=step,
                observation=observation,
                decision_summary=decision.summary,
                action=f"{decision.action}({decision.args})",
                result=result.message,
                state_change=state_change,
                stop_reason=stop_reason,
            )
        )
        if stop_reason:
            return state, trace, stop_reason

    if trace:
        trace[-1] = replace(trace[-1], stop_reason="max_steps_reached")
    return state, trace, "max_steps_reached"


def print_text(case: str, state: AgentState, trace: list[TraceStep], stop_reason: str) -> None:
    print(f"Case: {case}")
    print(f"Goal: {state.goal}")
    print(f"Stop reason: {stop_reason}")
    print()

    for item in trace:
        print(f"Step {item.step}")
        print(f"Observation: {item.observation}")
        print(f"Decision: {item.decision_summary}")
        print(f"Action: {item.action}")
        print(f"Result: {item.result}")
        print(f"State change: {item.state_change}")
        if item.stop_reason:
            print(f"Stop: {item.stop_reason}")
        print("-" * 40)

    print("Final state:")
    print(json.dumps(asdict(state), ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a minimal Agent loop demo.")
    parser.add_argument(
        "--case",
        choices=["success", "missing-notes", "tool-error", "looping-policy"],
        default="success",
        help="Choose a demo case.",
    )
    parser.add_argument("--max-steps", type=int, default=4, help="Maximum loop steps.")
    parser.add_argument("--json", action="store_true", help="Print JSON trace.")
    args = parser.parse_args()

    if args.max_steps < 1:
        raise SystemExit("--max-steps must be at least 1")

    state, trace, stop_reason = run_agent(args.case, args.max_steps)

    if args.json:
        print(
            json.dumps(
                {
                    "case": args.case,
                    "stop_reason": stop_reason,
                    "trace": [asdict(item) for item in trace],
                    "final_state": asdict(state),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    print_text(args.case, state, trace, stop_reason)


if __name__ == "__main__":
    main()
