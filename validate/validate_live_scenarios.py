#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import os

from dotenv import find_dotenv, load_dotenv

from agently import Agently, TriggerFlow


load_dotenv(find_dotenv())


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
    data = await response.result.async_get_data(ensure_keys=["answer", "checklist[*]"], max_retries=1)
    check(
        "deepseek_output_control",
        data.get("answer") and isinstance(data.get("checklist"), list),
        "DeepSeek-backed output control request succeeds",
        failures,
        passes,
    )

    response_2 = agent.input("Explain recursion in one short sentence.").output({"answer": (str,)}).get_response()
    text = await response_2.result.async_get_text()
    parsed = await response_2.result.async_get_data()
    check(
        "deepseek_model_response",
        isinstance(text, str) and isinstance(parsed.get("answer"), str),
        "DeepSeek-backed response reuse succeeds",
        failures,
        passes,
    )


def run_triggerflow_smoke(failures: list[str], passes: list[str]) -> None:
    flow = TriggerFlow()
    flow.to(lambda data: {"ok": True, "value": data.value}).end()
    result = flow.start("demo")
    check(
        "triggerflow_smoke",
        isinstance(result, dict) and result.get("ok") is True,
        "TriggerFlow smoke succeeds",
        failures,
        passes,
    )


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run V2 live validation scenarios.")
    parser.add_argument("--require-model", action="store_true", help="Fail if DeepSeek settings are missing.")
    args = parser.parse_args()

    passes: list[str] = []
    failures: list[str] = []
    run_triggerflow_smoke(failures, passes)

    if configure_deepseek():
        await run_model_smoke(failures, passes)
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
