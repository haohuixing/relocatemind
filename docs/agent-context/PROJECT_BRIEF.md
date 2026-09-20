# RelocateMind Project Brief

- **Last reviewed:** 2026-09-20
- **Status:** implemented product direction; prototype implementation

## Mission

RelocateMind helps digital nomads, remote employees, freelancers, and internationally mobile families discover realistic relocation pathways and execute a move with clearer next steps.

The product should move a user from:

```text
Discover → Assess → Compare → Save → Plan → Execute
```

## Product layers

### Stage 1: deterministic discovery

An anonymous assessment collects relevant profile inputs and compares them against relocation programs. The engine should explain hard requirements, financial shortfalls, program fit, and trade-offs quickly without an LLM call.

### Stage 2: registered planning workspace

A registered user can preserve assessments, manage a checklist, and request bounded AI-generated planning documents. AI content must use approved program snapshots and clearly state uncertainty and legal limitations.

## Target users

- digital nomads;
- remote employees;
- freelancers and self-employed professionals;
- people comparing residency or visa pathways;
- couples and families evaluating relocation options.

## Business direction

The approved initial commercial direction is **freemium SaaS, reports first**:

- free deterministic matching;
- account creation to preserve plans;
- bounded personalized reports and action plans;
- future paid reports, quotas, and subscriptions;
- defer an expert marketplace until the core product and data operations are reliable.

## Technology direction

Keep and improve the current stack incrementally:

- FastAPI and Python for web and domain logic;
- Supabase PostgreSQL and Auth initially;
- Jinja for acquisition and dashboard pages;
- compiled Tailwind/static assets as the frontend matures;
- versioned, provenance-aware program data;
- provider-neutral asynchronous AI reports;
- Render web, worker, and scheduled processes as the initial deployment shape.

## Product principles

1. Eligibility and ranking are deterministic and explainable.
2. AI does not determine legal eligibility or silently invent requirements.
3. Immigration data must have sources, timestamps, versions, review, and rollback.
4. Privacy and user trust are more important than maximizing AI output volume.
5. A free provider quota is useful for development but is not a reliability guarantee.
6. Historical assessments and reports must remain explainable after data changes.

## Explicit non-goals for the current phase

Do not prematurely introduce:

- microservices;
- Kubernetes or multi-region infrastructure;
- a full React/Next.js rewrite;
- unrestricted AI chat;
- automatic legal-data publication;
- a vector database before retrieval needs are proven;
- machine-learned ranking before sufficient validated behavior data exists;
- tax or legal advice presented as authoritative computation.
