---
name: adr
description: Create or update an Architecture Decision Record (ADR) to permanently log a technical decision. Use when the user says "log this decision", "write an ADR", "document why we chose", "record this choice", "architecture decision", "why did we pick X", or whenever a significant technical tradeoff is resolved (choosing a framework, DB schema pattern, auth strategy, API design, etc.). ADRs are the project's permanent memory — they explain the *why* behind decisions so future agents and developers don't undo them.
---

# ADR Skill

Creates a single **Architecture Decision Record** — a short, permanent file that explains a technical decision and why it was made. Stored in `/docs/adr/` or project root.

## File Naming

`ADR-[number]-[short-slug].md`  
Example: `ADR-003-use-jwt-for-auth.md`

## Output Format

```markdown
# ADR-[N]: [Title]

**Date:** [date]  
**Status:** Accepted

## Decision
One sentence. What did we choose?

## Context
2–3 sentences. What problem forced this decision? What constraints existed?

## Alternatives Considered
| Option | Why Rejected |
|--------|--------------|
| [alt 1] | [reason] |
| [alt 2] | [reason] |

## Consequences
- ✅ [upside]
- ⚠️ [tradeoff or known risk]
```

## Rules

- **Status options:** Proposed / Accepted / Deprecated / Superseded by ADR-N
- One decision per file. Never bundle multiple decisions.
- Consequences must include at least one ⚠️ — every decision has a tradeoff.
- Write for a future agent who has zero session context.

## Usage

Save the file to `docs/adr/`. If `CLAUDE.md` exists in the project, add a one-line reference:
```
- ADR-003: JWT for auth — see docs/adr/ADR-003-use-jwt-for-auth.md
```
This keeps the Context-Anchor current without bloating it.