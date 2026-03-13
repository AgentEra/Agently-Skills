from agently import Agently, TriggerFlow

agent = Agently.create_agent()
flow = TriggerFlow(name="status-and-actions")


def plan_step(data):
    response = (
        agent.input(f"Plan next actions for: {data.value}")
        .output({"status": (str,), "actions": [(str,)]})
        .get_response()
    )
    return {
        "status_text": response.result.get_text(),
        "plan": response.result.get_data(ensure_keys=["status", "actions[*]"], max_retries=1),
    }


def dispatch_step(data):
    return {
        "status": data.value["plan"]["status"],
        "actions": data.value["plan"]["actions"],
        "preview": data.value["status_text"],
    }


flow.to(plan_step).to(dispatch_step).end()
print(flow.start("demo"))
