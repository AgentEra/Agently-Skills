from agently import TriggerFlow

flow = TriggerFlow()
flow.to(lambda data: {"stage": "done", "input": data.value}).end()
print(flow.start("demo"))
