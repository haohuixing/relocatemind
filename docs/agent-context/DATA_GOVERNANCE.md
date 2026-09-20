# Relocation Data Governance

- **Last reviewed:** 2026-09-20
- **Status:** policy approved; ingestion workflow planned

RelocateMind deals with immigration, residency, tax, and relocation information that may change and may affect consequential user decisions. Data must be treated as informational, sourced, versioned, and reviewable.

## Core rule

Automated retrieval may discover, cache, normalize, validate, and propose a change. It may not activate a legal or program requirement without human approval.

The matcher must never imply that a result is legal advice or a guarantee of approval.

## Source records

Every published program requirement should have:

- jurisdiction and program identifier;
- source URL or official document reference;
- source type and authority level;
- retrieval timestamp;
- source snapshot or content hash where permitted;
- effective date, if known;
- last verified date;
- reviewer identity and review timestamp;
- active program-data version;
- confidence or review status.

Prefer official government sources. Trusted secondary sources may supplement but should not silently replace an official source for high-impact requirements.

## Proposed ingestion flow

```text
Discover source
  → retrieve/cache within terms
  → normalize into schema
  → validate types and sanity constraints
  → detect/diff changes
  → create review proposal
  → human review and approval
  → publish immutable version
  → activate matcher snapshot
```

## Validation requirements

Validate at minimum:

- required fields and types;
- currency and unit normalization;
- non-negative monetary values;
- valid dependent percentages;
- valid regions and income-type enums;
- processing/citizenship duration sanity;
- source and effective-date presence;
- no accidental removal of required fields;
- no unexplained extreme changes;
- cross-field consistency.

Large or legally significant changes require explicit reviewer attention.

## Versioning and rollback

- Published program versions are immutable.
- Assessments and AI reports retain the program-data version used.
- New publication creates a new version rather than mutating history.
- Every publication can be rolled back to a prior known-good version.
- Stale or withdrawn programs are marked, not silently deleted.

## User-facing behavior

- Show last verified/freshness information where appropriate.
- Provide source attribution for important requirements.
- Use uncertainty language when data is incomplete or stale.
- Tell users to confirm current requirements with the relevant authority or qualified professional.
- Never promise visa approval, tax outcomes, citizenship, or processing times.

## Privacy and retention

- Collect only inputs needed for the matching/planning purpose.
- Do not store raw identity documents unless a separately approved feature requires it.
- Define retention and deletion for anonymous assessments, user profiles, reports, logs, and raw source snapshots.
- Do not include emails, income, passport data, or private user records in analytics or context files unnecessarily.
- AI prompts must use the minimum necessary data and follow the provider privacy classification.

## Prohibited shortcuts

- No direct scraper-to-production publication.
- No uncited legal claims in the active dataset.
- No LLM-generated requirement treated as a source.
- No silently changing a historical match or report because current data changed.
- No “verified” label without a review record.
