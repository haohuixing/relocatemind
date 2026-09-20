# Application Overhaul Roadmap

- **Last reviewed:** 2026-09-20
- **Status:** approved plan; implementation pending except context foundation

## Milestone status

| Milestone | Status | Main outcome |
|---|---|---|
| Context foundation | implemented | Versioned agent instructions, state, architecture, governance, and handoff templates |
| 0. Baseline and safety | in progress | Reproducible baseline, staging separation, regression fixtures, ADRs |
| 1. Engineering foundation | in progress | Centralized configuration, startup validation, checks, initial tests |
| 2. Security and sessions | in progress | Baseline headers/cookies added; CSRF/rate limits/session redesign pending |
| 3. Canonical assessment/matcher | in progress | Validated input contract and authoritative service boundary added; browser parity pending |
| 4. Data model/repositories | planned | Versioned programs, assessments, snapshots, persistent checklist state |
| 5. Anonymous assessment migration | planned | Opaque server-side sessions and safe account claiming |
| 6. AI provider/report service | planned | Provider abstraction, grounded schemas, privacy controls, bounded reports |
| 7. Jobs and monetization readiness | planned | Idempotent worker jobs, quotas, usage tracking, future entitlements |
| 8. Reviewed legal-data ingestion | planned | Provenance, proposals, human review, publication, rollback |
| 9. Frontend/operations hardening | planned | Compiled assets, accessibility, SEO, observability, backups, runbooks |

## Milestone 0 — Baseline and safety

### Scope

- Preserve existing working-tree changes.
- Record current route behavior and matcher outputs.
- Confirm staging/production boundaries.
- Define architecture, privacy, AI, and legal-data ADRs.

### Acceptance criteria

- Baseline behavior is reproducible.
- Existing user changes are not overwritten.
- Representative matcher fixtures exist.
- Staging and production credentials are not mixed.

## Milestone 1 — Engineering foundation

### Scope

- Move dependency metadata to a reproducible/locked configuration.
- Consolidate duplicate Supabase configuration.
- Add migrations, CI, formatting, linting, typing, tests, and environment validation.
- Fail fast on missing or insecure production secrets.

### Acceptance criteria

- Clean setup can install, test, migrate, and start.
- CI blocks failing checks.
- One authoritative database configuration path exists.

## Milestone 2 — Security and sessions

### Scope

- Harden Supabase Auth integration and application sessions.
- Use secure HTTP-only cookies with explicit expiry/revocation.
- Restrict service-role usage.
- Add CSRF, rate limits, request IDs, secure headers, redacted logs, and ownership tests.

### Acceptance criteria

- No cross-user data access.
- No tokens in client JavaScript or logs.
- Unsafe forms require CSRF protection.
- Authentication/report abuse is throttled.

## Milestone 3 — Canonical assessment and matcher

### Scope

- Create strict `AssessmentInput` and output schemas.
- Make Python the authoritative matcher.
- Resolve EU data and implement/remove exposed fields such as climate and timeline.
- Add structured score breakdowns and explanations.
- Remove or contract-test browser-side business rules.

### Acceptance criteria

- Fixed inputs produce deterministic, versioned results.
- Eligibility and ranking are distinct and explainable.
- Python/UI contract cannot silently drift.

## Milestone 4 — Data model and repositories

### Scope

- Add versioned program/source records.
- Add assessment sessions, immutable match snapshots, saved programs, checklist templates, and checklist progress.
- Keep JSONB for flexible report output/snapshots, not all workflow state.
- Add typed repository and transaction boundaries.

### Acceptance criteria

- Historical results remain explainable after data changes.
- Checklist state persists across devices.
- User ownership is enforced in repositories and database policies.

## Milestone 5 — Anonymous assessment migration

### Scope

- Replace full result cookies with opaque server-side assessment IDs.
- Add expiry, one-time claim, fixation protection, and cleanup.

### Acceptance criteria

- Anonymous results survive navigation without sensitive cookie payloads.
- A session can be claimed exactly once by the correct account.

## Milestone 6 — AI provider and report service

### Scope

- Define provider-neutral capabilities and adapters.
- Implement Gemini initial adapter and test optional fallback adapters.
- Ground reports only in approved snapshots.
- Validate structured output and store model/prompt/data provenance.
- Add redaction and explicit privacy classification.

### Acceptance criteria

- No LLM determines eligibility.
- Report output is schema-valid and source-aware.
- Provider can be changed without changing product routes.
- Free-quota exhaustion degrades gracefully.

## Milestone 7 — Jobs and monetization readiness

### Scope

- Add durable AI jobs and Render worker.
- Add retries, idempotency, timeouts, quotas, usage/cost events, and report caching.
- Add future entitlement boundaries without requiring billing immediately.

### Acceptance criteria

- Web requests do not wait for generation.
- Duplicate clicks do not create duplicate billable jobs.
- Per-user and global caps are enforced.

## Milestone 8 — Human-reviewed program-data ingestion

### Scope

- Retrieve, cache, normalize, validate, diff, review, publish, and rollback program versions.
- Require citations, source freshness, effective dates, reviewer identity, and stale-data behavior.

### Acceptance criteria

- Automation cannot activate legal changes without approval.
- Every active rule is attributable, versioned, and reversible.

## Milestone 9 — Frontend and operations hardening

### Scope

- Compile assets and remove CDN dependency.
- Move inline JavaScript business logic into versioned modules/API contracts.
- Add accessibility, localization, SEO, consent-aware analytics.
- Add structured logs, health endpoints, monitoring, backups, restore drills, and rollback procedures.

### Acceptance criteria

- Core flows are keyboard/accessibility tested.
- Production deployment is observable and recoverable.
- Operational procedures are documented without secrets.

## Explicitly deferred

- Microservices and Kubernetes.
- Full frontend replacement.
- Unrestricted AI chatbot.
- Automatic legal-data publication.
- Expert marketplace.
- Vector database without a proven retrieval requirement.
- ML ranking before validated behavioral data exists.
