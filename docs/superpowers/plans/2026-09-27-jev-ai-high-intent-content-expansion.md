# Jev AI High-Intent Content Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add three source-grounded Jev AI pages that solve distinct developer tasks and strengthen internal navigation between existing guides.

**Architecture:** Keep the existing MDX content model and eight navigation categories. Add RAG source filtering and citation verification under community, and skill routing under agent. Add contextual Markdown links to existing pages without changing the renderer or URL system.

**Tech Stack:** Next.js static export, MDX, TypeScript content loader, official TypeSafe documentation links.

---

### Task 1: Add RAG source filtering guide

**Files:**
- Create: `content/en/community/jev-ai-rag-source-filtering.mdx`

- [ ] Write a 1,700+ word article covering candidate passage preparation, relevance/conflict/injection checks, Jev versus retrieval/generation, review thresholds, failure cases, a Python-shaped workflow example, tables, FAQ, and official cookbook links.
- [ ] Validate metadata, headings, URLs, and absence of unsupported benchmark claims.

### Task 2: Add citation verification guide

**Files:**
- Create: `content/en/community/jev-ai-citation-verification.mdx`

- [ ] Write a 1,700+ word article covering claim-evidence matching, citation existence checks, partial support, contradiction handling, audit records, human review, a typed workflow example, tables, FAQ, and official cookbook links.
- [ ] Validate metadata, headings, URLs, and separation between model judgment and deterministic checks.

### Task 3: Add skill routing guide

**Files:**
- Create: `content/en/agent/jev-ai-skill-routing.mdx`

- [ ] Write a 1,700+ word article covering candidate skill catalogs, none-of-the-above behavior, tool execution boundaries, confidence/review policies, agent loops, a typed workflow example, tables, FAQ, and official cookbook links.
- [ ] Validate metadata, headings, URLs, and no claims that Jev itself executes tools.

### Task 4: Add contextual internal links

**Files:**
- Modify: `content/en/guide/jev-ai-beginner-guide.mdx`
- Modify: `content/en/api/jev-ai-api-reference.mdx`
- Modify: `content/en/community/jev-ai-geo.mdx`
- Modify: `content/en/agent/jev-ai-agent.mdx`
- Modify: `content/en/community/jev-ai-use-cases.mdx`

- [ ] Add 3-5 natural links per article to relevant existing or new pages.
- [ ] Keep links in explanatory paragraphs or next-step sections, not keyword-only link lists.
- [ ] Confirm every internal href maps to an existing generated route.

### Task 5: Validate and publish

**Files:**
- No additional files.

- [ ] Run MDX metadata and internal-link checks.
- [ ] Run `npm run build`.
- [ ] Run `npm run lint`.
- [ ] Run `git diff --check`.
- [ ] Commit the content batch and push `main`.

