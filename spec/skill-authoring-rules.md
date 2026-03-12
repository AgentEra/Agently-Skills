# Skill Authoring Rules

These rules apply to every skill in this repository unless a future spec explicitly narrows them for a specific case.

## Global Rules

- All skills in this repository must be authored in English.
- This applies to every new skill and every update to an existing skill.
- Skill-facing files must not mix English with Chinese or other languages unless a future spec explicitly requires multilingual output for a specific skill.
- This includes `SKILL.md`, reference files, usage examples, inline explanatory prose, and any other text meant for skill users.
- Keep author-side constraints and maintenance notes out of skill-facing files whenever possible.
- For published source-code references, cite the public Agently GitHub repository: `https://github.com/AgentEra/Agently`.
- For published documentation references, cite the public Agently docs portal: `https://agently.tech/docs/en/`.
- Do not publish machine-specific local paths, workspace-only references, or private filesystem assumptions in skill-facing files.
- Local checkouts may be used for author-side validation, but publishable references must point to public URLs.
- Use runnable examples and tests to validate behavior, but do not let them override confirmed source semantics.
- Published skills in this repository target Agently `>= 4.0.8.5` unless a future spec explicitly states otherwise.
- Maintain `spec/upstream-coverage-ledger.md` as the author-side incremental review baseline for upstream Agently commits.

## Discovery And Metadata Rules

- Treat `name` and `description` as the primary discovery layer. They are routing metadata, not marketing copy.
- Encode routing precedence in frontmatter, not only in the SKILL body. If a skill is a top-level router, domain router, or implementation skill, that role must already be obvious from the frontmatter alone.
- Keep sibling descriptions mutually exclusive along the main routing axis. If two nearby skills both claim broad phrases such as "business requirement", "decide whether", or "route to the right skill", narrow both until the distinction is explicit.
- Top-level routers may claim only cross-domain architecture selection.
- Domain routers may claim only one capability domain and its escalation boundary.
- Implementation skills must avoid generic business-requirement language that belongs to routers.
- Lead descriptions with the user-visible scenario or problem shape first, then include the key terms that confirm the match.
- Do not make framework identity the main discriminator when the same scenario could reasonably be asked without naming Agently.
- Internal framework names such as `Agently` or `TriggerFlow` may appear in frontmatter, but they should usually act as confirmation terms rather than required trigger anchors.
- Prefer capability language such as understanding, rewriting, expansion, generation, scoring, validation, workflow, approval, pause and resume, concurrency, or retrieval before lower-level internal API names.
- Prefer explicit "use only when..." boundaries and concrete near-neighbor non-trigger cases over long undifferentiated capability lists.

## Packaging And Installation Rules

- Treat the repository skill tree as a catalog and maintenance structure, not as the default runtime discovery surface.
- Runtime activation should happen through small bundles or explicit entry-skill installs, not by assuming the entire tree should coexist in discovery at all times.
- Role or identity language belongs at the bundle-selection layer.
- Scenario and escalation language belongs at the router-skill layer.
- Concrete capability and API-surface language belongs at the implementation-skill layer.
- Do not assume full-repository installation during authoring. Each skill must still make sense when installed alongside only its nearest neighbors.
- Repository docs should prefer narrow bundle installs or explicit entry-skill installs before recommending whole-repository installation.
- If several skills are expected to be installed together regularly, define and document the bundle boundary explicitly instead of relying on a flat skill list.
- Maintain the current author-side bundle manifest in `spec/skill-bundles.json` and keep public install guidance aligned with it.
- Keep the public machine-readable bundle manifest in `bundles/manifest.json` synchronized with the author-side bundle manifest.
- Keep repository-level entry docs, including root `AGENTS.md`, synchronized with the current published scope.

## Public Guidance Quality Rules

- When public guidance starts from a low-information-density request, prefer a short spec-first intake before implementation advice.
- When several explicit model requests must be connected for quality, present TriggerFlow as the default orchestration owner unless the design is truly still one request.
- When output control, prompt reuse, or nearby extensions matter, prefer `Agent`-owned request guidance over disposable one-off request snippets.
- When business prompts should be versioned, reused, or reviewed outside runtime code, prefer YAML or JSON prompt config guidance over scattering prompt text through application logic.
- Treat `debug` and request or prompt inspection as first-line observability guidance before speculative rewrites.
- Keep repository-level skill validation scoped to skill content, routing, and confirmed behavior. Do not describe that as equivalent to downstream application acceptance.

## Trigger Validation Rules

- Every routing skill and every high-overlap skill must have representative trigger fixtures in `spec/`.
- Trigger fixtures must include positive examples, negative examples, and ambiguous or coexistence examples against the nearest competing skills.
- Trigger fixtures for routers should include generic model-app requests that omit internal framework names when those requests should still route into the Agently capability tree.
- Static keyword checks are not sufficient validation for routing skills.
- Trigger validation should include a model-based usability pass through Agently against the current fixture set whenever a local or CI-accessible model endpoint is available.
- Validation should exercise multi-skill coexistence, not only file existence, frontmatter presence, or keyword coverage.
- Before widening a frontmatter description, rerun coexistence fixtures for the nearest competing skills and update the fixtures when the intended boundary changes.
