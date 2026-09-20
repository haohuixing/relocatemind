# Current Project State

- **Last verified:** 2026-09-20
- **Branch at verification:** `main`
- **Overall status:** `in progress`
- **Current milestone:** Foundation hardening in progress; canonical assessment boundary implemented

## What is implemented

The repository currently contains a small FastAPI/Jinja prototype with:

- a homepage and server-rendered templates;
- Supabase Auth registration/login/dashboard flows;
- a Supabase client in `app/database.py` and a second client helper in `app/core/supabase.py`;
- a deterministic Python matcher in `app/modules/discovery/matcher.py`;
- a static `data/countries.json` program index;
- an interactive seven-step quiz in `templates/free_test.html`;
- signed anonymous result data in an `anon_test_data` cookie;
- a user profile table integration using `matches_json` and `checklist_json`;
- browser-only checklist progress updates;
- locale loading from `locales/en.json` with fallback strings.

The approved target architecture—typed repositories, true server-side versioned assessment sessions, persistent checklist state, durable AI jobs, reviewed ingestion, compiled assets, observability, and provider abstraction—is still largely **planned, not implemented**. This task implements the first foundation slice: centralized configuration, validated assessment/match contracts, a discovery service boundary, transitional validated assessment cookies, and regression tests.

## Verified repository condition

The context-system task added `AGENTS.md`, `PROMPT.md`, `docs/agent-context/*.md`, and the README agent-context pointer. These files are owned by this task.

The working tree was not clean during context-system work. Pre-existing changes that this task does not own:

- modified `PROMPT.txt`;
- modified `app/modules/discovery/matcher.py`;
- modified `data/countries.json`;
- modified `templates/free_test.html`;
- untracked `.freebuff/` directory.

Do not overwrite, reset, stash, stage, or commit these changes as part of unrelated work.

## Known implementation risks

1. The duplicate Supabase modules now delegate through centralized lazy client helpers, but route-level repository/service separation is not complete.
2. The service-role client no longer silently falls back to the anonymous client, but it is still used broadly by legacy dashboard routes.
3. Authentication performs a remote Supabase user lookup synchronously in request middleware/routes.
4. The anonymous cookie now stores only a validated assessment input snapshot and derives matches server-side; it is still a transitional signed cookie rather than the planned opaque server-side assessment session.
5. Python matching rules are still duplicated in browser JavaScript and can drift.
6. The canonical assessment schema now accepts climate/timeline, while the current matcher only uses the fields implemented in its scoring rules; these fields still need deliberate scoring or UI removal.
7. The profile/dashboard flow still stores matches/checklist state as legacy JSON and checklist completion is not persisted.
9. The program dataset lacks source provenance, effective dates, review status, freshness, and version history.
10. Requirements are broad ranges and there is no visible test, migration, CI, health-check, rate-limit, CSRF, observability, or deployment automation layer.
11. Tailwind is loaded from a CDN and the language selector currently logs rather than switches locale.

## Current validation record

- Repository inspection performed on 2026-09-20.
- A first regression suite now exists at `tests/test_assessment_contract.py`.
- Validation of the context and foundation changes included file/directory review, `git diff --check`, `venv/Scripts/python.exe -m compileall app tests`, `venv/Scripts/python.exe -m unittest discover -s tests -v`, and application import verification.
- The current three assessment contract tests pass.
- Live Supabase route behavior still requires staging credentials and has not been exercised here.
- The next implementation agent should add route/session tests and then implement true server-side anonymous assessment persistence.

## Context-system completion

The layered handoff system is implemented in the owned files listed above. The first foundation hardening slice is also implemented in `app/core/config.py`, the centralized Supabase helpers, `app/models/profile.py`, `app/modules/discovery/service.py`, `app/modules/discovery/session.py`, the updated discovery/auth boundaries, and `tests/test_assessment_contract.py`. The root `PROMPT.txt` remains untouched by this task because it already had unrelated working-tree edits; `LEGACY_PROMPT_NOTICE.md` marks it as historical rather than canonical.

## Immediate next action

Start the engineering overhaul with a non-destructive baseline:

1. add route-level tests for invalid/valid `/match` submissions and transitional cookie reads;
2. replace the transitional signed assessment cookie with an opaque server-side assessment session and migration path;
3. move legacy auth/dashboard Supabase calls behind typed repositories;
4. add CSRF/rate limiting and secure session tests;
5. then introduce database migrations for persistent assessment snapshots and checklist progress.

## Unresolved decisions

- Whether the application will use Supabase’s SDK behind typed repositories or add a direct PostgreSQL/SQLAlchemy layer for transactional workflows.
- Exact application-session strategy after Supabase Auth token validation is redesigned.
- Which AI providers pass the privacy and quality benchmark for real user reports.
- Exact schema and source set for human-reviewed program-data ingestion.
