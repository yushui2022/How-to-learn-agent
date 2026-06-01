"""Minimal OpenAI-compatible chat completion call for lesson 03.

The script uses only Python's standard library so beginners can inspect every
step: build messages, send an HTTP request, parse a response, and record basic
metadata.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request


DEFAULT_QUESTION = "什么是 RAG？"


def build_messages(question: str) -> list[dict[str, str]]:
    """Build the smallest useful message list for the learning assistant."""
    return [
        {
            "role": "system",
            "content": (
                "你是一个面向 AI Agent 初学者的中文学习助手。"
                "回答必须包含三部分：解释、常见误区、下一步练习。"
                "不要假装读取了外部资料。"
            ),
        },
        {"role": "user", "content": question},
    ]


def build_payload(
    *,
    model: str,
    question: str,
    temperature: float,
    max_tokens: int,
) -> dict[str, object]:
    return {
        "model": model,
        "messages": build_messages(question),
        "temperature": temperature,
        "max_tokens": max_tokens,
    }


def call_chat_completion(
    *,
    base_url: str,
    api_key: str,
    payload: dict[str, object],
    timeout: int,
) -> dict[str, object]:
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


def extract_text(response_json: dict[str, object]) -> str:
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a minimal LLM call.")
    parser.add_argument("--question", default=DEFAULT_QUESTION)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=500)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request payload without calling the model service.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

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
    print(extract_text(response_json))

    usage = response_json.get("usage")
    if usage is not None:
        print(f"\n[usage] {json.dumps(usage, ensure_ascii=False)}", file=sys.stderr)
    print(f"[latency] {latency:.2f}s", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
