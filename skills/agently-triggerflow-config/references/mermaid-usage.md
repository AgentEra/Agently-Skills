# Mermaid Usage

This page covers how Mermaid fits into TriggerFlow work.

## 1. `simplified` Mode

Use `to_mermaid(mode="simplified")` when:

- the goal is high-level structure
- grouped branching or nested sub-flow shape matters more than every internal edge
- the diagram is meant for human discussion

## 2. `detailed` Mode

Use `to_mermaid(mode="detailed")` when:

- internal nodes and callable labels matter
- debugging exact branch structure
- inspecting generated names or lambda labels
- inspecting exported contract labels and contract meta keys

## 3. Mermaid Is More Permissive Than Config Export

Important boundary:

- Mermaid can visualize some shapes that are not safe to serialize

Example:

- lambda handlers may appear in Mermaid
- the same flow may still be rejected by `get_flow_config()`

So use Mermaid for inspection, not as proof that the flow is export-safe.

## 4. Nested Sub Flows

Mermaid is especially useful when:

- the flow contains nested sub flows
- conditional groups exist inside child flows
- `for_each` or other grouped operators create layered structure

This is one of the main reasons to keep Mermaid in a separate config skill instead of burying it inside orchestration basics.

## 5. Contract Summary Node

When the definition carries exported contract metadata, Mermaid can show a contract summary node.

This is useful for:

- reviewing input, stream, and result labels
- checking whether contract meta exists
- seeing that system interrupt metadata is present
