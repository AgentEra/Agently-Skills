# Service Recipes

Use this page for the most common helper patterns.

## 1. Simple Agent Endpoint

Choose an `agent` provider when:

- one request maps to one agent response
- the service should expose chat or structured output quickly
- GET or POST is enough

## 2. Streamed TriggerFlow Endpoint

Choose a `TriggerFlow` or `TriggerFlowExecution` provider when:

- the service should emit runtime-stream events
- the workflow does more than a single model call
- SSE is the natural client contract

If the TriggerFlow also uses `set_contract(...)`:

- POST can expose typed request-body schema from `initial_input`
- the default wrapped response can expose typed `data` from `result`
- OpenAPI can carry `x-agently-triggerflow-contract`

This is the best fit when clients should discover typed workflow input and output from FastAPI itself.

## 3. Quick Rule

- single request, single final reply -> POST or GET
- progressive updates without client messages back -> SSE
- long-lived client interaction -> WebSocket
