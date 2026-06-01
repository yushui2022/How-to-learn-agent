"""Structured output example for lesson 05.

The script can dry-run a request, validate local mock responses, or call an
OpenAI-compatible chat completion endpoint and validate the returned JSON.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any


DEFAULT_QUESTION = "什么是 RAG？"

SYSTEM_PROMPT = """你是一个面向 AI Agent 初学者的中文学习助手。

只输出合法 JSON，不要输出 Markdown，不要在 JSON 前后添加解释文字。

JSON 必须包含：
- answer.explanation: string，概念解释
- answer.misconception: string，常见误区
- exercise.task: string，下一步练习
- exercise.duration_minutes: number，练习预计耗时，1 到 30 之间
- follow_up_needed: boolean，是否需要先澄清
- follow_up_questions: string[]，澄清问题列表

如果用户问题太大或太模糊，把 follow_up_needed 设为 true，并给出 1 到 3 个澄清问题。
不要假装读取了外部资料。"""


MOCK_RESPONSES = {
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
    "bad": {
        "explanation": "RAG 是检索增强生成。",
        "exercise": "去查资料",
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
            "你更想学应用开发、算法研究，还是产品落地？",
            "你每周能投入多少时间？",
        ],
    },
}


def build_context(question: str) -> dict[str, Any]:
    return {
        "user_question": question,
        "learner_level": "beginner",
        "course_stage": "第 5 章：上下文工程与结构化输出",
        "known_terms": ["LLM", "Prompt"],
        "answer_policy": "不要假装读取外部资料；问题过大时先澄清。",
    }


def build_payload(
    *,
    model: str,
    question: str,
    temperature: float,
    max_tokens: int,
) -> dict[str, Any]:
    context = build_context(question)
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": json.dumps(context, ensure_ascii=False, indent=2),
            },
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }


def call_chat_completion(
    *,
    base_url: str,
    api_key: str,
    payload: dict[str, Any],
    timeout: int,
) -> dict[str, Any]:
    url = f"{base_url.rstrip('/')}/chat/completions"
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        response_body = response.read().decode("utf-8")
        return json.loads(response_body)


def extract_text(response_json: dict[str, Any]) -> str:
    choices = response_json.get("choices")
    if not isinstance(choices, list) or not choices:
        return json.dumps(response_json, ensure_ascii=False, indent=2)

    first = choices[0]
    if not isinstance(first, dict):
        return json.dumps(response_json, ensure_ascii=False, indent=2)

    message = first.get("message")
    if not isinstance(message, dict):
        return json.dumps(response_json, ensure_ascii=False, indent=2)

    content = message.get("content")
    if isinstance(content, str):
        return content

    return json.dumps(response_json, ensure_ascii=False, indent=2)


def parse_json_like_text(text: str) -> Any:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.startswith("json"):
            stripped = stripped[4:].strip()

    start = stripped.find("{")
    end = stripped.rfind("}")
    if start != -1 and end != -1 and end > start:
        stripped = stripped[start : end + 1]

    return json.loads(stripped)


def validate_result(value: Any) -> list[str]:
    errors: list[str] = []

    if not isinstance(value, dict):
        return ["result must be a JSON object"]

    answer = value.get("answer")
    if not isinstance(answer, dict):
        errors.append("answer must be an object")
    else:
        if not isinstance(answer.get("explanation"), str):
            errors.append("answer.explanation must be a string")
        if not isinstance(answer.get("misconception"), str):
            errors.append("answer.misconception must be a string")

    exercise = value.get("exercise")
    if not isinstance(exercise, dict):
        errors.append("exercise must be an object")
    else:
        if not isinstance(exercise.get("task"), str):
            errors.append("exercise.task must be a string")
        duration = exercise.get("duration_minutes")
        if not isinstance(duration, int):
            errors.append("exercise.duration_minutes must be an integer")
        elif duration < 1 or duration > 30:
            errors.append("exercise.duration_minutes must be between 1 and 30")

    if not isinstance(value.get("follow_up_needed"), bool):
        errors.append("follow_up_needed must be a boolean")

    questions = value.get("follow_up_questions")
    if not isinstance(questions, list):
        errors.append("follow_up_questions must be a list")
    elif not all(isinstance(item, str) for item in questions):
        errors.append("follow_up_questions must contain only strings")

    return errors


def print_validation(raw_text: str) -> int:
    print("Raw output:")
    print(raw_text)

    try:
        parsed = parse_json_like_text(raw_text)
    except json.JSONDecodeError as exc:
        print(f"\nValidation failed: invalid JSON: {exc}", file=sys.stderr)
        return 1

    errors = validate_result(parsed)
    if errors:
        print("\nValidation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("\nValidation passed.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run structured output demo.")
    parser.add_argument("--question", default=DEFAULT_QUESTION)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--max-tokens", type=int, default=700)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--mock", choices=["good", "bad", "clarify"])
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.mock:
        raw_text = json.dumps(MOCK_RESPONSES[args.mock], ensure_ascii=False, indent=2)
        return print_validation(raw_text)

    base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("LLM_MODEL", "replace-with-your-model-name")
    payload = build_payload(
        model=model,
        question=args.question,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    missing = []
    if not api_key:
        missing.append("LLM_API_KEY or OPENAI_API_KEY")
    if model == "replace-with-your-model-name":
        missing.append("LLM_MODEL")
    if missing:
        print(
            "Missing environment variable(s): " + ", ".join(missing),
            file=sys.stderr,
        )
        return 2

    start = time.perf_counter()
    try:
        response_json = call_chat_completion(
            base_url=base_url,
            api_key=api_key,
            payload=payload,
            timeout=args.timeout,
        )
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP {exc.code}: {error_body}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Network error: {exc.reason}", file=sys.stderr)
        return 1
    except TimeoutError:
        print("Request timed out.", file=sys.stderr)
        return 1

    latency = time.perf_counter() - start
    raw_text = extract_text(response_json)
    result = print_validation(raw_text)

    usage = response_json.get("usage")
    if usage is not None:
        print(f"[usage] {json.dumps(usage, ensure_ascii=False)}", file=sys.stderr)
    print(f"[latency] {latency:.2f}s", file=sys.stderr)

    return result


if __name__ == "__main__":
    raise SystemExit(main())
