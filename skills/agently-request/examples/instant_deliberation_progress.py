import asyncio

from agently import Agently

agent = Agently.create_agent()


async def generate_system_map(topic: str):
    result = (
        agent
        .input({"topic": topic})
        .instruct(
            "Create a bounded generation plan, then a short user-safe progress "
            "message, then the final system map. Do not expose hidden reasoning."
        )
        .output(
            {
                "generation_plan": {
                    "sections": [(str, "Section required by the final map", True)],
                    "risk_checks": [(str, "Check applied to the final map", True)],
                },
                "progress_message": (str, "Short user-safe status explanation", True),
                "system_map": {
                    "nodes": [
                        {
                            "name": (str, "Component name", True),
                            "responsibility": (str, "Owned responsibility", True),
                        }
                    ],
                    "edges": [
                        {
                            "source": (str, "Source component", True),
                            "target": (str, "Target component", True),
                            "contract": (str, "Information or signal contract", True),
                        }
                    ],
                },
            },
            format="json",
        )
        .get_result()
    )

    map_started = False
    async for item in result.get_async_generator(type="instant"):
        if item.path == "generation_plan" and item.is_complete:
            print({"stage": "plan_ready", "plan": item.value})
        elif item.path.startswith("system_map") and not map_started:
            map_started = True
            print({"stage": "generating_system_map"})
        elif item.path == "progress_message" and item.delta:
            print({"stage": "progress", "delta": item.delta})
        elif (
            item.path == "$status"
            and isinstance(item.value, dict)
            and item.value.get("status") == "streaming_parse_deferred"
        ):
            print({"stage": "progress_deferred"})

    return await result.async_get_data()


if __name__ == "__main__":
    asyncio.run(generate_system_map("A retrieval-backed support service"))
