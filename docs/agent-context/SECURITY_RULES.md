# Security Rules

- **Last reviewed:** 2026-09-20
- **Status:** required policy; implementation incomplete

## Secrets

Never commit or place in context files:

- Supabase service-role keys;
- Supabase anon keys when repository policy prohibits them;
- Gemini, Groq, OpenRouter, or other provider keys;
- session/access/refresh tokens;
- passwords or signing secrets;
- production connection strings;
- private customer records or raw exports.

Use `.env.example` only for variable names and safe placeholders. Production secrets belong in the deployment secret manager. Do not print `.env` contents during diagnostics.

The application must fail fast in production when required secrets are absent or equal to known insecure placeholders.

## Authentication and sessions

- Keep Supabase Auth as the identity provider unless an accepted ADR changes it.
- Use secure, HTTP-only, appropriately scoped cookies.
- Enable `Secure` in production and define SameSite/expiry behavior deliberately.
- Never expose access tokens to browser JavaScript.
- Avoid an unbounded remote auth lookup on every request; use a deliberate validation/cache/session design.
- Logout must invalidate/clear application session state.
- Prevent session fixation and one-time anonymous-session claim abuse.
- Do not use the anonymous Supabase client as a silent substitute for a service-role client.

## Authorization and data access

- Every user-owned query/update must be scoped by authenticated user ID.
- Enforce ownership in both application repositories and database/RLS policies where applicable.
- Keep service-role access in narrow privileged operations only.
- Admin operations need an explicit role/permission boundary and audit trail.
- Never trust a user-supplied ID without authorization checks.

## Web security

- Protect state-changing browser requests with CSRF tokens and origin checks.
- Rate-limit login, registration, matching, report generation, and admin/ingestion operations.
- Add secure response headers, including a carefully tested Content Security Policy.
- Validate all external input with typed schemas and bounds.
- Use generic authentication errors to reduce account enumeration.
- Escape/render user content safely; do not mark untrusted HTML safe.
- Keep dependencies updated and locked.

## Logging and observability

- Add request IDs and structured logs.
- Redact authorization headers, cookies, passwords, emails where unnecessary, exact income/passport data, AI prompts, and report contents.
- Do not log raw provider requests/responses by default.
- Keep audit events separate from debug logs and minimize personal data.

## AI privacy

- Send only the minimum information required for the requested report.
- Remove names, emails, document numbers, and unrelated identifiers.
- Record provider/model/privacy mode for each report job.
- Do not route sensitive data through an unreviewed free provider or aggregator.
- Treat provider free-tier data-use terms as material to the privacy decision.

## Relocation-data safety

- The matcher and approved versioned data determine eligibility/ranking.
- AI output must be grounded and marked informational/not legal advice.
- No scraped or model-generated requirement may be activated without human review and source attribution.
- Preserve historical input/data/report versions.

## Privacy lifecycle

Plan for:

- consent where required;
- data minimization;
- retention and cleanup of anonymous sessions;
- user export and deletion;
- report deletion;
- provider deletion/data-use policies;
- incident response and secret rotation.
