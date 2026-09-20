# Operations Runbook

- **Last reviewed:** 2026-09-20
- **Status:** initial guidance; deployment details require verification

This runbook contains variable names and procedures, not secret values.

## Current local project

The repository is a Python FastAPI application with Jinja templates. Current declared dependencies are in `requirements.txt`. A virtual environment directory exists in the checkout, but agents must follow the project’s active dependency convention and must not install global packages.

Expected environment variable names are documented in `.env.example`, including:

- `SUPABASE_URL`;
- `SUPABASE_ANON_KEY`;
- `SUPABASE_SERVICE_ROLE_KEY`;
- `SECRET_KEY`.

Never copy real values into this file or any context document.

## Baseline checks

Until a formal toolchain is added, use non-destructive checks appropriate to the current repository, for example:

```bash
python -m compileall app
```

When the project adds test/lint/type commands, record the canonical commands here and in CI. Do not claim an application check passed unless it was actually run.

## Local startup

The current module exposes `app.main:app`. The development startup path is expected to use Uvicorn with a local environment configured from `.env`:

```bash
python -m uvicorn app.main:app --reload
```

Verify the actual installed dependencies and environment before relying on this command. Do not expose the app publicly with development reload enabled.

## Environments

Maintain separate:

- local development;
- staging Supabase/Render environment;
- production Supabase/Render environment.

Never point local experiments at production data unless explicitly approved and safely read-only.

## Render target shape

Approved target, not yet fully verified in repository configuration:

- web service: FastAPI HTTP traffic;
- background worker: AI report jobs;
- scheduled job: ingestion, cleanup, freshness checks;
- environment-specific secret settings;
- health/readiness endpoints;
- deploy logs and error monitoring.

Record actual service names, commands, and health URLs once configured.

## Database changes

- Use versioned migrations, not manual one-off production edits.
- Apply migrations to staging first.
- Back up or confirm recoverability before production changes.
- Verify RLS/authorization policies after schema changes.
- Record migration version and rollback notes.
- Never include production data in migration fixtures.

## AI worker failures

When a report is stuck or a provider is rate-limited:

1. Check worker health and job status.
2. Check provider quota/health without printing keys or prompts.
3. Confirm retry count and idempotency behavior.
4. Mark permanently failed jobs safely and expose a retry path.
5. Do not bypass quotas by creating uncontrolled keys or duplicate jobs.
6. Record the incident and update the provider guide if terms changed.

## Program-data rollback

If a published program version is wrong:

1. Stop or disable the affected ingestion/publication job.
2. Identify the bad version and affected assessments/reports.
3. Revert the active program pointer to the last known-good immutable version.
4. Preserve the audit trail and reviewer/source metadata.
5. Re-run matcher regression fixtures.
6. Decide whether affected users require notification or report regeneration.
7. Correct the source proposal before republishing.

## Deployment rollback

Before deployment, record the current application revision, migration level, and active program-data version. If the release is unhealthy:

1. Inspect readiness, errors, latency, worker status, and migrations.
2. Roll back application code using the platform’s supported revision mechanism.
3. Roll back data only through an approved reversible migration or data-version pointer; never destructive-reset production.
4. Confirm health and key user flows.
5. Document the incident and follow-up fix.

## Backups and recovery

Use Supabase-supported backups and verify a restore procedure in a non-production environment. A backup is not considered operationally useful until a restore drill has succeeded and the recovery steps are documented here.

## Operational documentation rule

Update this runbook whenever commands, services, migrations, health checks, backup procedures, provider behavior, or rollback steps change. Never place secret values in operational notes.
