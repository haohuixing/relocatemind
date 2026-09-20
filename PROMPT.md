# RelocateMind Agent Context

You are joining an ongoing software project. Do not assume that a planned feature exists because an older prompt describes it. Inspect the repository and verify the current state before editing.

## Product in one paragraph

RelocateMind is a global relocation discovery and planning platform. Stage 1 is a deterministic, low-cost assessment that compares a user's passport, income, income type, savings, household, region, and goals against versioned relocation programs. Stage 2 is a registered workspace that may generate bounded, grounded AI reports and persistent action plans. Eligibility and rankings must remain deterministic; AI is an explanation and planning layer, not a legal authority.

## Strategic direction

The approved direction is incremental hardening, not a rewrite:

- Keep FastAPI, Python, Supabase PostgreSQL/Auth, Jinja, and Tailwind initially.
- Preserve the Jinja frontend while improving asset delivery, accessibility, and API boundaries.
- Evolve the prototype into a modular monolith with typed schemas, repositories/services, versioned data, durable jobs, and observability.
- Use a provider-neutral AI service. Gemini 3.8 Flash is the initial development candidate; free capacity is not guaranteed. Providers must be replaceable and privacy-reviewed.
- Require human approval before automated immigration-data changes become active.
- Build reports first; defer unrestricted chat, a marketplace, microservices, Kubernetes, and a full frontend rewrite.

## Required reading order

1. `AGENTS.md`
2. `docs/agent-context/README.md`
3. `docs/agent-context/PROJECT_BRIEF.md`
4. `docs/agent-context/CURRENT_STATE.md`
5. `docs/agent-context/ARCHITECTURE.md`
6. `docs/agent-context/ROADMAP.md`
7. Read `SECURITY_RULES.md`, `DATA_GOVERNANCE.md`, `AI_PROVIDER_GUIDE.md`, or `OPERATIONS_RUNBOOK.md` when relevant.
8. Inspect the actual source, tests, migrations, and current Git status.

## Context authority

Source code, tests, migrations, and verified runtime behavior outrank these documents. Accepted decisions and current-state notes explain intent but cannot override what the repository proves. The root `PROMPT.txt` is retained as historical context and is not canonical; do not use it instead of these documents.

## Non-negotiable safety rules

- Never expose or commit secrets, tokens, private user data, or production exports.
- Preserve unrelated working-tree changes.
- Do not claim that planned target architecture is implemented until it is verified.
- Do not let an LLM decide visa eligibility or publish legal requirements.
- Run relevant validation and leave a precise handoff after meaningful work.

## Current phase

The context system has been added. The application itself remains a prototype and still requires the engineering overhaul described in `docs/agent-context/ROADMAP.md`. Begin future implementation from `CURRENT_STATE.md`, not from assumptions in the historical prompt.
