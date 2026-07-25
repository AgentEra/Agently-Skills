import asyncio
import hashlib
import json

from agently import Agently, TriggerFlow

MAX_RETRIEVAL_TASKS = 4
agent = Agently.create_agent()
flow = TriggerFlow(name="instant-retrieval-overlap")


def task_key(task: dict) -> str:
    payload = json.dumps(task, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def validate_plan(plan, _context):
    tasks = plan.get("retrieval_tasks", [])
    keys = [task_key(task) for task in tasks]
    if 1 <= len(tasks) <= MAX_RETRIEVAL_TASKS and len(keys) == len(set(keys)):
        return True
    return {
        "ok": False,
        "reason": "retrieval_tasks must contain 1 to 4 unique items",
    }


@flow.chunk("retrieve")
async def retrieve(data):
    # Replace this read-only demo adapter with the application's search Action.
    await asyncio.sleep(0.1)
    task = data.input["task"]
    result = {"query": task["query"], "hits": [{"title": "Demo result"}]}
    await data.async_set_state(f"retrieval:{data.input['key']}", result)
    return result


@flow.chunk("plan")
async def plan(data):
    result = (
        agent
        .input({"question": data.input})
        .instruct(
            "Emit 1 to 4 independent retrieval tasks first, then a short "
            "user-safe progress message and the answer plan."
        )
        .output(
            {
                "retrieval_tasks": [
                    {
                        "query": (str, "One focused retrieval query", True),
                        "purpose": (str, "Why the answer needs this evidence", True),
                    }
                ],
                "progress_message": (str, "Short user-safe progress explanation", True),
                "answer_plan": [(str, "Answer section using retrieved evidence", True)],
            },
            format="json",
        )
        .validate(validate_plan)
        .get_result()
    )

    started = {}

    async def start_once(task):
        key = task_key(task)
        if key not in started and len(started) < MAX_RETRIEVAL_TASKS:
            started[key] = await data.async_emit_nowait(
                "RETRIEVE",
                {"key": key, "task": task},
            )
        return key

    async for item in result.get_async_generator(type="instant"):
        if (
            item.wildcard_path == "retrieval_tasks[*]"
            and item.is_complete
            and isinstance(item.value, dict)
        ):
            await start_once(item.value)
        elif item.path == "progress_message" and item.delta:
            await data.async_put_into_stream(
                {"stage": "planning", "delta": item.delta, "provisional": True}
            )

    final = await result.async_get_data(max_retries=1)
    accepted = {task_key(task): task for task in final["retrieval_tasks"]}

    extra_handles = [handle for key, handle in started.items() if key not in accepted]
    for handle in extra_handles:
        if handle is not None:
            handle.cancel()
    await asyncio.gather(
        *(handle for handle in extra_handles if handle is not None),
        return_exceptions=True,
    )
    started = {key: handle for key, handle in started.items() if key in accepted}

    for task in accepted.values():
        await start_once(task)

    await asyncio.gather(
        *(started[key] for key in accepted if started[key] is not None),
    )

    final_result = {
        "plan": final,
        "retrievals": [
            data.get_state(f"retrieval:{key}", inherit=False) for key in accepted
        ],
    }
    await data.async_set_state("final_result", final_result)
    return final_result


flow.to(plan)
flow.when("RETRIEVE").to(retrieve)


async def main():
    execution = flow.create_execution(auto_close=False, concurrency=4)
    await execution.async_start("What should our support team investigate?")
    state = await execution.async_close()
    print(state["final_result"])


if __name__ == "__main__":
    asyncio.run(main())
