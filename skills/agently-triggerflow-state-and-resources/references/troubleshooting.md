# Troubleshooting

- Values leaked from one run into another:
  Re-check whether request-local data was stored in `flow_data` instead of `runtime_data`.
- A resource works in one execution but not another:
  Re-check whether it was injected only at execution level or created with `data.set_resource(...)`.
- Restored execution fails after restart:
  Re-check runtime-resource reinjection. Save/load keeps resource keys, not resource objects.
- Restored flow config runs but a handler is missing a client or helper:
  Flow config does not serialize runtime resources; reinject them at runtime.
- Child flow did not see the expected parent state:
  Re-check sub-flow `capture`. Parent state and resources do not cross automatically.
