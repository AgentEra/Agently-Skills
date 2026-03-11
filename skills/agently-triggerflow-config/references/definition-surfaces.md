# Definition Surfaces

This page explains the three main TriggerFlow definition surfaces.

## 1. Blueprint Copy

Use:

- `save_blue_print()`
- `load_blue_print()`

Good fit:

- same Python process
- same callable objects still exist
- fast in-memory duplication or reuse

Think of this as:

- copying a live definition object, not exporting a file format

## 2. Flow Config

Use:

- `get_flow_config()`
- `get_json_flow()`
- `get_yaml_flow()`
- `load_flow_config()`
- `load_json_flow()`
- `load_yaml_flow()`

Good fit:

- repository storage
- transport across processes
- long-lived definition artifacts
- reviewable JSON or YAML assets

Think of this as:

- serializing the flow definition into a portable artifact
- including contract metadata when the source flow exported one

## 3. Mermaid

Use:

- `to_mermaid(mode="simplified")`
- `to_mermaid(mode="detailed")`

Good fit:

- architecture review
- visual debugging
- human-readable discussion of nested or branching flow shape

Think of this as:

- inspection output, not an executable persistence format
- contract labels may also appear here for human review
