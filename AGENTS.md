---
name: agently-skills-catalog
description: Central catalog and documentation for Agently Skills V2. Use when working with Agently framework development, skill installation, validation, or catalog management.
---

# Agently Skills Catalog

This repository publishes the Agently Skills V2 catalog under `skills/`. Each skill follows the Agently Skills specification and provides framework-native capabilities for model-powered applications.

## Repository Layout

### Core Structure
- `skills/` - Published installable V2 skill payloads
- `validate/` - Shared V2 validation sources and fixtures
- `bundles/` - Bundle manifests and installation metadata
- `spec/` - Local-only author workspace (not publishable)

### Skill Directory Structure
Each skill follows this structure:
```
skill-name/
├── SKILL.md              # Skill definition and documentation
├── examples/             # Usage examples and templates
├── outputs/              # Runtime artifacts and templates
├── references/           # Reference documentation
└── scripts/              # Utility scripts
```

## Available Skills

### Core Skills
1. **agently-playbook** - Top-level router for unresolved model-powered product requests
2. **agently-model-setup** - Provider connection and model settings
3. **agently-prompt-management** - Prompt composition and YAML-backed prompts
4. **agently-output-control** - Structured output and required keys
5. **agently-model-response** - Response reuse and streaming consumption
6. **agently-session-memory** - Session continuity and conversational state

### Extension Skills
7. **agently-agent-extensions** - Tools, MCP, and FastAPIHelper
8. **agently-knowledge-base** - Embeddings and retrieval flows
9. **agently-triggerflow** - Workflow orchestration and event-driven execution

### Migration Skills
10. **agently-migration-playbook** - Migration from LangChain/LangGraph
11. **agently-langchain-to-agently** - LangChain migration helpers
12. **agently-langgraph-to-triggerflow** - LangGraph to TriggerFlow migration

## Installation

### Install All Skills
```bash
npx skills add AgentEra/Agently-Skills
```

### Install Specific Skills
```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-model-setup
```

### Bundle Installation
```bash
# Install from bundle manifest
npx skills install bundles/manifest.json
```

## Usage Guidelines

### When to Use Which Skill

1. **Start with `agently-playbook`** when:
   - Request starts from business goals or product behavior
   - Owner layer is unresolved
   - Building model-powered assistants, tools, or workflows
   - Project initialization or structure refactor

2. **Route to specific skills** based on capability needs:
   - Model setup → `agently-model-setup`
   - Prompt design → `agently-prompt-management`
   - Output control → `agently-output-control`
   - Workflow orchestration → `agently-triggerflow`
   - Knowledge retrieval → `agently-knowledge-base`

### Project Structure
For maintainable Agently projects, follow this structure:
```
project/
├── SETTINGS.yaml          # Provider config and environment placeholders
├── app.py                 # Main application layer
├── prompts/               # YAML/JSON prompt contracts
├── workflow/              # TriggerFlow graphs and implementations
├── tools/                 # Search, browse, MCP adapters
└── outputs/               # Runtime artifacts
```

## Validation

### Validation Suite
The repository includes comprehensive validation:
- `validate/validate_catalog.py` - Catalog structure validation
- `validate/validate_bundle_manifest.py` - Bundle manifest validation
- `validate/validate_trigger_paths.py` - Trigger path validation
- `validate/validate_native_usage.py` - Native capability validation
- `validate/validate_live_scenarios.py` - Live scenario validation
- `validate/validate_reference_retrieval.py` - Reference retrieval validation

### Validation Fixtures
- `validate/fixtures/route_cases.json` - Routing test cases
- `validate/fixtures/implementation_cases.json` - Implementation test cases
- `validate/fixtures/reference_retrieval_cases.json` - Retrieval test cases

## Authoring Guidelines

### Priorities
1. **Route unresolved requests through `agently-playbook` first**
2. **Prefer Agently-native capabilities** before custom solutions
3. **Keep skill boundaries capability-first** and mutually exclusive
4. **Treat multi-agent flows as scenario recipes** unless they need dedicated framework surfaces
5. **Keep validation fixtures in sync** with skill implementations

### Skill Development
1. Each skill must have a clear, single responsibility
2. Skills should be framework-native and avoid custom orchestration layers
3. Include comprehensive examples and references
4. Follow the standard directory structure
5. Update validation fixtures when changing skill boundaries

## References

### Primary References
- `bundles/manifest.json` - Bundle installation metadata
- `validate/fixtures/route_cases.json` - Routing test cases
- `validate/fixtures/implementation_cases.json` - Implementation test cases
- `validate/fixtures/reference_retrieval_cases.json` - Retrieval test cases

### Validation Scripts
- `validate/validate_catalog.py` - Catalog validation
- `validate/validate_bundle_manifest.py` - Bundle validation
- `validate/validate_trigger_paths.py` - Trigger path validation
- `validate/validate_native_usage.py` - Native usage validation
- `validate/validate_live_scenarios.py` - Live scenario validation
- `validate/validate_reference_retrieval.py` - Reference retrieval validation

## Maintenance

### Versioning
- Skills follow semantic versioning
- Bundle manifests track compatible versions
- Validation fixtures are versioned with skills

### Updates
1. Update skill implementations
2. Update validation fixtures
3. Update bundle manifests
4. Run validation suite
5. Update documentation

### Testing
```bash
# Run all validation tests
cd validate
python validate_catalog.py
python validate_bundle_manifest.py
python validate_trigger_paths.py
python validate_native_usage.py
python validate_live_scenarios.py
python validate_reference_retrieval.py
```

## Support

For issues, questions, or contributions:
1. Check the skill-specific documentation in `skills/[skill-name]/SKILL.md`
2. Review validation fixtures for expected behavior
3. Consult the Agently framework documentation
4. Open issues in the repository

---

**Remember:** Always start with `agently-playbook` when the owner layer is unresolved. Prefer Agently-native capabilities before custom solutions.
