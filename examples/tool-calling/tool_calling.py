"""Minimal tool-calling example for lesson 09.

The model output is mocked. The important part is the application-side control:
validate tool name, validate arguments, check permission, execute, and log.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any, Callable


ToolHandler = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    schema: dict[str, type]
    required: tuple[str, ...]
    permission: str
    handler: ToolHandler


COURSE_NOTES = {
    "rag": "RAG 是先检索资料，再基于资料生成回答，不是让模型永久记住资料。",
    "workflow": "工作流的下一步由预设规则决定；Agent 会根据中间结果动态决定下一步。",
    "tool": "工具调用由模型提出请求，应用程序负责校验、授权和执行。",
}


def search_course_notes(args: dict[str, Any]) -> dict[str, Any]:
    query = args["query"].lower()
    top_k = args["top_k"]
    hits = [
        {"topic": topic, "text": text}
        for topic, text in COURSE_NOTES.items()
        if query in topic or query in text.lower()
    ]
    return {"hits": hits[:top_k], "count": min(len(hits), top_k)}


def generate_practice(args: dict[str, Any]) -> dict[str, Any]:
    topic = args["topic"]
    difficulty = args["difficulty"]
    return {
        "task": f"用自己的话解释 {topic}，再写一个适合初学者的问题。",
        "difficulty": difficulty,
        "duration_minutes": 10,
    }


def save_learning_record(args: dict[str, Any]) -> dict[str, Any]:
    return {
        "saved": True,
        "topic": args["topic"],
        "status": args["status"],
    }


TOOLS = {
    "search_course_notes": ToolSpec(
        name="search_course_notes",
        description="查询课程笔记，返回相关片段。",
        schema={"query": str, "top_k": int},
        required=("query", "top_k"),
        permission="read_only",
        handler=search_course_notes,
    ),
    "generate_practice": ToolSpec(
        name="generate_practice",
        description="为一个主题生成练习任务。",
        schema={"topic": str, "difficulty": str},
        required=("topic", "difficulty"),
        permission="read_only",
        handler=generate_practice,
    ),
    "save_learning_record": ToolSpec(
        name="save_learning_record",
        description="保存用户学习记录。",
        schema={"topic": str, "status": str},
        required=("topic", "status"),
        permission="write_requires_confirmation",
        handler=save_learning_record,
    ),
}


MOCK_TOOL_REQUESTS = {
    "search": {
        "tool": "search_course_notes",
        "arguments": {"query": "rag", "top_k": 2},
    },
    "practice": {
        "tool": "generate_practice",
        "arguments": {"topic": "Tool Calling", "difficulty": "beginner"},
    },
    "save-record": {
        "tool": "save_learning_record",
        "arguments": {"topic": "RAG", "status": "reviewed"},
    },
    "invalid-args": {
        "tool": "search_course_notes",
        "arguments": {"top_k": "many"},
    },
    "unknown-tool": {
        "tool": "delete_learning_record",
        "arguments": {"topic": "RAG"},
    },
}


def validate_arguments(spec: ToolSpec, arguments: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for name in spec.required:
        if name not in arguments:
            errors.append(f"missing required argument: {name}")
            continue
        expected_type = spec.schema[name]
        if not isinstance(arguments[name], expected_type):
            errors.append(
                f"{name} must be {expected_type.__name__}, "
                f"got {type(arguments[name]).__name__}"
            )

    if "top_k" in arguments and isinstance(arguments["top_k"], int):
        if arguments["top_k"] < 1 or arguments["top_k"] > 5:
            errors.append("top_k must be between 1 and 5")

    return errors


def execute_tool_request(
    request: dict[str, Any],
    *,
    confirmed: bool,
) -> dict[str, Any]:
    trace: dict[str, Any] = {
        "request": request,
        "status": "pending",
        "validation_errors": [],
        "permission": "",
        "result": None,
    }

    tool_name = request.get("tool")
    arguments = request.get("arguments", {})
    if not isinstance(tool_name, str) or tool_name not in TOOLS:
        trace["status"] = "rejected"
        trace["validation_errors"].append(f"unknown tool: {tool_name}")
        return trace

    if not isinstance(arguments, dict):
        trace["status"] = "rejected"
        trace["validation_errors"].append("arguments must be an object")
        return trace

    spec = TOOLS[tool_name]
    trace["permission"] = spec.permission
    errors = validate_arguments(spec, arguments)
    if errors:
        trace["status"] = "rejected"
        trace["validation_errors"] = errors
        return trace

    if spec.permission == "write_requires_confirmation" and not confirmed:
        trace["status"] = "rejected"
        trace["validation_errors"].append("confirmation required")
        return trace

    trace["result"] = spec.handler(arguments)
    trace["status"] = "executed"
    return trace


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a tool-calling demo.")
    parser.add_argument(
        "--case",
        choices=list(MOCK_TOOL_REQUESTS.keys()),
        default="search",
    )
    parser.add_argument("--confirm", action="store_true")
    parser.add_argument("--show-log", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    request = MOCK_TOOL_REQUESTS[args.case]
    trace = execute_tool_request(request, confirmed=args.confirm)

    print(f"status: {trace['status']}")
    if trace["result"] is not None:
        print("result:")
        print(json.dumps(trace["result"], ensure_ascii=False, indent=2))
    if trace["validation_errors"]:
        print("errors:")
        for error in trace["validation_errors"]:
            print(f"- {error}")

    if args.show_log:
        print("\ntrace:")
        print(json.dumps(trace, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
