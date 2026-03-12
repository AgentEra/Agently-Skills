# Skill Discovery And Packaging Refactor Plan

This note is author-side only. It does not belong in the published skill payload.

## Why This Plan Exists

Recent review of the repository surfaced a discovery-layer problem rather than a knowledge-coverage problem.

The skill tree is broad and well-structured, but the frontmatter for the main routers is too similar, it still overweights internal framework vocabulary, installation guidance favors whole-repository installs before bundle guidance exists, and current validation is stronger on static structure than on real trigger behavior.

## Current Findings

### 1. Router descriptions overlap too heavily

The current frontmatter for:

- `agently-playbook`
- `agently-model-request-playbook`
- `agently-triggerflow-playbook`

all compete on variations of:

- business requirement
- decide whether
- route to the right skill
- escalate to another solution level

This creates router-on-router competition before the SKILL body is ever loaded.

### 2. Router precedence is explained in the body, not fully in frontmatter

The current bodies explain the intended hierarchy correctly:

- top-level router
- domain router
- implementation skill

But frontmatter does not encode that hierarchy strongly enough. If only `name` and `description` are available during discovery, the intended precedence is under-specified, and the current wording still asks the user to think in Agently-internal terms too early.

### 3. README install guidance biases toward full coexistence too early

The repository README currently presents whole-repository installation first. That is convenient for availability, but it increases trigger competition before narrow bundle guidance exists.

### 4. Validation does not yet model coexistence well enough

Current validation scripts mainly check:

- file presence
- frontmatter presence
- keyword coverage
- reference-file existence

This does not answer the most important discovery question:

- when nearby skills coexist, does the right skill trigger first?

### 5. Repository-level entry docs are not fully synchronized

The root `AGENTS.md` still describes the repository as an initial scaffold. That no longer matches the published repository surface.

## External Guidance Reviewed

These external guidance sources all point in the same direction:

- Anthropic Agent Skills best practices:
  - descriptions should be specific and include key terms
  - build evaluations first
  - representative trigger queries matter
- Anthropic enterprise skills guidance:
  - skills compete for attention
  - coexistence testing matters
  - narrow or role-based grouping is safer than broad undifferentiated installs
- OpenAI instruction guidance:
  - use clear trigger-action structure
  - break multi-step behavior into explicit steps
  - use concrete examples
- GitHub Copilot custom-instructions guidance:
  - keep instruction surfaces scoped and minimal
  - avoid broad overlapping instruction layers when narrower scope is possible

Reference URLs:

- `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`
- `https://support.claude.com/en/articles/10166093-building-effective-skills`
- `https://support.claude.com/en/articles/11326709-skills-for-enterprise-using-skills-with-the-api`
- `https://help.openai.com/en/articles/9358033-key-guidelines-for-writing-instructions-for-custom-gpts`
- `https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions`

## Refactor Plan

### Phase 1. Reset discovery boundaries in frontmatter

Rewrite the frontmatter descriptions for the main routers so they are mutually exclusive and scenario-led:

- `agently-playbook`
  - only the top-level cross-domain router
- `agently-model-request-playbook`
  - only the one-request domain router
- `agently-triggerflow-playbook`
  - only the workflow-orchestration router

Then review neighboring implementation skills to ensure they do not reclaim generic router language.

### Phase 2. Introduce an activation layer between the catalog and the skills

Treat the current tree as a catalog, then define a smaller runtime activation surface through bundles.

Three-layer model:

- catalog layer
  - the full repository skill tree for maintenance and long-form coverage
- activation layer
  - a small bundle of active skills chosen for the current product, role, or workflow
- disclosure layer
  - progressive loading inside the selected skills through frontmatter, SKILL.md, and referenced files

The tree should remain rich for authoring, but runtime discovery should happen against a bundle-sized active set.

### Phase 3. Make installation guidance narrower by default

Shift repository guidance from:

- whole repository first

to:

- explicit entry skill first
- narrow bundle second
- full repository only when the user truly wants the complete capability tree

Target bundle shapes:

- request core
  - `agently-playbook`
  - `agently-model-request-playbook`
  - `agently-model-setup`
  - `agently-input-composition`
  - `agently-output-control`
- request extensions
  - `agently-tools`
  - `agently-mcp`
  - `agently-session-memo`
  - `agently-prompt-config-files`
  - `agently-fastapi-helper`
  - `agently-embeddings`
  - `agently-knowledge-base-and-rag`
- triggerflow core
  - `agently-triggerflow-playbook`
  - all published TriggerFlow implementation skills
- migrations
  - LangChain and LangGraph migration skills

### Phase 4. Add trigger and coexistence evaluation

Create trigger fixtures under `spec/` for every routing skill and every high-overlap skill.

Each target should include:

- positive examples
- negative examples
- ambiguous or coexistence examples

Minimum high-priority coexistence sets:

- `agently-playbook` vs `agently-model-request-playbook`
- `agently-playbook` vs `agently-triggerflow-playbook`
- `agently-model-request-playbook` vs `agently-model-setup`
- `agently-model-request-playbook` vs `agently-input-composition`
- `agently-model-request-playbook` vs `agently-output-control`
- `agently-triggerflow-playbook` vs `agently-triggerflow-orchestration`
- `agently-triggerflow-playbook` vs `agently-triggerflow-subflows`

The validation bar should move from:

- "does the description mention the right words?"

to:

- "does the right skill win against its nearest competing skills?"

Use two validation layers:

- static fixture integrity checks
- Agently-driven live judging against the fixture set on a configured model endpoint such as local Ollama

### Phase 5. Clean repository entry points

- update or remove the stale root `AGENTS.md`
- align README install order with the new packaging strategy
- require metadata-boundary review whenever a router description changes

## Success Criteria

The refactor is successful when these behaviors are reliably true:

- a cross-domain business goal triggers `agently-playbook`
- a single-request business problem triggers `agently-model-request-playbook`
- a workflow-orchestration problem triggers `agently-triggerflow-playbook`
- generic model-app requests can still route into the Agently skill tree even when the user does not explicitly say Agently
- direct provider setup questions trigger `agently-model-setup`, not the playbooks
- direct prompt-composition questions trigger `agently-input-composition`
- direct output-shape questions trigger `agently-output-control`
- explicit low-level TriggerFlow API questions trigger the corresponding implementation skill
- narrow installs remain understandable without requiring the whole repository to be present

## Immediate Next Changes

1. Rewrite the three main router descriptions.
2. Add first-pass coexistence fixtures for the router trio.
3. Add router-vs-leaf fixtures for the request domain.
4. Update README install guidance.
5. Fix the stale root `AGENTS.md`.
