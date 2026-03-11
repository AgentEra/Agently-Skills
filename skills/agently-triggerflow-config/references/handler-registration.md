# Handler Registration

This page explains what must exist before a restored TriggerFlow definition can run.

## 1. Named Or Inspected Callables Need Registries

When a flow config refers to chunk handlers or condition handlers, the restored `TriggerFlow` must know how to resolve them.

Typical pattern:

```python
restored = TriggerFlow()
restored.register_chunk_handler(my_chunk)
restored.register_condition_handler(my_condition)
restored.load_json_flow(json_content)
```

## 2. Register Before Loading

Public guidance should prefer:

- register handlers first
- then call `load_flow_config(...)`, `load_json_flow(...)`, or `load_yaml_flow(...)`

This matches the current runtime model where definition compilation binds references against the registry available at load time.

## 3. Runtime Resources Are Separate

Even after a successful config load, runtime resources still need runtime injection.

Typical pattern:

```python
result = await restored.async_start(
    payload,
    runtime_resources={"renderer": renderer},
)
```

or:

```python
restored.update_runtime_resources(renderer=renderer)
```

## 4. Lambdas And Other Non-Serializable Callables

Mermaid may still show lambda-based chunks or conditions for inspection.

But for portable config export:

- use registered named handlers
- avoid anonymous non-serializable callables
