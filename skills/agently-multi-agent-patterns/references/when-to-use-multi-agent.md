# When To Use Multi-Agent

Use multi-agent architecture only when specialization, isolation, or staged ownership is the real problem.

Start with the simplest viable option:

1. one standard request
2. one high-quality request with structured output or structured streaming
3. one request plus tools, MCP, KB/RAG, or session continuity
4. multi-agent design only after the earlier levels are clearly insufficient

Multi-agent design is usually justified when:

- one agent should plan or route while another should execute
- one agent should review or revise another
- several specialists should work in parallel and one final owner should synthesize
- different agents need different tools, MCP servers, models, or memory boundaries
- the business process benefits from explicit ownership boundaries between stages

Avoid multi-agent design when:

- one high-quality structured request could do the same work
- the only difference between agents is a small prompt wording change
- there is no explicit handoff contract
- no one agent owns the final result

The practical question is not "can several agents be used". The practical question is "what specialization or boundary does each additional agent make safer, clearer, or easier to evolve".
