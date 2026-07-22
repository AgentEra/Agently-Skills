import asyncio

from agently import TriggerFlow


child_entered = asyncio.Event()
release_child = asyncio.Event()
child_side_effects: list[str] = []
parent_continuations: list[str] = []

child = TriggerFlow(name="controlled-child")


async def child_work(data):
    child_entered.set()
    await release_child.wait()
    child_side_effects.append(f"committed:{data.value}")


child.to(child_work)

parent = TriggerFlow(name="controlling-parent")
parent.to_sub_flow(child).to(lambda data: parent_continuations.append(data.value))


async def main():
    execution = parent.create_execution(auto_close=False)
    start_task = asyncio.create_task(execution.async_start("older-run"))

    try:
        await child_entered.wait()

        async def wait_for_running_frame():
            while not execution.get_sub_flow_frames():
                await asyncio.sleep(0)
            return next(iter(execution.get_sub_flow_frames().items()))

        frame_id, running_frame = await asyncio.wait_for(
            wait_for_running_frame(),
            timeout=1,
        )
        assert running_frame["status"] == "running"

        won = await execution.async_cancel_sub_flow(
            frame_id,
            reason="superseded",
        )
        release_child.set()
        await start_task

        cancelled_frame = execution.get_sub_flow_frames()[frame_id]
        summary = {
            "cancel_won": won,
            "frame_status": cancelled_frame["status"],
            "child_side_effects": child_side_effects,
            "parent_continuations": parent_continuations,
            "parent_open": execution.is_open(),
        }
        assert summary == {
            "cancel_won": True,
            "frame_status": "cancelled",
            "child_side_effects": [],
            "parent_continuations": [],
            "parent_open": True,
        }
        print(summary)
    finally:
        release_child.set()
        await asyncio.gather(start_task, return_exceptions=True)
        await execution.async_close()


# Expected key output from a local Agently 4.1.4.2 run:
# {'cancel_won': True, 'frame_status': 'cancelled', 'child_side_effects': [],
#  'parent_continuations': [], 'parent_open': True}
asyncio.run(main())
