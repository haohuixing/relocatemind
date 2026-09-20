# Task: <short title>

## Objective

What outcome should be achieved?

## Why this matters

Which product, reliability, security, or maintenance problem does this solve?

## Repository context to read

- `AGENTS.md`
- `PROMPT.md`
- `docs/agent-context/CURRENT_STATE.md`
- Relevant architecture, security, data, AI, and operations documents
- Specific source files, tests, and migrations

## Scope

List the behavior and files/components this task owns.

## Explicit non-scope

List related work that must not be changed in this task.

## Files/components likely affected

- 

## Constraints and safety rules

- Preserve unrelated working-tree changes.
- Do not expose or commit secrets/private data.
- Follow relevant security, data-governance, and provider rules.
- Keep planned and implemented behavior distinct.

## Acceptance criteria

- [ ] 
- [ ] 
- [ ] 

## Tests/checks required

- [ ] Unit tests
- [ ] Integration or route tests
- [ ] Type check/lint/build
- [ ] Migration or contract check
- [ ] Manual smoke test, if applicable

## Rollback or migration concerns

Describe data changes, compatibility concerns, feature flags, and rollback approach.

## Handoff requirements

Before ending:

- update `CURRENT_STATE.md`;
- add an ADR if a durable decision was made;
- update `ROADMAP.md` if milestone scope/status changed;
- record files changed and checks run;
- list failures, risks, pre-existing changes, and exact next action;
- do not include credentials, tokens, private user data, or raw production logs.
