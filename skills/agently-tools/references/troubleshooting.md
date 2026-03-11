# Troubleshooting

- The tool never seems to run:
  Check whether the agent actually attached tools with `use_tools(...)` and whether tool loop is enabled.
- The tool loop keeps going too long:
  Lower `max_rounds`, cap `concurrency`, and set a `timeout`.
- The tool is remote instead of local:
  Switch to `agently-mcp`.
- The request has become a multi-step workflow with explicit state and branching:
  Switch to `agently-triggerflow-playbook`.
- The main question is now how to consume streamed output or response metadata:
  Switch to `agently-output-control`.
