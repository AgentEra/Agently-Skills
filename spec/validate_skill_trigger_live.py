#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

from agently import Agently


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "spec" / "skill-trigger-fixtures.json"
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
OLLAMA_CHAT_MODEL = os.environ.get("OLLAMA_CHAT_MODEL", "qwen2.5:latest")


def check(name: str, condition: bool, details: str, failures: list[str], passes: list[str]):
    if condition:
        passes.append(f"{name}: {details}")
    else:
        failures.append(f"{name}: {details}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate skill-trigger fixtures through Agently + a local Ollama judge."
    )
    parser.add_argument("--group", help="Only evaluate one fixture group")
    parser.add_argument("--case", dest="case_id", help="Only evaluate one fixture id")
    parser.add_argument("--temperature", type=float, default=0.1, help="Judge temperature")
    parser.add_argument("--max-retries", type=int, default=1, help="Structured-output retries")
    return parser


def configure_judge() -> None:
    Agently.set_settings(
        "OpenAICompatible",
        {
            "base_url": OLLAMA_BASE_URL,
            "model": OLLAMA_CHAT_MODEL,
            "model_type": "chat",
            "auth": "nothing",
        },
    )


def load_frontmatter_description(skill_name: str) -> str:
    skill_md = ROOT / "skills" / skill_name / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if frontmatter is None:
        raise RuntimeError(f"Missing frontmatter in {skill_md}")
    block = frontmatter.group(1)
    match = re.search(r"^description:\s*(.+)$", block, re.MULTILINE)
    if match is None:
        raise RuntimeError(f"Missing description in {skill_md}")
    return match.group(1).strip()


def normalize_skill_name(value: str) -> str:
    return value.strip().strip("`").strip().split()[0]


def judge_case(case: dict, *, temperature: float, max_retries: int) -> dict:
    installed_skills = case["installed_skills"]
    descriptions = {
        skill_name: load_frontmatter_description(skill_name) for skill_name in installed_skills
    }
    installed_block = "\n".join(
        f"- {skill_name}: {descriptions[skill_name]}" for skill_name in installed_skills
    )
    allowed = ", ".join(installed_skills)

    prompt = (
        "You are evaluating which Agently skill should trigger from frontmatter metadata only.\n\n"
        f"User request:\n{case['query']}\n\n"
        "Installed skills and frontmatter descriptions:\n"
        f"{installed_block}\n\n"
        "Selection rules:\n"
        "- Choose the single best trigger winner from the installed skills only.\n"
        "- Match by scenario, capability, and problem shape first. Do not require the user to mention internal framework names.\n"
        "- Treat words such as Agently or TriggerFlow as supporting confirmation terms rather than mandatory query tokens.\n"
        "- Prefer the narrowest skill whose description already matches the request.\n"
        "- Prefer a router only when the request is still unresolved at that router's level.\n"
        "- If the request already names a concrete implementation surface, do not choose a broader router.\n"
        f"- The winner must be exactly one of: {allowed}.\n"
    )

    agent = Agently.create_agent(f"skill-trigger-live-{case['id']}")
    response = (
        agent
        .input(prompt)
        .output(
            {
                "winner": (str, f"One skill name only. Must be exactly one of: {allowed}."),
                "confidence": (str, "low, medium, or high"),
                "reason": (str, "Short explanation of why this skill wins."),
            }
        )
        .options({"temperature": temperature})
        .get_response()
    )
    data = response.result.get_data(
        ensure_keys=["winner", "confidence", "reason"],
        max_retries=max_retries,
    )
    data["winner"] = normalize_skill_name(data["winner"])
    return data


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))["cases"]
    if args.group:
        fixtures = [case for case in fixtures if case["group"] == args.group]
    if args.case_id:
        fixtures = [case for case in fixtures if case["id"] == args.case_id]
    if not fixtures:
        raise SystemExit("No fixtures matched the requested filter.")

    configure_judge()

    passes: list[str] = []
    failures: list[str] = []
    print("Skill trigger live validation")
    print(f"base_url: {OLLAMA_BASE_URL}")
    print(f"chat_model: {OLLAMA_CHAT_MODEL}")
    print(f"cases: {len(fixtures)}")

    for case in fixtures:
        judged = judge_case(case, temperature=args.temperature, max_retries=args.max_retries)
        expected = case["should_trigger"]
        predicted = judged["winner"]
        detail = (
            f"expected={expected} predicted={predicted} confidence={judged['confidence']} "
            f"reason={judged['reason']}"
        )
        check(case["id"], predicted == expected, detail, failures, passes)

    print(f"passes: {len(passes)}")
    for item in passes:
        name, details = item.split(": ", 1)
        print(f"PASS  {name}: {details}")
    print(f"failures: {len(failures)}")
    for item in failures:
        name, details = item.split(": ", 1)
        print(f"FAIL  {name}: {details}")

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
