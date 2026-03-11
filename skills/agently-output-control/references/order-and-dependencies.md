# Order And Dependencies

This page explains why output field order is a real control surface in Agently.

## 1. Order Is Not Cosmetic

For structured `.output({...})` schemas, field order is preserved through prompt generation.

Agently also reuses that schema order in structured streaming and parsing internals.

That means output key order is part of the control design, not just a formatting detail.

## 2. Practical Rule

If one field should help produce another field, define the helper field first.

Put prerequisite fields before dependent fields.

Typical patterns:

- facts before summary
- extracted evidence before conclusion
- decision before explanation
- `prethinking` before `reply`

## 3. Why This Enables CoT-Like Control

Agently generates structured outputs in schema order.

That makes it possible to force a staged output shape such as:

1. collect intermediate facts or planning signals
2. use those earlier fields as context for the later final field

This is the core reason order can be used for CoT-like or planning-first output control.

If `reply` comes first, the model may answer too early and skip the intended intermediate control fields.

## 4. Strong Recommendation

All information that should guide later generation should appear earlier in the schema.

If a later field depends on:

- facts
- extracted entities
- confidence checks
- plan steps
- self-review notes
- `prethinking`

place those fields before the dependent field.

## 5. Example

Prefer this:

```python
.output({
  "prethinking": (str, "Brief internal planning for the answer"),
  "reply": (str, "Final user-facing answer"),
})
```

Over this:

```python
.output({
  "reply": (str, "Final user-facing answer"),
  "prethinking": (str, "Brief internal planning for the answer"),
})
```

The second version weakens the dependency structure because the final answer appears before the planning field.

## 6. Pair Order With `ensure_keys`

If later fields depend on earlier fields, protect the earlier fields with `ensure_keys`.

Example:

```python
response.result.get_data(
  ensure_keys=["prethinking", "reply"],
  max_retries=1,
)
```

This does not create the dependency by itself. The dependency comes from schema order. `ensure_keys` only protects completeness.

## 7. Streaming Implication

In structured streaming, earlier fields are also the earliest fields the parser expects to see completed.

That makes good ordering especially important when the caller wants:

- early UI updates
- progressive reveal
- staged logic that reacts to intermediate fields before the final answer arrives

## 8. Boundary

Order improves control and stability, but it is still a prompting mechanism, not a mathematical guarantee of model reasoning quality.

Use ordering to shape the generation path, then use `ensure_keys` or simpler schemas when reliability matters.
