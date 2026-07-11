#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "validate" / "fixtures" / "implementation_cases.json"
TRIGGERFLOW_EXAMPLES = ROOT / "skills" / "agently-triggerflow" / "examples"
AGENTLY_ROOT = ROOT.parent / "Agently"
SUBMITTED_DAG_EXAMPLES = [
    AGENTLY_ROOT / "examples" / "cookbook" / "03_todo_concurrent_model.py",
    AGENTLY_ROOT / "examples" / "step_by_step" / "12-patterns-02_todo_concurrent.py",
]
REAL_MODEL_PROVIDER_TOKENS = {
    "03_todo_concurrent_model": ["configure_model("],
    "12-patterns-02_todo_concurrent": ["DEEPSEEK_API_KEY", "OLLAMA_BASE_URL"],
}
TRIGGERFLOW_LEGACY_ALLOWLIST: set[Path] = set()
DEPRECATED_TRIGGERFLOW_TOKENS = [
    ".end(",
    ".start(",
    "set_result(",
    "get_runtime_data(",
    "set_runtime_data(",
    "append_runtime_data(",
    "del_runtime_data(",
    "get_flow_data(",
    "set_flow_data(",
    "append_flow_data(",
    "del_flow_data(",
    "get_runtime_stream(",
]
DEPRECATED_TRIGGERFLOW_PATTERNS = [
    ("execution.get_result(", re.compile(r"\bexecution\.get_result\(")),
    ("execution.async_get_result(", re.compile(r"\bexecution\.async_get_result\(")),
]


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
            if required == "tuple_ensure":
                condition = re.search(r"\([^)\n]+,\s*True\)", content) is not None
                details = "required primitive tuple ensure is present"
            else:
                condition = required in content
                details = f"required primitive {required} is present"
            check(
                f"{case['id']}_{required}",
                condition,
                details,
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

    for example_path in sorted(TRIGGERFLOW_EXAMPLES.glob("*.py")):
        relative_path = example_path.relative_to(ROOT)
        if relative_path in TRIGGERFLOW_LEGACY_ALLOWLIST:
            continue
        content = example_path.read_text(encoding="utf-8")
        for token in DEPRECATED_TRIGGERFLOW_TOKENS:
            check(
                f"triggerflow_examples_no_deprecated_{example_path.stem}_{token}",
                token not in content,
                f"recommended TriggerFlow example does not use deprecated token {token}",
                failures,
                passes,
            )
        for name, pattern in DEPRECATED_TRIGGERFLOW_PATTERNS:
            check(
                f"triggerflow_examples_no_deprecated_{example_path.stem}_{name}",
                pattern.search(content) is None,
                f"recommended TriggerFlow example does not use deprecated lifecycle call {name}",
                failures,
                passes,
            )
        check(
            f"triggerflow_examples_close_{example_path.stem}",
            "async_close" in content or ".close(" in content,
            "recommended TriggerFlow example uses explicit execution close",
            failures,
            passes,
        )

    if AGENTLY_ROOT.exists():
        for example_path in SUBMITTED_DAG_EXAMPLES:
            check(
                f"submitted_dag_example_{example_path.stem}_exists",
                example_path.exists(),
                "submitted TaskDAG example exists",
                failures,
                passes,
            )
            if not example_path.exists():
                continue
            content = example_path.read_text(encoding="utf-8")
            syntax_tree = ast.parse(content)
            submitted_plan = None
            for node in syntax_tree.body:
                if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                    continue
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                if any(isinstance(target, ast.Name) and target.id == "SUBMITTED_PLAN" for target in targets):
                    submitted_plan = ast.literal_eval(node.value)
                    break
            submitted_tasks = (
                submitted_plan.get("tasks", []) if isinstance(submitted_plan, dict) else []
            )
            check(
                f"submitted_dag_example_{example_path.stem}_uses_dynamic_task",
                "Agently.create_dynamic_task(" in content and "plan=SUBMITTED_PLAN" in content,
                "submitted TaskDAG example uses the DynamicTask facade with an explicit plan",
                failures,
                passes,
            )
            check(
                f"submitted_dag_example_{example_path.stem}_all_tasks_use_real_model",
                bool(submitted_tasks)
                and all(
                    isinstance(task, dict)
                    and task.get("kind") == "model"
                    and "binding" not in task
                    for task in submitted_tasks
                )
                and "handlers=" not in content
                and all(
                    token in content
                    for token in REAL_MODEL_PROVIDER_TOKENS[example_path.stem]
                ),
                "submitted TaskDAG example keeps every node model-owned and configures a real provider",
                failures,
                passes,
            )
            check(
                f"submitted_dag_example_{example_path.stem}_no_ad_hoc_runtime_compiler",
                "while pending" not in content
                and "asyncio.gather(" not in content
                and "TriggerFlow(" not in content
                and ".async_plan(" not in content,
                "submitted TaskDAG example avoids manual readiness and runtime graph compilation",
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
