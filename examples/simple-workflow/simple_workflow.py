"""A minimal deterministic AI workflow for lesson 06.

The model step is mocked on purpose. This keeps the example focused on workflow
structure: state, nodes, conditions, branches, and trace.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from typing import Any


MOCK_MODEL_OUTPUTS: dict[str, dict[str, Any]] = {
    "good": {
        "answer": {
            "explanation": "RAG 是先检索资料，再基于资料生成回答的方法。",
            "misconception": "RAG 不是让模型永久记住所有知识。",
        },
        "exercise": {
            "task": "找一段课程笔记，写出 3 个适合检索的问题。",
            "duration_minutes": 10,
        },
        "follow_up_needed": False,
        "follow_up_questions": [],
    },
    "clarify": {
        "answer": {
            "explanation": "",
            "misconception": "",
        },
        "exercise": {
            "task": "",
            "duration_minutes": 1,
        },
        "follow_up_needed": True,
        "follow_up_questions": [
            "你现在的 AI 基础是什么？",
            "你更想学习应用开发、算法研究，还是产品落地？",
            "你每周能投入多少时间？",
        ],
    },
    "invalid": {
        "explanation": "RAG 是检索增强生成。",
        "exercise": "去查资料。",
    },
}


def add_trace(
    state: dict[str, Any],
    *,
    node: str,
    output: dict[str, Any],
) -> None:
    state["trace"].append(
        {
            "step": len(state["trace"]) + 1,
            "node": node,
            "output": deepcopy(output),
        }
    )


def build_context(state: dict[str, Any]) -> dict[str, Any]:
    context = {
        "user_question": state["question"],
        "learner_level": "beginner",
        "course_stage": "第 6 章：AI 工作流",
        "known_terms": ["LLM", "Prompt", "结构化输出"],
        "answer_policy": "问题过大时先澄清；不要假装读取外部资料。",
    }
    state["context"] = context
    add_trace(state, node="build_context", output={"context": context})
    return state


def generate_answer(state: dict[str, Any]) -> dict[str, Any]:
    case = state["case"]
    model_output = deepcopy(MOCK_MODEL_OUTPUTS[case])
    state["model_output"] = model_output
    add_trace(state, node="generate_answer", output={"model_output": model_output})
    return state


def validate_output(state: dict[str, Any]) -> dict[str, Any]:
    value = state["model_output"]
    errors: list[str] = []

    if not isinstance(value.get("answer"), dict):
        errors.append("answer must be an object")
    if not isinstance(value.get("exercise"), dict):
        errors.append("exercise must be an object")
    if not isinstance(value.get("follow_up_needed"), bool):
        errors.append("follow_up_needed must be a boolean")
    if not isinstance(value.get("follow_up_questions"), list):
        errors.append("follow_up_questions must be a list")

    state["validation_errors"] = errors
    add_trace(state, node="validate_output", output={"validation_errors": errors})
    return state


def route_next_action(state: dict[str, Any]) -> dict[str, Any]:
    if state["validation_errors"]:
        next_action = "error"
    elif state["model_output"].get("follow_up_needed") is True:
        next_action = "clarify"
    else:
        next_action = "answer"

    state["next_action"] = next_action
    add_trace(state, node="route_next_action", output={"next_action": next_action})
    return state


def render_result(state: dict[str, Any]) -> dict[str, Any]:
    action = state["next_action"]
    output = state["model_output"]

    if action == "answer":
        result = (
            f"解释：{output['answer']['explanation']}\n"
            f"常见误区：{output['answer']['misconception']}\n"
            f"下一步练习：{output['exercise']['task']}"
        )
    elif action == "clarify":
        questions = "\n".join(f"- {item}" for item in output["follow_up_questions"])
        result = "这个目标太大，需要先澄清：\n" + questions
    else:
        errors = "\n".join(f"- {item}" for item in state["validation_errors"])
        result = "模型输出不合规，已进入错误分支：\n" + errors

    state["final_output"] = result
    add_trace(state, node="render_result", output={"final_output": result})
    return state


def run_workflow(question: str, case: str) -> dict[str, Any]:
    state: dict[str, Any] = {
        "question": question,
        "case": case,
        "context": {},
        "model_output": {},
        "validation_errors": [],
        "next_action": "",
        "final_output": "",
        "trace": [],
    }

    for node in [
        build_context,
        generate_answer,
        validate_output,
        route_next_action,
        render_result,
    ]:
        state = node(state)

    return state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a deterministic workflow.")
    parser.add_argument("--question")
    parser.add_argument("--case", choices=["good", "clarify", "invalid"], default="good")
    parser.add_argument("--show-trace", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    question = args.question
    if question is None:
        question = "帮我学会所有 AI" if args.case == "clarify" else "什么是 RAG？"

    state = run_workflow(question, args.case)

    print(state["final_output"])

    if args.show_trace:
        print("\nTrace:")
        print(json.dumps(state["trace"], ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
