# Response Wrapping And Errors

Use this page when the main question is what the helper returns.

## 1. Default Response Shape

By default, `FastAPIHelper` wraps successful results as:

- `status`
- `data`
- `msg`

and wraps errors with:

- `status`
- `data`
- `msg`
- `error`

## 2. Default Error Classification

Current default wrapper maps:

- `ValueError` -> `422`
- `TimeoutError` -> `504`
- other exceptions -> `400`

These values belong to the helper's response body shape.

## 3. Transport Status Versus Wrapped Status

With the default helper wrapper, the HTTP transport layer can remain `200` while the actual helper-level failure is reported in the wrapped body:

- HTTP status: `200`
- response body `status`: actual helper-level result code

This is expected helper behavior. Treat the wrapped `status` field as the contract for success or failure:

- `status < 400` -> success
- `status >= 400` -> helper-level failure

This design keeps the response envelope stable even when internal provider or node-level failures must still be reported to the caller.

## 4. Route-Level Validation Versus Helper Wrapping

For helper routes with FastAPI request-model validation, malformed POST bodies can fail before the helper wrapper runs.

That means both patterns can exist:

- helper-level runtime or provider errors -> HTTP `200` with wrapped body `status`
- request-model validation failures -> transport-level HTTP `422`

This applies to malformed helper payloads in general, and TriggerFlow contracts can add deeper typed request validation on top of the route-level schema.

## 5. Contract-Aware TriggerFlow Routes

For contract-backed TriggerFlow providers, there is an additional boundary:

- POST request-body validation can happen before the helper wrapper runs
- invalid request bodies can therefore return transport-level HTTP `422`

In other words:

- helper-level runtime or provider errors can still appear as HTTP `200` plus wrapped body `status`
- request-model validation for a typed TriggerFlow POST can fail earlier at the FastAPI transport layer

If the helper uses the default response wrapper and the TriggerFlow contract declares a `result` type, the wrapped response `data` can also be typed from that result contract.

## 6. Custom Response Warper

Use a custom `response_warper` when the service needs a different body shape or different application-level error schema.

Keep in mind that helper wrapping and overall HTTP service design are separate concerns.
