#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
from pathlib import Path
from typing import Literal

from dotenv import find_dotenv, load_dotenv

from agently import Agently, TriggerFlow


load_dotenv(find_dotenv())
ROOT = Path(__file__).resolve().parents[1]
ROUTE_FIXTURES = ROOT / "validate" / "fixtures" / "route_cases.json"


def configure_deepseek() -> bool:
    base_url = os.environ.get("DEEPSEEK_BASE_URL")
    model = os.environ.get("DEEPSEEK_DEFAULT_MODEL")
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not all([base_url, model, api_key]):
        return False
    Agently.set_settings(
        "OpenAICompatible",
        {
            "base_url": base_url,
            "model": model,
            "auth": api_key,
            "request_options": {"temperature": 0},
        },
    )
    return True


def check(name: str, condition: bool, details: str, failures: list[str], passes: list[str]) -> None:
    if condition:
        passes.append(f"{name}: {details}")
    else:
        failures.append(f"{name}: {details}")


async def run_model_smoke(failures: list[str], passes: list[str]) -> None:
    agent = Agently.create_agent("v2-live-validator")
    response = (
        agent.input("Return answer=ok and one checklist item.")
        .output({"answer": (str,), "checklist": [(str,)]})
        .get_response()
    )
    try:
        data = await asyncio.wait_for(
            response.result.async_get_data(ensure_keys=["answer", "checklist[*]"], max_retries=1),
            timeout=60,
        )
        check(
            "deepseek_output_control",
            data.get("answer") and isinstance(data.get("checklist"), list),
            "DeepSeek-backed output control request succeeds",
            failures,
            passes,
        )
    except TimeoutError:
        failures.append("deepseek_output_control: timed out while waiting for DeepSeek-backed output control request")

    response_2 = agent.input("Explain recursion in one short sentence.").output({"answer": (str,)}).get_response()
    try:
        text = await asyncio.wait_for(response_2.result.async_get_text(), timeout=60)
        parsed = await asyncio.wait_for(response_2.result.async_get_data(), timeout=60)
        check(
            "deepseek_model_response",
            isinstance(text, str) and isinstance(parsed.get("answer"), str),
            "DeepSeek-backed response reuse succeeds",
            failures,
            passes,
        )
    except TimeoutError:
        failures.append("deepseek_model_response: timed out while waiting for DeepSeek-backed response reuse request")


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


async def judge_route_case(case: dict) -> dict:
    installed_skills = case["installed_skills"]
    descriptions = {
        skill_name: load_frontmatter_description(skill_name) for skill_name in installed_skills
    }
    installed_block = "\n".join(
        f"- {skill_name}: {descriptions[skill_name]}" for skill_name in installed_skills
    )
    allowed = ", ".join(installed_skills)

    prompt = (
        "You are simulating metadata-first skill routing.\n"
        "Use only each skill's name and frontmatter description.\n"
        "Do not assume access to the full SKILL body.\n"
        "The user does not need to mention Agently, TriggerFlow, or framework names explicitly.\n\n"
        f"User request:\n{case['query']}\n\n"
        "Installed skills and frontmatter descriptions:\n"
        f"{installed_block}\n\n"
        "Routing rules:\n"
        "- Return an ordered route path of 1 to 3 skills.\n"
        "- Choose only from the installed skills.\n"
        "- Match by scenario, capability, and problem shape first.\n"
        "- Set decision=sure only when the route path is clearly supported by the metadata and the best alternative skills are meaningfully worse.\n"
        "- Set decision=unsure when the metadata overlap is still high or the boundary is not explicit enough.\n"
        "- If the request starts from a generic product or workflow scenario, or the owner layer is unresolved, include agently-playbook first when it is installed.\n"
        "- If the request explicitly says the owner layer is not decided yet, do not route past agently-playbook.\n"
        "- Mentions of possible capabilities such as tools, memory, approvals, streaming, or retrieval do not justify a later skill when the owner layer is still undecided.\n"
        "- Mentions of a UI, web page, desktop shell, or local model service such as Ollama are supporting constraints and do not disqualify agently-playbook when the request is still about building a model-powered tool.\n"
        "- If one installed non-playbook skill directly and narrowly owns the request, prefer that leaf skill without agently-playbook.\n"
        "- If the request is still unresolved between one request family and workflow orchestration, stop at agently-playbook.\n"
        "- If the request clearly stays inside one request family and asks for stable structured fields, required keys, or machine-readable reports, continue with agently-output-control when installed.\n"
        "- If the same request also needs response reuse, metadata consumption, or partial structured updates, continue with agently-model-response when installed.\n"
        "- If the request clearly needs branching, concurrency, approvals, waiting and resume, runtime stream, or explicit draft-review-revise loops, continue with agently-triggerflow when installed.\n"
        "- If the request is mainly provider wiring or connectivity, continue with agently-model-setup when installed.\n"
        f"- Every item in route_path must be exactly one of: {allowed}.\n"
    )

    agent = Agently.create_agent(f"v2-route-live-{case['id']}")
    response = (
        agent
        .input(prompt)
        .output(
            {
                "decision": (
                    Literal["sure", "unsure"],
                    "Routing confidence. Use sure only when metadata boundaries clearly support the chosen path.",
                ),
                "route_path": [(str, f"Exact skill name. Must be one of: {allowed}.")],
                "reason": (str, "Short explanation of why this route path is correct."),
                "evidence": [(str, "Short metadata evidence supporting the selected route.")],
            }
        )
        .get_response()
    )
    data = await response.result.async_get_data(
        ensure_keys=["decision", "route_path[*]", "reason", "evidence[*]"],
        max_retries=1,
    )
    data["decision"] = str(data["decision"]).strip().lower()
    data["route_path"] = [normalize_skill_name(item) for item in data["route_path"]]
    return data


