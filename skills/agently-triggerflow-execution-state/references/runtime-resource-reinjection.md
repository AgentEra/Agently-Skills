# Runtime Resource Reinjection

This page covers one of the most important restore boundaries.

## 1. Resource Keys Are Saved, Resources Are Not

Execution state records resource key names so the caller can understand what the execution depended on.

It does not serialize:

- service objects
- functions
- clients
- connections

## 2. Reinject Before Continuing

Use one of these patterns:

```python
restored.load(saved_state, runtime_resources={"service": service})
```

or:

```python
restored.update_runtime_resources(service=service)
restored.load(saved_state)
```

Then continue the execution.

## 3. Why This Matters

Waiting executions often fail on resume not because state was lost, but because runtime-only dependencies were not restored.

If a resumed branch calls `require_resource(...)`, restore the resource environment as part of the resume path.
