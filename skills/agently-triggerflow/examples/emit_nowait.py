import asyncio

from agently import TriggerFlow

flow = TriggerFlow(name="nowait-emit-demo")


async def kick(data):
    await data.async_emit_nowait(
        "AUDIT",
        {
            "input": data.input,
            "queued_by": "kick",
        },
    )
    await data.async_set_state(
        "kick",
        {
            "input": data.input,
            "queued": True,
        },
    )
    return {"queued": True}


async def audit(data):
    await asyncio.sleep(0.05)
    await data.async_set_state(
        "audit",
        {
            "received": data.input["input"],
            "queued_by": data.input["queued_by"],
        },
    )
    return data.input


flow.to(kick)
flow.when("AUDIT").to(audit)


async def main():
    execution = flow.create_execution(auto_close=False)
    await execution.async_start("demo")
    state = await execution.async_close()
    assert state["kick"] == {"input": "demo", "queued": True}
    assert execution.result.get_state("audit") == {
        "received": "demo",
        "queued_by": "kick",
    }
    print({"audit": state["audit"], "meta": execution.result.get_meta()})


asyncio.run(main())
