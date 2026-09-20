# AI Provider Guide

- **Last reviewed:** 2026-09-20
- **Status:** provider strategy approved; integration planned

## Role of AI

AI is a bounded explanation and planning layer. It may summarize approved program facts, organize a user's action plan, draft non-authoritative letters, and explain trade-offs. It must not determine visa eligibility, replace the matcher, invent requirements, or present tax/legal advice as certain.

## Provider-neutral contract

Implement a provider adapter behind a common service contract. The contract should expose capabilities rather than provider-specific behavior:

- structured report generation;
- JSON/schema-constrained output;
- streaming support if later needed;
- vision/document support if explicitly approved;
- maximum context/output limits;
- privacy classification;
- health/availability;
- usage and cost metadata.

The product report service owns prompts, schemas, grounding, quotas, retries, idempotency, provenance, and user-facing status. Routes must not call vendor SDKs directly.

## Grounding rules

Every report request should use:

- normalized assessment input;
- approved match snapshot;
- active program-data version;
- source metadata and freshness;
- report type and schema version;
- legal-safety disclaimer version.

The model should not receive arbitrary database dumps or unnecessary identity information. Generated output must be validated against Pydantic schemas before storage or display.

## Report-first scope

Start with bounded outputs:

- relocation strategy dossier;
- structured program comparison;
- document/action plan;
- consulate preparation draft.

Defer unrestricted concierge chat until report quality, cost controls, privacy policy, and escalation behavior are proven.

## Current development provider strategy

### Gemini 3.8 Flash

Initial development candidate because the current official Gemini API pricing documentation lists Free-tier input/output access for certain Gemini 3.x Flash models. Free-tier quota is model/project dependent and can change. Free-tier content may be used to improve Google products, so sensitive production user data requires an explicit privacy decision and should not be routed casually.

Official references to recheck before use:

- https://ai.google.dev/gemini-api/docs/pricing
- https://ai.google.dev/gemini-api/docs/billing
- https://ai.google.dev/gemini-api/docs/rate-limits

### Groq

Potential fallback/evaluation provider with fast hosted open-weight models and OpenAI-compatible patterns. Exact free-tier limits are account-specific and lower than paid/developer limits. Verify current quota and data policy before routing real user data.

Reference: https://console.groq.com/docs/rate-limits

### OpenRouter

Useful for development comparison and model experimentation. Free variants have low, changing rate limits and pass requests through upstream providers. Do not treat it as guaranteed production capacity or route sensitive data without an approved provider/privacy configuration.

References:

- https://openrouter.ai/docs/faq
- https://openrouter.ai/docs/api-reference/limits

### Cloudflare Workers AI

Useful for selected lightweight tasks such as classification, extraction, embeddings, or moderation. The free allocation is daily and model-specific; some frontier models require paid billing. Do not assume free models are equivalent to a frontier report model.

Reference: https://developers.cloudflare.com/workers-ai/platform/pricing/

### Cerebras and trial-credit services

Fast inference and trial credits can be useful for benchmarking, but a time/credit-bounded trial is not a permanent free-tier dependency. Treat it as optional evaluation capacity.

## Quotas and cost controls

Enforce controls before provider calls:

- per-user daily/monthly report quota;
- global daily spend/request cap;
- maximum input and output tokens;
- provider/model allowlist;
- concurrency limit;
- timeout and retry budget;
- circuit breaker for unhealthy providers;
- usage and estimated-cost event;
- graceful queued/unavailable response when capacity is exhausted.

Free-tier capacity is disposable. The product must never promise immediate generation solely because a provider currently has a free quota.

## Privacy routing

Classify requests before routing:

- synthetic benchmark data;
- de-identified development data;
- ordinary user profile data;
- highly sensitive identity/document data.

Each provider must have a documented data-use posture. Do not route a more sensitive class to a provider until the privacy decision is accepted. Redact names, emails, exact document numbers, and unnecessary identifiers.

## Quality and safety evaluation

Maintain a fixed benchmark set of representative relocation profiles and expected properties. Compare providers on:

- factual grounding to supplied program data;
- schema validity;
- citation/source preservation;
- refusal to invent legal requirements;
- consistency across repeated calls;
- latency;
- token usage/cost;
- multilingual quality where relevant.

Model names, parameter counts, and public benchmark claims are not substitutes for application-specific evaluation.

## Job behavior

AI requests should be durable jobs:

```text
queued → running → completed
              ↘ retrying → failed
```

Jobs must be idempotent, retryable with backoff, bounded by a timeout, and associated with an assessment/program/prompt/model version. Store failed status and a safe user-facing message rather than exposing provider internals.
