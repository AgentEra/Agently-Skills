from __future__ import annotations

import importlib.util
from pathlib import Path


VALIDATOR_PATH = Path(__file__).with_name("validate_reference_retrieval.py")


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_reference_retrieval",
        VALIDATOR_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_model_validation_requires_explicit_cli_authorization() -> None:
    validator = _load_validator()
    parser = validator.build_parser()

    assert validator.model_validation_authorized(parser.parse_args([])) is False
    assert (
        validator.model_validation_authorized(
            parser.parse_args(["--allow-model-calls"]),
        )
        is False
    )
    assert (
        validator.model_validation_authorized(
            parser.parse_args(
                ["--allow-model-calls", "--max-model-requests", "24"],
            ),
        )
        is True
    )


def test_default_validation_never_configures_or_calls_a_model(monkeypatch) -> None:
    validator = _load_validator()

    def fail_if_called() -> bool:
        raise AssertionError("default validation must not inspect model configuration")

    monkeypatch.setattr(validator, "configure_deepseek", fail_if_called)

    validator.run([])
