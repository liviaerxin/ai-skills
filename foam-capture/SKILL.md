---
name: foam-capture
description: Extracts a chat conversation or URL into a structured Foam PKG note ready to save into VS Code + GitHub. Trigger when the user says "save to foam", "capture to knowledge base", "save this chat", "add to PKG", "save to foam vault", "log to foam", or pastes a Claude/ChatGPT URL or raw markdown chat they want to preserve. Fetches the URL if provided, then generates a complete Foam-ready .mdx file with auto-generated frontmatter — title, tags, description, keywords — based on the content. Reads live templates from .foam/templates/ if available, falls back to hardcoded templates.
---

# Foam Capture Skill

Turns a raw chat (pasted markdown or public URL) into a production-ready Foam `.mdx` note with auto-generated metadata, ready to drop into your VS Code + GitHub vault.

---

## Step 0 — Load the Right Template

**First, determine note type from the content:**

| Content type | Template to load | Output folder |
|---|---|---|
| Tutorial, walkthrough, opinion, workflow | `blog` template | `blog/` |
| Reference, architecture, how-to, technical spec | `doc` template | `docs/` |

**Then try to read the live template from disk:**

```
Try: .foam/templates/blog.md   → use for blog type
Try: .foam/templates/doc.md    → use for doc type
```

**Decision logic:**
- ✅ File found → read it, extract its frontmatter structure and body sections, use as the output contract for Step 3
- ❌ File not found → fall back to the hardcoded templates at the bottom of this skill
- 🔍 If in Claude Code: use `Read File` tool on `.foam/templates/blog.md` or `.foam/templates/doc.md`
- 🌐 If in Claude.ai web UI: filesystem unavailable — go straight to fallback templates

Always tell the user which template was used:
> "Using live template from `.foam/templates/blog.md`" or "Template file not found — using built-in fallback."

---

## Step 1 — Get the Content

**If a URL is provided:**
- Fetch full content using `web_fetch`
- Extract conversation text, strip UI chrome, navigation, and buttons

**If raw markdown is pasted:**
- Use the pasted content directly

---

## Step 2 — Analyze the Content

Extract these fields before writing anything:

| Field | How to derive it |
|---|---|
| `title` | The central topic — concise, title-case, Googleable |
| `type` | `blog` or `doc` — drives template choice from Step 0 |
| `tags` | 3–6 specific keywords (not generic) |
| `description` | One sentence — what this note teaches |
| `keywords` | Same as tags + 1–2 more specific terms |
| `slug` | Lowercase title, spaces → `-` |
| `draft` | `true` if exploratory/incomplete, `false` if resolved |

---

## Step 3 — Generate the Foam Note

Use the template loaded in Step 0 (live or fallback).

Replace all Foam snippet variables with real derived values:
- `${FOAM_TITLE}` → derived title
- `${FOAM_DATE_YEAR}` → current year
- `${FOAM_DATE_MONTH}` → current month (2-digit)
- `${FOAM_DATE_DATE}` → current day (2-digit)

**Body sections to always include regardless of template:**

```
## Context
2–3 sentences: what problem or question sparked this conversation?

## Key Insights
3–5 distilled ideas — not transcript, signal only.

## Decisions / Conclusions
What was decided or resolved? If none: "Exploratory — no decisions made."

## Related Concepts
Foam [[wiki-links]] to connected notes.
- [[concept-one]]
- [[concept-two]]

## Source
URL or "Chat session — [date]"
```

---

## Step 4 — Output Instructions

After generating the note, tell the user:

```
📁 Save to:  blog/[slug].mdx  OR  docs/[slug].md
🏷️  Tags:    [list]
🔗 Links:    [[wiki-link-1]], [[wiki-link-2]]
📋 Template: [live from .foam/templates/xxx.md] OR [built-in fallback]

In VS Code:
  Cmd+Shift+P → "Foam: Create Note from Template"
  Select the matching template, then replace frontmatter with generated version.
```

---

## Fallback Templates (used when .foam/templates/ not found)

### Blog Fallback

```mdx
---
authors:
  - frank
tags:
  - [tag1]
  - [tag2]
  - [tag3]
description: [one sentence summary]
keywords:
  - [keyword1]
  - [keyword2]
image: https://i.imgur.com/mErPwqL.png
date: [YYYY-MM-DD]
draft: false
enableComments: true
---

# [Title]

> [Core insight in one sentence.]

<!--truncate-->
```

### Doc Fallback

```md
---
title: [Title]
tags:
  - [tag1]
  - [tag2]
description: [one sentence summary]
keywords:
  - [keyword1]
  - [keyword2]
date: [YYYY-MM-DD]
draft: false
---

# [Title]

> [Core insight in one sentence.]
```

---

## Metadata Rules

**Tags — specific, not generic:**
- ❌ `ai`, `coding`, `notes`
- ✅ `promptops`, `context-rot`, `agent-handoff`, `foam-pkm`

**Description — written as a lesson learned:**
- ❌ "A conversation about AI engineering"
- ✅ "Why managing the PromptOps layer matters more than model choice in 2026."

**Title — what would you Google to find this again?**
- ❌ "Chat about workflows"
- ✅ "PromptOps Mastery — The Three Areas of Agent Engineering"

**Wiki-links — connect to concepts, not just topics:**
- `context rot` discussed → `[[context-rot]]`
- `ADR` discussed → `[[architecture-decision-records]]`
- `multi-agent` discussed → `[[agent-handoff]]`

---

## Rules

- Never dump raw transcript — distill signal, not conversation
- Every note must have at least one `[[wiki-link]]` — orphan notes break the knowledge graph
- If content covers 2+ distinct topics → tell the user to split into separate notes
- Always report which template was used (live vs. fallback)
- If live template has extra frontmatter fields not in the fallback → keep them, fill them in