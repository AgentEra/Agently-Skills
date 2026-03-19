from agently import Agently, TriggerFlow

agent = Agently.create_agent()
flow = TriggerFlow(name="stream-bridge-demo")


def item_is_complete(item):
    return isinstance(item, dict) and {"name", "score", "comment"}.issubset(item.keys())


@flow.chunk("judge")
async def judge(data):
    response = (
        agent.input(f"Score this draft and explain strengths: {data.value}")
        .output({"judge_items": [{"name": (str,), "score": (int,), "comment": (str,)}]})
        .get_response()
    )

    partial = {"judge_items": []}
    emitted = set()

    async for msg in response.get_async_generator(type="instant"):
        path = getattr(msg, "path", None) or getattr(msg, "wildcard_path", None)
        if not path or not path.startswith("judge_items."):
            continue
        parts = path.split(".")
        if len(parts) != 3 or not parts[1].isdigit():
            continue
        index = int(parts[1])
        field = parts[2]
        while len(partial["judge_items"]) <= index:
            partial["judge_items"].append({})
        partial["judge_items"][index][field] = getattr(msg, "value", None) or getattr(msg, "delta", None)
        if index not in emitted and item_is_complete(partial["judge_items"][index]):
            emitted.add(index)
            await data.async_put_into_stream(
                {
                    "stage": "judge_item_ready",
                    "index": index,
                    "item": partial["judge_items"][index],
                }
            )

    return await response.result.async_get_data()


flow.to(judge).end()
