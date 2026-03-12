---
name: agently-fastapi-helper
description: Use only when the main task is direct HTTP, SSE, or WebSocket exposure through `FastAPIHelper`, including POST or GET APIs, payload shape, response wrapping, provider binding, or TriggerFlow-contract-aware request, response, and OpenAPI behavior.
---

# Agently FastAPI Helper

This skill is the service-exposure leaf for `FastAPIHelper` after the underlying Agently provider is already known. It focuses on exposing an agent, request, flow, execution, or generator as HTTP, SSE, or WebSocket endpoints with the helper's standard payload and response wrapper. It does not choose between one-request extensions or TriggerFlow design paths, and it does not cover full service architecture or multi-component business-system design.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- `FastAPIHelper`
- `use_post(...)`
- `use_get(...)`
- `use_sse(...)`
- `use_websocket(...)`
- request payload shape
- response wrapping and error payloads
- TriggerFlow contract-aware request and response models
- contract metadata in OpenAPI
- provider types such as `BaseAgent`, `ModelRequest`, `TriggerFlow`, `TriggerFlowExecution`, or generator functions

Do not use this skill for:

- general FastAPI architecture beyond the helper
- TriggerFlow business workflow design
- model setup or tool design as the main problem

## Workflow

1. Start with [references/provider-types-and-payloads.md](references/provider-types-and-payloads.md) when the main problem is which provider type should sit behind the helper.
2. Read [references/http-sse-websocket.md](references/http-sse-websocket.md) when choosing between ordinary APIs, SSE, and WebSocket.
3. Read [references/response-wrapping-and-errors.md](references/response-wrapping-and-errors.md) when the main issue is payload shape, wrapper semantics, or error handling.
4. Read [references/service-recipes.md](references/service-recipes.md) when wiring a quick agent endpoint or a streamed TriggerFlow endpoint.
5. If the task grows into broader service-system design, leave this helper skill and route at the playbook layer later.
6. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

`FastAPIHelper` is a service exposure helper, not a service architecture framework.

It standardizes:

- request payload parsing
- provider invocation
- response wrapping
- optional streaming over SSE or WebSocket

For TriggerFlow providers with `set_contract(...)`, it can also expose contract-aware HTTP and OpenAPI surfaces:

- POST body typing from `contract.initial_input`
- wrapped response `data` typing from `contract.result`
- OpenAPI extension metadata from exported TriggerFlow contract metadata

Agently guidance here should remain async-first:

- prefer async providers
- prefer SSE or WebSocket for progressive output
- treat sync wrappers as compatibility bridges, not the preferred service layer

## Selection Rules

- quick single-request HTTP endpoint -> POST or GET helper
- progressive one-way stream -> SSE helper
- bi-directional session-like stream -> WebSocket helper
- plain agent or model request behind one endpoint -> `BaseAgent` or `ModelRequest` provider
- runtime stream from TriggerFlow -> `TriggerFlow` or `TriggerFlowExecution` provider
- TriggerFlow provider should expose typed request or typed wrapped response in OpenAPI -> use a contract-backed TriggerFlow provider

## Important Boundaries

- `FastAPIHelper` standardizes the body shape; it does not automatically design the surrounding service architecture
- the default helper wrapper can keep HTTP transport status stable while reporting the actual helper-level status inside the response body
- clients must inspect the wrapped `status` field, not only the HTTP transport status
- FastAPI request-model validation can reject malformed POST request bodies at transport level with HTTP `422` before the helper wrapper runs
- contract-backed TriggerFlow POST routes can add deeper typed request-body validation on top of that route-level validation
- provider logic and business orchestration remain separate from HTTP exposure

## References

- `references/source-map.md`
- `references/provider-types-and-payloads.md`
- `references/http-sse-websocket.md`
- `references/response-wrapping-and-errors.md`
- `references/service-recipes.md`
- `references/troubleshooting.md`
