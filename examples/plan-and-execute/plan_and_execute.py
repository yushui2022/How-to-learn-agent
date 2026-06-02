from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field


NOTES = {
    "RAG": "RAG connects retrieval, context construction, answer generation, and citation.",
    "Tool Calling": "Tool calling separates model requests from application-side validation and execution.",
}


@dataclass
class PlanStep:
    step_id: str
    owner: str
    action: str
    expected_output: str
    pass_criteria: str
    status: str = "pending"


@dataclass
class PlanningState:
    goal: str
    topic: str
    case: str
    plan_version: int = 1
    replan_count: int = 0
    notes: str = ""
    explanation: str = ""
    practice: str = ""
    completed: bool = False
    plan: list[PlanStep] = field(default_factory=list)


@dataclass
class StepResult:
    ok: bool
    evidence: str
    state_change: str
    reviewer_decision: str
    replan_reason: str = ""
    stop_reason: str = ""


@dataclass
class ExecutionRecord:
    iteration: int
    plan_version: int
    step_id: str
    owner: str
    action: str
    expected_output: str
    evidence: str
    status: str
    reviewer_decision: str
    replan_reason: str = ""
    stop_reason: str = ""


def build_plan(topic: str, mode: str = "standard") -> list[PlanStep]:
    if mode == "request_materials":
        return [
            PlanStep(
                step_id="S1",
                owner="Reviewer",
                action="request_materials",
                expected_output="向用户说明缺少资料，并请求补充课程材料",
                pass_criteria="用户知道下一步需要提供什么",
            )
        ]

    return [
        PlanStep(
            step_id="S1",
            owner="Planner",
            action="confirm_goal",
            expected_output=f"确认本轮目标是学习 {topic}",
            pass_criteria="目标明确且没有变化",
        ),
        PlanStep(
            step_id="S2",
            owner="Executor",
            action="retrieve_notes",
            expected_output=f"找到 {topic} 的课程资料",
            pass_criteria="至少找到一段可引用资料",
        ),
        PlanStep(
            step_id="S3",
            owner="Executor",
            action="explain_concept",
            expected_output=f"生成 {topic} 的概念说明",
            pass_criteria="说明包含输入、处理和输出",
        ),
        PlanStep(
            step_id="S4",
            owner="Executor",
            action="generate_practice",
            expected_output=f"生成 {topic} 练习题",
            pass_criteria="练习能检查核心概念",
        ),
        PlanStep(
            step_id="S5",
            owner="Reviewer",
            action="review_result",
            expected_output="判断本轮学习任务是否完成",
            pass_criteria="资料、说明和练习都存在",
        ),
    ]


def next_pending_step(plan: list[PlanStep]) -> PlanStep | None:
    return next((step for step in plan if step.status == "pending"), None)


def execute_step(state: PlanningState, step: PlanStep) -> StepResult:
    if step.action == "confirm_goal":
        if state.case == "user-change" and state.plan_version == 1:
            state.topic = "Tool Calling"
            return StepResult(
                ok=False,
                evidence="用户改口：先学 Tool Calling，再回到 RAG",
                state_change="topic=Tool Calling",
                reviewer_decision="replan",
                replan_reason="user_changed_goal",
            )
        return StepResult(
            ok=True,
            evidence=f"目标确认：学习 {state.topic}",
            state_change="goal_confirmed=true",
            reviewer_decision="continue",
        )

    if step.action == "retrieve_notes":
        if state.case == "retrieval-fails" and state.plan_version == 1:
            return StepResult(
                ok=False,
                evidence=f"没有找到 {state.topic} 的可靠资料",
                state_change="notes=",
                reviewer_decision="replan",
                replan_reason="missing_materials",
            )
        state.notes = NOTES.get(state.topic, "")
        if not state.notes:
            return StepResult(
                ok=False,
                evidence=f"资料库没有 {state.topic}",
                state_change="notes=",
                reviewer_decision="replan",
                replan_reason="missing_materials",
            )
        return StepResult(
            ok=True,
            evidence=state.notes,
            state_change="notes_found=true",
            reviewer_decision="continue",
        )

    if step.action == "explain_concept":
        if not state.notes:
            return StepResult(
                ok=False,
                evidence="缺少资料，不能生成可靠说明",
                state_change="explanation=",
                reviewer_decision="stop",
                stop_reason="missing_notes",
            )
        state.explanation = f"{state.topic}：先拿到相关资料，再基于资料完成任务。"
        return StepResult(
            ok=True,
            evidence=state.explanation,
            state_change="explanation_created=true",
            reviewer_decision="continue",
        )

    if step.action == "generate_practice":
        if not state.explanation:
            return StepResult(
                ok=False,
                evidence="没有概念说明，不能生成练习",
                state_change="practice=",
                reviewer_decision="stop",
                stop_reason="missing_explanation",
            )
        state.practice = f"用一句话说明 {state.topic} 的输入、处理和输出。"
        return StepResult(
            ok=True,
            evidence=state.practice,
            state_change="practice_created=true",
            reviewer_decision="continue",
        )

    if step.action == "review_result":
        if state.notes and state.explanation and state.practice:
            state.completed = True
            return StepResult(
                ok=True,
                evidence="资料、说明和练习都存在",
                state_change="completed=true",
                reviewer_decision="stop",
                stop_reason="goal_complete",
            )
        return StepResult(
            ok=False,
            evidence="学习产物不完整",
            state_change="completed=false",
            reviewer_decision="replan",
            replan_reason="incomplete_outputs",
        )

    if step.action == "request_materials":
        return StepResult(
            ok=False,
            evidence=f"请补充 {state.topic} 的课程资料后再继续",
            state_change="waiting_for_user=true",
            reviewer_decision="stop",
            stop_reason="blocked_missing_materials",
        )

    return StepResult(
        ok=False,
        evidence=f"未知动作：{step.action}",
        state_change="none",
        reviewer_decision="stop",
        stop_reason="unknown_action",
    )


