
# Blackletter — Docs Shard Map

This index lists the shard-ready documents for the Blackletter project and gives a recommended reading order. Add new shards here when created.

## Recommended order

1. `docs/prd-blackletter.md` — Product Requirements Document (vision, users, scope, acceptance criteria).
2. `docs/shard-ready-arc.md` — Consolidated architecture overview and system-level constraints (high-level reference).
3. `docs/architecture-blackletter.md` — Shard: system overview, environments & deployment, technology stack.
4. `docs/backlog-blackletter.md` — Shard: epics, stories, and initial acceptance criteria (MVP backlog).
5. `docs/tests-blackletter.md` — Shard: testing strategy, golden fixtures, CI gates.

## Quick links & purpose

- `docs/prd-blackletter.md` — The canonical PRD describing MVP features, user personas, and acceptance criteria.
- `docs/shard-ready-arc.md` — A single-file reference of the fullstack architecture for quick handoffs.
- `docs/architecture-blackletter.md` — Sharded architecture content intended for handoff to architects and infra.
- `docs/backlog-blackletter.md` — The epic/story map to use for sprint planning and backlog creation.
- `docs/tests-blackletter.md` — Testing and QA plans, golden fixtures, and CI gating rules.

## How to add or update a shard

1. Create or edit a markdown file under `docs/` with a clear title and responsibilities.
2. Add an entry to this `SHARD_MAP.md` with a one-line description and suggested place in the reading order.
3. Commit and push; open a PR if the change affects more than documentation (or per your repo rules).

## Ownership

- Docs owner: Winston (Architect) — owns architectural shards.
- PRD owner: John (PM) — owns product requirements and acceptance criteria.

---
Generated: 2025-09-02
