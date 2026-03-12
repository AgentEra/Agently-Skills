from agently import Agently

agent = Agently.create_agent()
response = agent.input("Explain recursion briefly.").output({"answer": (str,)}).get_response()
print(response.result.get_data())