async def validate_route_case(case: dict, *, timeout_seconds: int) -> dict:
    case_name = f"route_{case['id']}"
    try:
        judged = await asyncio.wait_for(judge_route_case(case), timeout=timeout_seconds)
    except TimeoutError:
        return {
            "name": case_name,
            "ok": False,
            "details": f"timed out after {timeout_seconds}s",
        }
    except Exception as exc:
        return {
            "name": case_name,
            "ok": False,
            "details": f"raised {type(exc).__name__}: {exc}",
        }

    expected_paths = case["expected_route_paths"]
    predicted = judged["route_path"]
    return {
        "name": case_name,
        "ok": judged["decision"] == "sure" and predicted in expected_paths,
        "details": (
            f"expected={expected_paths} predicted={predicted} decision={judged['decision']} "
            f"reason={judged['reason']} evidence={judged['evidence']}"
        ),
    }


async def run_route_live_validation(
    failures: list[str],
    passes: list[str],
    *,
    timeout_seconds: int,
    concurrency: int,
) -> None:
    fixtures = json.loads(ROUTE_FIXTURES.read_text(encoding="utf-8"))["cases"]
    flow = TriggerFlow(name="v2-live-route-validation")

    async def validate_in_flow(data):
        return await validate_route_case(data.value, timeout_seconds=timeout_seconds)

    flow.for_each(concurrency=concurrency).to(validate_in_flow).end_for_each().end()
    results = await flow.async_start(fixtures)

    for result in results:
        check(result["name"], result["ok"], result["details"], failures, passes)

async def main() -> None:
    parser = argparse.ArgumentParser(description="Run V2 live validation scenarios.")
    parser.add_argument("--require-model", action="store_true", help="Fail if DeepSeek settings are missing.")
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=60,
        help="Per-request timeout for model-backed route simulation.",
    )
    parser.add_argument(
        "--route-concurrency",
        type=int,
        default=4,
        help="Concurrent TriggerFlow workers for route-case validation.",
    )
    args = parser.parse_args()

    passes: list[str] = []
    failures: list[str] = []

    if configure_deepseek():
        await run_model_smoke(failures, passes)
        await run_route_live_validation(
            failures,
            passes,
            timeout_seconds=args.timeout_seconds,
            concurrency=args.route_concurrency,
        )
    else:
        missing = ["DEEPSEEK_BASE_URL", "DEEPSEEK_DEFAULT_MODEL", "DEEPSEEK_API_KEY"]
        if args.require_model:
            failures.append(f"deepseek_env: missing one or more required vars {missing}")
        else:
            passes.append(f"deepseek_env: skipped model-backed smoke because vars are not fully set {missing}")

    print("V2 live scenario validation")
    print(f"passes: {len(passes)}")
    for item in passes:
        print(f"PASS  {item}")
    print(f"failures: {len(failures)}")
    for item in failures:
        print(f"FAIL  {item}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
