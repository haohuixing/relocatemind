# Architecture

- **Last reviewed:** 2026-09-20
- **Status:** actual prototype documented; target architecture planned

This document intentionally separates what exists from what is approved for future implementation.

## Actual architecture today

```text
Browser
  ├── Jinja pages rendered by FastAPI
  ├── inline quiz JavaScript with a duplicated matcher
  └── cookies containing auth/result state
          │
          ▼
FastAPI application
  ├── homepage route
  ├── discovery routes and Python matcher
  ├── auth/dashboard routes
  ├── centralized lazy Supabase client helpers, with legacy raw calls still in auth routes
  ├── validated assessment service at the discovery boundary
  ├── signed transitional assessment-input cookie
  └── Jinja2 templates
          │
          ▼
Supabase Auth + PostgreSQL

Static program data: data/countries.json
Static locale data: locales/en.json
```

### Current ownership

- `app/main.py`: app creation, locale loading, auth context middleware, router mounting.
- `app/core/config.py`: centralized environment settings, secure-cookie behavior, and production validation.
- `app/database.py`: cached normal/admin Supabase client factories with no privileged-key fallback.
- `app/core/supabase.py`: compatibility wrapper delegating to `app/database.py`.
- `app/core/auth.py`: HMAC cookie helpers and Supabase user lookup.
- `app/core/i18n.py`: locale discovery, cache, fallback translations.
- `app/core/templates.py`: template directory resolution and Jinja globals.
- `app/modules/auth_router.py`: registration, login, logout, dashboard reads, profile updates.
- `app/modules/discovery/router.py`: quiz page, `/match`, and cookie-backed results page.
- `app/modules/discovery/matcher.py`: file-backed deterministic scoring rules.
- `app/modules/discovery/service.py`: validated assessment boundary and matcher/data version envelope.
- `app/modules/discovery/session.py`: transitional validated assessment-input cookie helpers.
- `app/models/`: Pydantic models, not yet used consistently as the request/domain contract.
- `templates/`: Jinja presentation, including inline UI logic.
- `data/countries.json`: unversioned static program dataset.

## Target modular-monolith architecture

```text
Jinja public pages + quiz UI
              │
              ▼
       Versioned FastAPI API/HTML routes
              │
 ┌────────────┼───────────────┐
 ▼            ▼               ▼
Assessment  Dashboard       Reports
Service     Service         Service
 │            │               │
 └──────┬─────┴───────┬───────┘
        ▼             ▼
 Typed repositories  Provider-neutral AI jobs
        │             │
        └──────┬──────┘
               ▼
      Supabase PostgreSQL/Auth/Storage
               │
       Render web + worker + scheduler
               │
       Reviewed program-data ingestion
```

## Target boundaries

### Assessment and matching

- `AssessmentInput` is the strict canonical input schema.
- The Python domain matcher is the authoritative eligibility/ranking engine.
- Matching returns structured requirements, shortfalls, explanations, score breakdowns, matcher version, and program-data version.
- Browser code presents results; it does not independently decide legal rules.

### Data access

Routes should not contain scattered raw Supabase queries. A typed repository/service boundary should own authorization filters, transactions, serialization, and persistence. The initial repository implementation may use Supabase APIs; direct PostgreSQL access is introduced only when needed for atomic transactions or job claiming.

### Anonymous sessions

The target flow stores assessment inputs and match snapshots server-side. The browser carries only a short-lived opaque session identifier. Registration claims that session once and links it to the authenticated user.

### User workspace

Profiles, saved programs, assessment snapshots, checklist templates, and checklist progress are queryable relational state. Flexible AI output and immutable report context may use JSONB, but core workflow state is not a single blob.

### AI reports

A provider-neutral report service accepts an approved report request, creates an idempotent durable job, calls an allowed provider through an adapter, validates structured output, stores provenance, and exposes status. It never determines eligibility or silently publishes legal requirements.

### Program data

Published programs are immutable versions with sources, retrieval timestamps, effective dates, review status, and rollback support. Ingestion creates proposals; human approval activates changes.

### Frontend

Jinja remains the initial rendering system. Tailwind moves from CDN delivery to compiled/versioned assets. Inline business logic moves into static modules or server/API responses. Accessibility, localization, SEO, and privacy-safe analytics become explicit concerns.

## Deployment target

The approved initial operational shape is:

- Render web service for HTTP traffic;
- Render background worker for AI jobs;
- Render scheduled job for ingestion and cleanup;
- Supabase for managed PostgreSQL/Auth/Storage;
- separate staging and production environments.

The exact deployment configuration is not yet verified in this repository and must be documented when implemented.
