from agently import Agently

agent = Agently.create_agent()
result = (
    agent
    .input("Summarize the repository and identify concrete risks.")
    .instruct("The summary must contain non-whitespace text.")
    .output(
        {
            "summary": (str, "Non-empty repository summary", "not_null"),
            "risks": [(str, "Concrete repository risk", True)],
        }
    )
    .validate(lambda result, context: len(result["summary"].strip()) > 0)
    .start(max_retries=1)
)
print(result)
