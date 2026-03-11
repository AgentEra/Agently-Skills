# Troubleshooting

- The workflow shape still feels unclear:
  Decide first whether this is routing, fan-out and fan-in, item-wise work, a loop, or a human gate.
- The pattern keeps growing into many nested state questions:
  Switch to `agently-triggerflow-state-and-resources`.
- The pattern needs explicit child workflows:
  Switch to `agently-triggerflow-subflows`.
- The loop can wait or needs approval:
  Switch to `agently-triggerflow-interrupts-and-stream`.
- The loop is really about model calls, structured streaming, or tool use with model requests:
  Switch to `agently-triggerflow-model-integration`.
