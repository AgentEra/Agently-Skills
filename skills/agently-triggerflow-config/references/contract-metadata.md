# Contract Metadata

Use this page when the definition artifact should carry TriggerFlow contract information.

## 1. What Exported Config Carries

Current flow config can carry exported contract metadata such as:

- `initial_input`
- `stream`
- `result`
- `meta`
- `system_stream.interrupt`

This is useful for:

- schema inspection
- architecture review
- documentation artifacts
- Mermaid output that shows the contract node

## 2. What Mermaid Shows

Detailed Mermaid can now expose a contract summary, including:

- input label
- stream label
- result label
- contract meta keys
- system interrupt presence

## 3. Important Boundary

Config roundtrip preserves contract metadata, not the original live Python contract validators.

That means:

- `get_flow_config()` can include contract schema metadata
- `load_flow_config()` can preserve that metadata for later export and Mermaid
- `get_contract()` after config load does not automatically recover the original Python contract types

If the restored flow still needs live runtime validation, reapply `set_contract(...)` in Python after loading.
