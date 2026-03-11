# Export And Import Roundtrip

This page covers portable TriggerFlow definition roundtrip.

## 1. Standard Roundtrip

Typical sequence:

1. build the source flow
2. export JSON or YAML
3. create a fresh `TriggerFlow()`
4. register required handlers
5. load the exported config
6. start the restored flow

## 2. JSON Versus YAML

Use JSON when:

- machine generation is the primary goal
- exact structural diffs matter more than hand editing

Use YAML when:

- people are more likely to inspect or edit the artifact directly
- readability is a higher priority

## 3. What The Roundtrip Preserves

- operator graph
- named chunks and condition references
- branching and loop structure
- sub-flow structure
- signal declarations that belong to the definition
- exported contract metadata and system interrupt metadata

## 4. What The Roundtrip Does Not Carry

- runtime resources such as functions, services, or clients
- arbitrary anonymous lambdas as serializable handler references
- execution-local state
- waiting interrupts or pending runtime stream state
- the original live Python contract validators behind `set_contract(...)`

## 5. Safe Public Guidance

When writing or using this skill:

- restore the definition first
- re-register handlers before load
- reinject runtime resources at execution time
