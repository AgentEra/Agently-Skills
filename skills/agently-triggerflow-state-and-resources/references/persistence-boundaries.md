# Persistence Boundaries

This page covers what survives and what does not.

## 1. Execution Save / Load

Execution state can carry:

- `runtime_data`
- flow-data snapshot
- interrupts
- result readiness and result value
- resource key names

Execution state does not carry:

- live resource objects
- client instances
- functions
- the whole flow definition

## 2. Flow Config Export / Import

Flow config preserves:

- serializable definition structure
- handler references
- state and signal structure

Flow config does not preserve:

- runtime resource objects
- current execution runtime state

## 3. Restart-Safe Design

Use this design split:

- definition shape -> `agently-triggerflow-config`
- running-instance state -> `agently-triggerflow-execution-state`
- runtime-only dependencies -> reinject at restore time
- long-lived memory outside the workflow runtime -> external persistence or `agently-session-memo`

## 4. Real-World Rule

If a resumed execution fails after restore, the missing piece is often not the saved state itself but the runtime resource environment.
