from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    case_id: str
    title: str
    task: str
    fixed_steps: bool
    needs_external_knowledge: bool
    needs_tools: bool
    needs_dynamic_choice: bool
    needs_iteration: bool
    needs_state: bool
    has_side_effects: bool
    risk: str


SCENARIOS: dict[str, Scenario] = {
    "chat-answer": Scenario(
        case_id="chat-answer",
        title="一次性概念解释",
        task="用户问：RAG 是不是让模型记住资料？系统直接解释概念。",
        fixed_steps=False,
        needs_external_knowledge=False,
        needs_tools=False,
        needs_dynamic_choice=False,
        needs_iteration=False,
        needs_state=False,
        has_side_effects=False,
        risk="low",
    ),
    "rag-answer": Scenario(
        case_id="rag-answer",
        title="课程资料问答",
        task="用户问第 7 章内容，系统检索课程资料后回答并引用来源。",
        fixed_steps=True,
        needs_external_knowledge=True,
        needs_tools=False,
        needs_dynamic_choice=False,
        needs_iteration=False,
        needs_state=False,
        has_side_effects=False,
        risk="low",
    ),
    "fixed-workflow": Scenario(
        case_id="fixed-workflow",
        title="固定学习计划生成",
        task="系统按固定步骤收集目标、生成计划、生成练习、输出结果。",
        fixed_steps=True,
        needs_external_knowledge=True,
        needs_tools=False,
        needs_dynamic_choice=False,
        needs_iteration=False,
        needs_state=False,
        has_side_effects=False,
        risk="low",
    ),
    "tool-app": Scenario(
        case_id="tool-app",
        title="带工具的学习助手",
        task="模型可以请求查询课程笔记、生成练习、保存学习记录。",
        fixed_steps=True,
        needs_external_knowledge=True,
        needs_tools=True,
        needs_dynamic_choice=False,
        needs_iteration=False,
        needs_state=True,
        has_side_effects=True,
        risk="medium",
    ),
    "study-agent": Scenario(
        case_id="study-agent",
        title="长期学习目标跟踪",
        task="用户说两周内学会 RAG，系统要检查进度、选择下一步、生成练习并根据结果调整。",
        fixed_steps=False,
        needs_external_knowledge=True,
        needs_tools=True,
        needs_dynamic_choice=True,
        needs_iteration=True,
        needs_state=True,
        has_side_effects=True,
        risk="medium",
    ),
    "browser-action": Scenario(
        case_id="browser-action",
        title="浏览器自动操作",
        task="系统根据目标打开网页、填写表单，并可能提交真实业务动作。",
        fixed_steps=False,
        needs_external_knowledge=True,
        needs_tools=True,
        needs_dynamic_choice=True,
        needs_iteration=True,
        needs_state=True,
        has_side_effects=True,
        risk="high",
    ),
}


def yes_no(value: bool) -> str:
    return "是" if value else "否"


def decide(scenario: Scenario) -> tuple[str, list[str], list[str]]:
    reasons: list[str] = []
    guardrails: list[str] = []

    if scenario.needs_dynamic_choice:
        reasons.append("下一步需要根据观察结果变化")
    if scenario.needs_iteration:
        reasons.append("任务需要多轮行动和反馈")
    if scenario.needs_state:
        reasons.append("系统需要维护任务状态")
    if scenario.needs_tools:
        reasons.append("系统需要调用外部工具")
    if scenario.needs_external_knowledge:
        reasons.append("系统需要使用外部资料")

    if scenario.has_side_effects:
        guardrails.append("写入、提交或发送类动作需要用户确认")
    if scenario.needs_iteration:
        guardrails.append("设置最大执行步数，避免无限循环")
    if scenario.needs_state:
        guardrails.append("记录状态字段，并说明哪些可以长期保存")
    if scenario.risk in {"medium", "high"}:
        guardrails.append("保存完整执行日志，便于复盘")
    if scenario.risk == "high":
        guardrails.append("默认人工确认高风险工具，不允许自动提交真实业务动作")

    if (
        scenario.needs_dynamic_choice
        and scenario.needs_iteration
        and scenario.needs_state
        and scenario.needs_tools
    ):
        if scenario.risk == "high":
            return "Agent 候选（高风险，必须人工确认）", reasons, guardrails
        return "Agent 候选", reasons, guardrails

    if scenario.needs_tools:
        return "Tool Calling 应用", reasons, guardrails

    if scenario.fixed_steps:
        if scenario.needs_external_knowledge:
            return "RAG 或固定工作流", reasons, guardrails
        return "固定工作流", reasons, guardrails

    return "普通 LLM 调用或 Chatbot", reasons, guardrails


def print_checklist(scenario: Scenario) -> None:
    rows = [
        ("步骤是否固定", scenario.fixed_steps),
        ("是否需要外部资料", scenario.needs_external_knowledge),
        ("是否需要工具", scenario.needs_tools),
        ("是否需要动态选择下一步", scenario.needs_dynamic_choice),
        ("是否需要多轮反馈", scenario.needs_iteration),
        ("是否需要维护状态", scenario.needs_state),
        ("是否有副作用", scenario.has_side_effects),
    ]

    print("\n判断清单")
    print("-" * 32)
    for label, value in rows:
        print(f"{label}: {yes_no(value)}")
    print(f"风险等级: {scenario.risk}")


def print_decision(scenario: Scenario, show_checklist: bool) -> None:
    recommendation, reasons, guardrails = decide(scenario)

    print(f"场景: {scenario.case_id}")
    print(f"标题: {scenario.title}")
    print(f"任务: {scenario.task}")

    if show_checklist:
        print_checklist(scenario)

    print("\n推荐形态")
    print("-" * 32)
    print(recommendation)

    print("\n判断依据")
    print("-" * 32)
    if reasons:
        for reason in reasons:
            print(f"- {reason}")
    else:
        print("- 任务可以一次性回答，不需要工具、状态或循环")

    print("\n第一版边界")
    print("-" * 32)
    if guardrails:
        for guardrail in guardrails:
            print(f"- {guardrail}")
    else:
        print("- 暂时不需要 Agent 边界，保持简单实现")


def main() -> None:
    parser = argparse.ArgumentParser(description="判断一个 AI 需求是否需要 Agent")
    parser.add_argument("--list", action="store_true", help="列出可用场景")
    parser.add_argument(
        "--case",
        choices=sorted(SCENARIOS.keys()),
        default="study-agent",
        help="选择一个内置场景",
    )
    parser.add_argument(
        "--show-checklist",
        action="store_true",
        help="显示判断清单",
    )
    args = parser.parse_args()

    if args.list:
        print("可用场景")
        print("-" * 32)
        for case_id, scenario in sorted(SCENARIOS.items()):
            print(f"{case_id}: {scenario.title}")
        return

    print_decision(SCENARIOS[args.case], args.show_checklist)


if __name__ == "__main__":
    main()
