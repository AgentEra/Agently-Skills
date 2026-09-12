import asyncio
import os

from agently import Agently, TriggerFlow

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY", "ollama")


Agently.set_settings(
    "plugins.ModelRequester.OpenAICompatible",
    {
        "base_url": OLLAMA_BASE_URL,
        "api_key": OLLAMA_API_KEY,
        "model": OLLAMA_MODEL,
        "model_type": "chat",
        "request_options": {"temperature": 0},
    },
)

flow = TriggerFlow(name="plan-response-fanout")


def validate_plan(plan, _context):
    status = plan.get("status")
    actions = plan.get("actions", [])
    valid_actions = (
        isinstance(actions, list)
        and 1 <= len(actions) <= 4
        and all(isinstance(item, str) and item.strip() for item in actions)
        and len(set(actions)) == len(actions)
    )
    if status in {"ready", "needs_info"} and valid_actions:
        return True
    return {
        "ok": False,
        "reason": (
            "status must be ready or needs_info; actions must contain 1 to 4 "
            "unique non-empty steps"
        ),
    }


async def plan_step(data):
    result = (
        Agently.create_agent()
        .input({"delivery_request": data.input})
        .info(
            {
                "planning_contract": {
                    "status_values": ["ready", "needs_info"],
                    "action_count": {"minimum": 1, "maximum": 4},
                    "actions_must_be_unique": True,
                }
            }
        )
        .instruct(
            "Assess whether the request has enough information, then propose "
            "specific next actions that obey the planning contract."
        )
        .output(
            {
                "status": (str, "ready or needs_info", True),
                "actions": [(str, "One concrete next action", True)],
            },
            format="json",
        )
        .validate(validate_plan)
        .get_result()
    )
    return await result.async_get_data(max_retries=1)


async def status_view(data):
    return {"status": data.input["status"]}


async def action_view(data):
    return {
        "actions": data.input["actions"],
        "count": len(data.input["actions"]),
    }


async def store_views(data):
    await data.async_set_state("views", data.input)
    return data.input


(
    flow.to(plan_step)
    .batch(
        ("status_view", status_view),
        ("action_view", action_view),
        concurrency=2,
    )
    .to(store_views)
)


async def main():
    execution = flow.create_execution()
    await execution.async_start(
        "Prepare the release notes and verification checklist for tomorrow."
    )
    snapshot = await execution.async_close()
    views = snapshot["views"]
    assert set(views) == {"status_view", "action_view"}
    assert views["status_view"]["status"] in {"ready", "needs_info"}
    assert views["action_view"]["count"] == len(views["action_view"]["actions"])
    print({"views": views, "meta": execution.result.get_meta()})


asyncio.run(main())

# Expected key output invariant:
# views has independent status_view and action_view results produced by one
# ModelRequest result fanning out through a two-branch TriggerFlow batch.
