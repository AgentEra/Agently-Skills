# Scenario Router

Use this page to classify the source system before choosing a narrower migration skill.

## 1. LangChain-side migration

Use `agently-langchain-to-agently` when the source system is mainly about:

- `create_agent`
- tools
- structured output
- short-term memory
- middleware or guardrails
- retrieval or service exposure around one agent

## 2. LangGraph-side migration

Use `agently-langgraph-to-triggerflow` when the source system is mainly about:

- `StateGraph`
- nodes and edges
- graph state
- interrupts
- persistence or checkpoints
- streaming
- subgraphs
- durable execution

## 3. Mixed system

If the source system mixes LangChain agents inside a LangGraph graph:

- start from `agently-langgraph-to-triggerflow` when orchestration is the harder migration problem
- start from `agently-langchain-to-agently` when the workflow is simple and the real migration work is one-agent behavior

## 4. Simplification-first case

If the source design looks over-engineered for the actual problem:

- stay in this playbook first
- choose the smallest Agently target architecture
- then route to the narrower migration skill
