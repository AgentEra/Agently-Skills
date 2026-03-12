#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "validate" / "fixtures" / "implementation_cases.json"


def check(name: str, condition: bool, details: str, failures: list[str], passes: list[str]) -> None:
    if condition:
        passes.append(f"{name}: {details}")
    else:
        failures.append(f"{name}: {details}")


def main() -> None:
    data = json.loads(FIXTURES.read_text(encoding="utf-8"))
    passes: list[str] = []
    failures: list[str] = []

    for case in data["cases"]:
        example_path = ROOT / case["reference_example"]
        check(case["id"] + "_example", example_path.exists(), "reference example exists", failures, passes)
        if not example_path.exists():
            continue
        content = example_path.read_text(encoding="utf-8")
        for required in case["required_primitives"]:
            check(
                f"{case['id']}_{required}",
                required in content,
                f"required primitive {required} is present",
                failures,
                passes,
            )
        for forbidden in case["forbidden_antipatterns"]:
            check(
                f"{case['id']}_not_{forbidden}",
                forbidden not in content,
                f"forbidden anti-pattern {forbidden} is absent",
                failures,
                passes,
            )
        check(
            f"{case['id']}_profile",
            case["live_smoke_profile"] in {"deepseek", "local"},
            "live smoke profile is valid",
            failures,
            passes,
        )

    print("V2 native usage validation")
    print(f"passes: {len(passes)}")
    for item in passes:
        print(f"PASS  {item}")
    print(f"failures: {len(failures)}")
    for item in failures:
        print(f"FAIL  {item}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
