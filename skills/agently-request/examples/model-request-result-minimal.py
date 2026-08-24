from agently import Agently

request = Agently.create_request()
result = (
    request
    .input("Explain recursion briefly.")
    .output({"answer": (str, "Brief explanation", "not_null")})
    .get_result()
)
print(result.get_data())
