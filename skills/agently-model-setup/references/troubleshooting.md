# Troubleshooting

This page only covers model setup issues. It does not cover structured output or streaming-consumption issues.

## 1. Default debugging order

1. Run the minimal verification case first
2. Enable `debug`
3. Check `request_url`
4. Check `request_options`
5. Check `model`
6. Check `stream`
7. Then check auth and provider-specific fields

## 2. `temperature` / `top_p` Does Not Take Effect

Source-backed conclusion:

- plugin-root `options` still works as a backward-compatible fallback
- plugin-level default parameters should go into `request_options`
- per-request parameters should go into `agent.options({...})`

So the common mistake is:

- assuming plugin-root `options` is the preferred long-term entry point

## 3. `model` Does Not Take Effect

Most common cause:

- trying to override it via `agent.options({"model": ...})`

The source writes the plugin-level `model` back into the final request body.

## 4. `stream` Does Not Take Effect

Most common cause:

- trying to override it via `agent.options({"stream": ...})`

The source writes it back using plugin-level or default logic.

## 5. `401 Unauthorized`

Check these first:

- whether `api_key` is correct
- whether `auth` has the expected structure
- whether the provider actually accepts Bearer auth

If the user relies on custom header auth, confirm which field should own `Authorization`.

In the current requester path, `auth.headers` is merged into outgoing request headers. If `api_key` is also set, Agently writes Bearer auth into `Authorization` after that merge, so custom non-Authorization headers survive but `Authorization` follows `api_key`.

## 6. `404` / endpoint error

Check these first:

- whether `base_url` is missing `/v1`
- whether `path_mapping` matches the service’s actual path
- whether `full_url` should be used instead

## 7. Network Reachability Or Regional Access Fails

Typical signals:

- connect timeout before any provider response
- DNS or reachability errors
- the same API key and model work only when a local proxy is enabled

Check these first:

- whether `proxy` is configured as a top-level plugin setting
- whether the proxy address itself is reachable
- whether the proxy is being added in the wrong place such as `request_options` or `agent.options(...)`
- whether the real issue is `base_url` or `full_url`, not the proxy

Default advice:

- start with top-level `proxy`
- keep the rest of the config minimal until the request succeeds

## 8. HTTP Client Behavior Needs Customization

Typical signals:

- connection count needs to be capped
- redirects must be followed through a proxy or gateway
- the environment requires a custom CA bundle or environment-driven proxy settings
- the user is trying to solve an HTTP client issue by putting transport settings into `request_options`

Check these first:

- whether the requirement is really HTTP-client level, not request-body level
- whether a dedicated top-level field already exists, especially `proxy` or `timeout`
- whether `client_options` is the correct layer for the change

Default advice:

- use `client_options` for `limits`, `follow_redirects`, `http2`, `verify`, `cert`, `trust_env`, or `transport`
- keep `request_options` for request-body parameters only

## 9. model not found

Check these first:

- whether the model name is exact
- whether it needs a full prefix or version suffix
- whether a chat model was incorrectly configured as completions

## 10. `completions` Does Not Work

Most of the time this is not an Agently issue. It is usually because:

- the provider only really supports chat endpoints
- the user assumed “text generation” must mean completions

Default advice:

- if there is no explicit completion-endpoint requirement, switch back to `chat`

## 11. VLM Does Not Work

Check these first:

- whether the task is actually an image-understanding / OCR / visual-Q&A scenario
- whether the selected model really supports vision
- whether the request is still using `chat`
- whether `attachment()` is being used
- whether the image URL is reachable

Reminder:

- VLM is not a separate `model_type` here

## 12. Self-Hosted Or Gateway Response Is Non-Standard

Possible symptoms:

- empty `delta`
- missing `usage`
- missing `finish_reason`
- different tool or reasoning field paths

Check these first:

- `content_mapping`
- `content_mapping_style`
- `yield_extra_content_separately`

## 13. Fast Triage

- routing issues: check `base_url`, `full_url`, and `path_mapping`
- auth issues: check `api_key` and `auth`
- network reachability issues: check `proxy`, then `timeout`, then the endpoint itself
- HTTP client behavior issues: check `client_options` and whether a top-level field should be used instead
- parameter issues: check `request_options` and `agent.options()`
- VLM / image-understanding issues: first check vision support, then check `attachment()`
