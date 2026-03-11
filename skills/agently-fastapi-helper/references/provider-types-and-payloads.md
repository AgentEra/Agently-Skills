# Provider Types And Payloads

Use this page when the main problem is what sits behind `FastAPIHelper`.

## 1. Supported Provider Shapes

`FastAPIHelper` can wrap:

- `BaseAgent`
- `ModelRequest`
- `TriggerFlow`
- `TriggerFlowExecution`
- generator or async-generator functions

## 2. Standard Request Payload

The helper expects a JSON object with:

- `data`
- `options`

Typical shape:

```json
{
  "data": {
    "input": "hello"
  },
  "options": {}
}
```

For ordinary providers, `data` can be any request payload that the wrapped provider understands.

For TriggerFlow providers with `set_contract(initial_input=...)`:

- POST routes can expose `data` as the contract's typed initial input model
- invalid POST bodies can be rejected by FastAPI request validation before the helper wrapper runs

## 3. How Request Data Is Applied

For `BaseAgent` and `ModelRequest`, Agently maps known keys onto matching methods first and sends any remaining values through `input(...)`.

For `TriggerFlow` and `TriggerFlowExecution`, request data becomes the flow input.

For contract-backed `TriggerFlow` and `TriggerFlowExecution` providers:

- `POST` can use the TriggerFlow `initial_input` contract as the typed request-body schema
- the default wrapped response can use the TriggerFlow `result` contract as the typed `data` schema
- OpenAPI can expose `x-agently-triggerflow-contract` metadata

For `GET`, `SSE`, and `WebSocket`, the helper still exposes the provider through their route forms, but contract support is most visible in POST request-body typing and OpenAPI metadata.

For generator providers, request data is passed to the generator function directly.
