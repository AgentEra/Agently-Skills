# Standard Request Path

Use this page when the requirement should still be solved as one normal model request.

## 1. Standard Path

The standard Agently request path is:

1. connect the right model capability
2. compose the input
3. send one request
4. read the final result

In skill terms, that usually means:

- `agently-model-setup`
- `agently-input-composition`

and sometimes:

- `agently-output-control`

if the result should be structured instead of plain text.

## 2. When Standard Is Enough

Stay on the standard path when:

- one request can answer directly
- no external tool use is needed
- no external retrieval step is needed
- no long-lived memory is required
- no workflow branching or waiting is required

## 3. Practical Default

Default to one request first.

Do not jump to tools, RAG, session, or TriggerFlow unless the business problem clearly exceeds the single-request boundary.
