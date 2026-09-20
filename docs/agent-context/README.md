# Agent Context System

This directory contains the durable, versioned context that helps future agents resume RelocateMind work after a conversation or model context is cleared.

## Purpose

These files preserve product intent, verified current state, architecture, decisions, safety constraints, operations knowledge, and repeatable task/handoff formats. They are deliberately separated so stable product context does not get confused with fast-changing implementation state.

## Authority

Use this order when documents disagree:

1. Current source code, tests, migrations, and verified runtime behavior
2. Safe inspection of staging/live configuration and schema
3. Accepted decisions in `DECISIONS.md`
4. `CURRENT_STATE.md`
5. `ARCHITECTURE.md`, `ROADMAP.md`, and `PROJECT_BRIEF.md`
6. Historical prompt exports, including root `PROMPT.txt`

Context files explain intent; they do not override verified behavior.

## Reading order

Every incoming agent should read:

1. Root `AGENTS.md`
2. Root `PROMPT.md`
3. This `README.md`
4. `PROJECT_BRIEF.md`
5. `CURRENT_STATE.md`
6. `ARCHITECTURE.md`
7. `ROADMAP.md`
8. The safety/runbook documents relevant to the task
9. The actual source, tests, migrations, and configuration for the assigned area

## Files

- `PROJECT_BRIEF.md`: stable product and strategy context.
- `CURRENT_STATE.md`: current implementation facts, blockers, validation, and next action.
- `ARCHITECTURE.md`: actual-versus-target system boundaries and data flows.
- `ROADMAP.md`: milestones, dependencies, acceptance criteria, and deferred work.
- `DECISIONS.md`: append-only architectural decision records.
- `DATA_GOVERNANCE.md`: immigration-data provenance, review, freshness, and privacy rules.
- `AI_PROVIDER_GUIDE.md`: provider abstraction, quality, privacy, quotas, and fallback rules.
- `SECURITY_RULES.md`: secrets, authentication, authorization, web security, and data handling.
- `OPERATIONS_RUNBOOK.md`: local, staging, Render, database, worker, and recovery procedures.
- `TASK_TEMPLATE.md`: reusable task brief.
- `HANDOFF_TEMPLATE.md`: reusable end-of-session handoff.

## Status labels

Use these labels consistently:

- `implemented`: verified in the repository and by the stated checks;
- `in progress`: actively being changed;
- `planned`: approved intent not yet implemented;
- `blocked`: cannot proceed without an external decision/dependency;
- `superseded`: intentionally replaced by a newer decision or design.

## Maintenance rules

- Update `CURRENT_STATE.md` after every meaningful implementation session.
- Update `ARCHITECTURE.md` when actual boundaries or data flow change; keep target design separate.
- Update `ROADMAP.md` when milestone scope, dependencies, or status change.
- Append an ADR to `DECISIONS.md` for material architecture, security, data, AI, product, or deployment decisions.
- Update governance, provider, security, and operations files when their rules or external terms change.
- Put dates on mutable state and mark stale information as superseded instead of silently leaving contradictions.
- Do not put secrets, tokens, private user data, raw production exports, or sensitive logs in any context file.
- Do not treat `repomix-output.xml` as authoritative; it is an optional snapshot only.

## Ownership

A task should declare the files/components it owns. Agents must preserve unrelated user or agent changes and mention them in the handoff. Documentation should only claim completed work after the implementation and validation are complete.