def replan(state: PlanningState, reason: str) -> None:
    state.replan_count += 1
    state.plan_version += 1
    if reason == "missing_materials":
        state.plan = build_plan(state.topic, mode="request_materials")
        return
    state.plan = build_plan(state.topic)


def run(case: str, max_steps: int) -> tuple[PlanningState, list[ExecutionRecord], str]:
    state = PlanningState(goal="两周内学会 RAG", topic="RAG", case=case)
    state.plan = build_plan(state.topic)
    records: list[ExecutionRecord] = []

    for iteration in range(1, max_steps + 1):
        step = next_pending_step(state.plan)
        if step is None:
            return state, records, "plan_finished_without_reviewer"

        result = execute_step(state, step)
        step.status = "done" if result.ok else "failed"
        records.append(
            ExecutionRecord(
                iteration=iteration,
                plan_version=state.plan_version,
                step_id=step.step_id,
                owner=step.owner,
                action=step.action,
                expected_output=step.expected_output,
                evidence=result.evidence,
                status=step.status,
                reviewer_decision=result.reviewer_decision,
                replan_reason=result.replan_reason,
                stop_reason=result.stop_reason,
            )
        )

        if result.reviewer_decision == "replan":
            replan(state, result.replan_reason)
            continue

        if result.reviewer_decision == "stop":
            return state, records, result.stop_reason or "stopped"

    if records:
        records[-1].stop_reason = "max_steps_reached"
    return state, records, "max_steps_reached"


def print_text(state: PlanningState, records: list[ExecutionRecord], stop_reason: str) -> None:
    print(f"Case: {state.case}")
    print(f"Goal: {state.goal}")
    print(f"Final topic: {state.topic}")
    print(f"Plan version: v{state.plan_version}")
    print(f"Replans: {state.replan_count}")
    print(f"Stop reason: {stop_reason}")
    print()

    for record in records:
        print(f"Iteration {record.iteration} | Plan v{record.plan_version} | {record.step_id}")
        print(f"Owner: {record.owner}")
        print(f"Action: {record.action}")
        print(f"Expected: {record.expected_output}")
        print(f"Evidence: {record.evidence}")
        print(f"Status: {record.status}")
        print(f"Reviewer decision: {record.reviewer_decision}")
        if record.replan_reason:
            print(f"Replan reason: {record.replan_reason}")
        if record.stop_reason:
            print(f"Stop: {record.stop_reason}")
        print("-" * 48)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a deterministic plan-and-execute demo.")
    parser.add_argument(
        "--case",
        choices=["happy-path", "retrieval-fails", "user-change"],
        default="happy-path",
        help="Choose a demo case.",
    )
    parser.add_argument("--max-steps", type=int, default=8, help="Maximum execution iterations.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args()

    if args.max_steps < 1:
        raise SystemExit("--max-steps must be at least 1")

    state, records, stop_reason = run(args.case, args.max_steps)

    if args.json:
        print(
            json.dumps(
                {
                    "stop_reason": stop_reason,
                    "state": asdict(state),
                    "records": [asdict(record) for record in records],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    print_text(state, records, stop_reason)


if __name__ == "__main__":
    main()
