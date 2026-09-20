# Architectural Decision Records

This file is append-only. Add new records rather than rewriting accepted history. Supersede an old decision explicitly when necessary.

## ADR-0001: Evolve the current stack incrementally

- **Date:** 2026-09-20
- **Status:** accepted
- **Scope:** architecture

### Context

RelocateMind is an early FastAPI/Supabase/Jinja prototype. A full framework or infrastructure rewrite would create migration cost before product-market validation.

### Decision

Keep FastAPI, Python, Supabase PostgreSQL/Auth, Jinja, and Tailwind initially. Improve boundaries, testing, data modeling, security, workers, and operations incrementally.

### Alternatives considered

- Full frontend/backend rewrite.
- Immediate microservices and cloud-native platform migration.

### Consequences

The team can ship hardening work faster and preserve existing product behavior. Some prototype boundaries must be carefully replaced over time.

### Revisit when

Traffic, team size, product interaction complexity, or operational requirements make the modular monolith a demonstrated bottleneck.

## ADR-0002: Use a modular monolith before microservices

- **Date:** 2026-09-20
- **Status:** accepted
- **Scope:** architecture/deployment

### Context

The product needs clearer boundaries and background jobs, but its scale and team size do not justify distributed service operations.

### Decision

Keep one repository and product while separating web, worker, and scheduled processes behind domain/service boundaries. Introduce independent services only after measured need.

### Alternatives considered

- Microservices from the start.
- One unstructured web process forever.

### Consequences

Lower operational overhead with a path to later extraction. Boundary discipline and tests are required to prevent the monolith from becoming tangled.

### Revisit when

A component has independent scaling, security, reliability, or deployment needs that are proven in production.

## ADR-0003: Make the deterministic matcher authoritative

- **Date:** 2026-09-20
- **Status:** accepted
- **Scope:** product/data/AI

### Context

Eligibility and ranking must be explainable and low cost. The current browser and Python implementations can drift.

### Decision

Use a versioned, validated Python domain matcher as the authoritative source for eligibility, requirements, rankings, shortfalls, and score explanations. Browser code presents results rather than independently deciding legal rules.

### Alternatives considered

- Let an LLM determine eligibility.
- Maintain separate browser and server scoring engines.

### Consequences

Results are more testable and auditable. The UI may need preview API calls or contract fixtures to preserve responsiveness.

### Revisit when

A formal alternative engine is introduced with complete parity tests and an explicit governance decision.

## ADR-0004: Require human approval for legal-data publication

- **Date:** 2026-09-20
- **Status:** accepted
- **Scope:** data/governance

### Context

Automated source retrieval can detect changes, but immigration requirements and tax claims are high-impact and may be ambiguous or stale.

### Decision

Automation may retrieve, normalize, validate, and propose changes. No legal/program requirement becomes active without human review, source attribution, effective dates, versioning, and rollback.

### Alternatives considered

- Auto-publish trusted-source changes.
- Manual-only data maintenance.

### Consequences

Publication is slower but safer, auditable, and reversible. An internal review workflow is required.

### Revisit when

A constrained source class and validation process demonstrate safe automated publication under an explicitly approved policy.

## ADR-0005: Build a provider-neutral AI service before report features

- **Date:** 2026-09-20
- **Status:** accepted
- **Scope:** AI/architecture

### Context

Provider quality, quotas, pricing, privacy policies, and model availability change. The project is not investing in API usage yet and needs a free-tier path.

### Decision

Define a provider-neutral capability and report contract before coupling routes to one vendor. Start development with Gemini 3.8 Flash Free when appropriate, but keep adapters replaceable and quotas disposable.

### Alternatives considered

- Hard-code Gemini calls into dashboard routes.
- Route sensitive data through arbitrary free-model aggregators.

### Consequences

Slightly more initial abstraction work, but lower switching risk and clearer privacy/quality controls.

### Revisit when

A provider becomes a strategic dependency with contractual privacy, reliability, or volume guarantees.

## ADR-0006: Reports before unrestricted chat or marketplace

- **Date:** 2026-09-20
- **Status:** accepted
- **Scope:** product/AI

### Context

Bounded reports are easier to validate, meter, cache, and ground than open-ended chat or expert workflows.

### Decision

Launch bounded personalized reports and action plans first. Defer unrestricted chat and an expert marketplace until report quality, usage controls, and data operations are proven.

### Alternatives considered

- Build a concierge chatbot first.
- Build provider referrals and booking workflows first.

### Consequences

The initial product is narrower but safer, cheaper, and easier to evaluate.

### Revisit when

Validated users demonstrate sustained demand and the safety/operational controls are ready.
