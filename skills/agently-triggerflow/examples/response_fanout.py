import asyncio
import os

from agently import Agently, TriggerFlow

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY", "ollama")
USE_LIVE_MODEL = bool(os.getenv("AGENTLY_TRIGGERFLOW_USE_LIVE_MODEL"))
# Default path: local Ollama qwen2.5:7b. Live mode is opt-in and uses explicit AGENTLY_TRIGGERFLOW_LIVE_* env vars.


def configure_model():
    if USE_LIVE_MODEL:
        base_url = os.environ.get("AGENTLY_TRIGGERFLOW_LIVE_BASE_URL")
        model = os.environ.get("AGENTLY_TRIGGERFLOW_LIVE_MODEL")
        api_key = os.environ.get("AGENTLY_TRIGGERFLOW_LIVE_API_KEY")
        if not base_url or not model or not api_key:
            raise RuntimeError(
                "Enable live mode only after setting AGENTLY_TRIGGERFLOW_LIVE_BASE_URL, "
                "AGENTLY_TRIGGERFLOW_LIVE_MODEL, and AGENTLY_TRIGGERFLOW_LIVE_API_KEY."
            )
        Agently.set_settings(
            "OpenAICompatible",
            {
                "base_url": base_url,
                "api_key": api_key,
                "model": model,
                "model_type": "chat",
                "request_options": {"temperature": 0},
            },
        )
        return

    Agently.set_settings(
        "OpenAICompatible",
        {
            "base_url": OLLAMA_BASE_URL,
            "api_key": OLLAMA_API_KEY,
            "model": OLLAMA_MODEL,
            "model_type": "chat",
            "request_options": {"temperature": 0},
        },
    )


configure_model()

flow = TriggerFlow(name="status-and-actions")


async def plan_step(data):
    agent = Agently.create_agent()
    agent.role(
        "Return JSON only. status must be exactly ready. actions must be exactly the three strings draft, review, ship.",
        always=True,
    )
    result = (
        agent.input(f"Plan next actions for: {data.input}")
        .output({"status": (str, None, True), "actions": [(str, None, True)]})
        .get_result()
    )
    return {
        "status_text": await result.async_get_text(),
        "plan": await result.async_get_data(max_retries=1),
    }


async def dispatch_step(data):
    output = {
        "status": data.input["plan"]["status"],
        "actions": data.input["plan"]["actions"],
        "preview": data.input["status_text"],
    }
    await data.async_set_state("dispatch", output)
    return output


flow.to(plan_step).to(dispatch_step)


async def main():
    execution = flow.create_execution()
    await execution.async_start("demo")
    snapshot = await execution.async_close()
    dispatch = execution.result.get_state("dispatch")
    assert dispatch["status"] == "ready"
    assert dispatch["actions"] == ["draft", "review", "ship"]
    assert isinstance(dispatch["preview"], str) and dispatch["preview"].strip()
    print({"dispatch": snapshot["dispatch"], "meta": execution.result.get_meta()})


asyncio.run(main())
