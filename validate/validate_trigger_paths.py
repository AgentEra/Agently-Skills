#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "validate" / "fixtures" / "route_cases.json"


def check(name: str, condition: bool, details: str, failures: list[str], passes: list[str]) -> None:
    if condition:
        passes.append(f"{name}: {details}")
    else:
        failures.append(f"{name}: {details}")


def predict_route(query: str, installed_skills: list[str]) -> list[str]:
    q = query.lower()
    path: list[str] = []
    if "agently-playbook" in installed_skills:
        path.append("agently-playbook")

    if "langchain" in q or "langgraph" in q or "migrate" in q or "migration" in q:
        if "agently-migration-playbook" in installed_skills:
            path.append("agently-migration-playbook")
        if "langgraph" in q and "agently-langgraph-to-triggerflow" in installed_skills:
            path.append("agently-langgraph-to-triggerflow")
        elif "langchain" in q and "agently-langchain-to-agently" in installed_skills:
            path.append("agently-langchain-to-agently")
        return path

    workflow_terms = (
        "workflow",
        "branch",
        "concurrency",
        "resume",
        "runtime stream",
        "draft judge revise",
        "waiting and resume",
        "stop conditions",
    )
    if any(term in q for term in workflow_terms):
        if "agently-triggerflow" in installed_skills:
            path.append("agently-triggerflow")
        return path

    if any(term in q for term in ("deepseek", "ollama", "openaicompatible", "base url", "auth", "connect")):
        if "agently-model-setup" in installed_skills:
            path.append("agently-model-setup")
        return path

    if any(term in q for term in ("prompt config", "mappings", "input", "instruct", "placeholder")):
        if "agently-prompt-management" in installed_skills:
            path.append("agently-prompt-management")
        return path

    if any(term in q for term in ("session", "memo", "restore after restart", "continuity")):
        if "agently-session-memory" in installed_skills:
            path.append("agently-session-memory")
        return path

    if any(term in q for term in ("tool", "mcp", "fastapihelper", "fastapi", "keywaiter", "auto_func")):
        if "agently-agent-extensions" in installed_skills:
            path.append("agently-agent-extensions")
        return path

    if any(term in q for term in ("knowledge-base", "knowledge base", "chroma", "embeddings", "retrieval")):
        if "agently-knowledge-base" in installed_skills:
            path.append("agently-knowledge-base")
        return path

    if "agently-output-control" in installed_skills:
        path.append("agently-output-control")
    if "agently-model-response" in installed_skills and any(term in q for term in ("report", "response", "stream", "simulator", "stable")):
        path.append("agently-model-response")
    return path


def main() -> None:
    data = json.loads(FIXTURES.read_text(encoding="utf-8"))
    passes: list[str] = []
    failures: list[str] = []

    for case in data["cases"]:
        predicted = predict_route(case["query"], case["installed_skills"])
        expected = case["expected_route_path"]
        check(
            case["id"],
            predicted == expected,
            f"expected={expected} predicted={predicted}",
            failures,
            passes,
        )

    print("V2 trigger path validation")
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
