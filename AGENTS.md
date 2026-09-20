# RelocateMind Agent Instructions

These instructions apply to every human or AI agent working in this repository.

## Authority and context

The repository is the final authority for implemented behavior. Use this order when sources disagree:

1. Current source code, tests, migrations, and verified runtime behavior
2. Safe inspection of staging/live configuration and database schema
3. Accepted architecture and security decisions
4. `docs/agent-context/CURRENT_STATE.md`
5. `docs/agent-context/ROADMAP.md` and `PROJECT_BRIEF.md`
6. Historical prompt exports and repomix snapshots

Prompt files describe intent and workflow; they must not be treated as proof that planned architecture exists.

## Start every task

1. Read `PROMPT.md` and the relevant files in `docs/agent-context/`.
2. Inspect the current branch and working tree before consequential work.
3. Inspect the actual source, tests, migrations, and configuration related to the task.
4. Identify pre-existing changes and do not overwrite, discard, stash, stage, or commit them unless the user explicitly asks and the changes are part of the task.
5. State the task scope, non-scope, likely files, acceptance criteria, and validation plan before editing.

## Engineering rules

- Match existing project conventions unless the task deliberately changes them.
- Prefer the smallest coherent change over broad rewrites.
- Keep business rules in testable services/domain code, not templates or route handlers.
- Use strict typed schemas at external boundaries.
- Keep planned and implemented architecture clearly separated in documentation.
- Add or update tests for non-trivial behavior and regressions.
- Run relevant tests, type checks, builds, and migration checks before handoff.
- Review the diff and working tree after editing.
- Do not commit, push, deploy, or open a pull request unless explicitly requested.

## Security and privacy

- Never place API keys, access tokens, cookies, passwords, service-role credentials, private user records, or production exports in source, prompts, logs, tests, or handoffs.
- Never read or print `.env` values unless explicitly required and safe; use `.env.example` for variable names.
- Never use a service-role credential for ordinary user data access.
- Preserve authentication, authorization, CSRF, rate-limit, RLS, and secure-cookie boundaries.
- Redact sensitive data from diagnostics and AI prompts.
- Do not send personal relocation data to a new AI provider without an approved privacy decision.

## Relocation and AI safety

- The deterministic matcher and approved, versioned program data—not an LLM—are authoritative for eligibility and ranking.
- AI output must be grounded, schema-validated, source-aware, and clearly presented as informational rather than legal advice.
- Automated immigration-data retrieval may propose changes, but must not publish legal requirements without human review, provenance, effective dates, and rollback support.
- Free-tier AI capacity is disposable and must never be treated as guaranteed availability.

## Handoff requirements

At the end of meaningful work, update `docs/agent-context/CURRENT_STATE.md` and use `docs/agent-context/HANDOFF_TEMPLATE.md` to report:

- objective and completed work;
- files changed;
- tests/checks run and failures;
- decisions and risks;
- unrelated pre-existing changes;
- the exact next action.

Do not put secrets or private production data in a handoff.
