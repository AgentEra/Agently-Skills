# Troubleshooting

- The design keeps adding more agents without becoming clearer:
  Collapse the design back toward one request or fewer specialist stages.
- Agents keep passing large free-form text blobs to each other:
  Replace raw handoff text with explicit structured contracts.
- Several agents can all produce the final answer:
  Define one final owner and make the other agents feed it.
- Agents recursively trigger more agents:
  Add bounded fan-out, step budgets, or an approval gate before more delegation.
- Everything shares the same chat history:
  Isolate per-agent context by default and move truly shared state into workflow state or external storage.
