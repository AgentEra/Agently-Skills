from agently import Agently

agent = Agently.create_agent()

result = (
    agent
    .input("Classify this production incident.")
    .instruct(
        "Return status exactly 'ready'. Classify severity as exactly one of "
        "P0, P1, P2, or P3."
    )
    .output(
        {
            "status": (str, "Exactly 'ready'", "not_null"),
            "severity": (str, "Exactly one of P0 | P1 | P2 | P3", "not_null"),
        }
    )
    .get_result()
)

data = result.get_data(
    validate_handler=lambda result, context: (
        result["status"] == "ready"
        and result["severity"] in {"P0", "P1", "P2", "P3"}
    ),
    max_retries=2,
)

print(data)
