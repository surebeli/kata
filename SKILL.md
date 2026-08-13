---
name: kata
description: "Kata — a self-evolving knowledge system for AI-paired builders. CORE: self-closing wiki loop + auto-dreaming on Karpathy's LLM-Wiki principle. Phase 1 (current): AI-paired engineering — compile project business semantics so agents read project conventions before they write code. Phase 2 (designed): team spec authoring + dispute resolution. 18 skills (init / import / ingest / search / graph / tier / digest / query / lint / config / dream / watch / sync / spec / session-ingest / mcp-server / federate / skill-create). **v1.13 SHM complete (Phase 0+2+3+4)**. **v1.15 work-loop bridge**: `wiki-skill-create` generates project-local skills wrapping kata's query/ingest with the project's actual work pipeline (issue-fix / feature-build / bug-debug / custom patterns); closes consult-before / file-back-after as structural default rather than discipline."
version: 2.16.3
author: litianyi-007
license: MIT
---

# Kata (Standalone Prompt Version)

> **A self-evolving knowledge system for AI-paired builders.**
> Inherit a kata, adapt it to your project, then transcend the form.

**The layered model:**

- **Base** — Karpathy's LLM-Wiki principle: compiled once, kept current; humans
  curate, LLMs maintain; everything optional and modular.
- **Core** — A self-evolving knowledge system on the base: (1) self-closing
  ingest/synthesis loop where filed queries compound back into pages; (2)
  auto-dreaming that resurfaces frozen pages when their relevance returns.
- **Phase 1 (current)** — AI-paired engineering. Use the core wiki to compile
  business semantics (thresholds, lifecycle invariants, domain conventions) so
  agents read project conventions before they write code.
- **Phase 2 (designed, not yet implemented)** — Team spec authoring + dispute
  resolution as a closed-loop wiki workflow.
- **Phase 3+** — Open. The core extends as we learn what compounds.

**The mastery curve:** accept (run the starter kata as-is) → adapt (customize
schema + skills for your project) → transcend (the form fades; only the work
remains).

The wiki underneath is **compiled once and kept current** (not RAG — synthesis
is baked into pages, cross-references are written down). Cross-references are
there. Contradictions have been flagged. Synthesis reflects everything ingested.

> Obsidian is the IDE. The LLM is the programmer. The wiki is the codebase.

**Division of labor:** The human curates sources, drops them in `raw/`, asks good
questions, and edits `SCHEMA.md` when conventions need to evolve. The human
**never (or rarely) writes wiki pages themselves**. The LLM does everything else:
reading, summarizing, cross-referencing, filing, maintaining consistency. This is
the whole point — humans abandon wikis because the maintenance burden grows faster
than the value, but LLMs don't get bored.

---

## SCHEMA.md is authoritative

Every convention — page types, frontmatter fields, tag taxonomy, page creation
policy, cross-reference policy, page size limits, log rotation, **custom
frontmatter dimensions**, and **memory-tier thresholds** — lives in `SCHEMA.md`.
That file is **user-editable and co-evolves** with the wiki. `wiki-init` writes
a starter based on the user's domain; `wiki-lint` proposes updates over time.
This skill set **reads and enforces** SCHEMA.md rather than hardcoding opinions.

This matters because Karpathy's original is intentionally abstract: _"Everything
mentioned above is optional and modular — pick what's useful, ignore what isn't."_
A reading-a-book wiki and a research wiki need different page types and different
policies. SCHEMA.md is where that per-domain customization lives.

---

## Custom frontmatter dimensions

Beyond standard fields (title, created, updated, type, tags, sources), SCHEMA.md
can declare **custom dimensions** — extra frontmatter fields specific to the domain.
A software project wiki might declare `version:` (string, required, prompted on
every ingest). A research wiki might declare `venue:` or `citation_count:`.

Each dimension has: `name`, `type` (string/date/number/enum/list), `description`
(prompt text), `required`, `default`, `refresh_on` (`[ingest, import, digest,
manual]`), and optional `applies_to` (page types). `wiki-init` sets them up
interactively; `wiki-ingest` and `wiki-import` prompt per `refresh_on`;
`wiki-digest` surfaces stale values; `wiki-lint` validates completeness.

---

## Memory tiers (active / archived / frozen)

SCHEMA.md `memory_tiers:` controls three-tier aging:
- **active** (default < 365 days) — the hot surface; all query skills default here
- **archived** (default 365–730 days) — accessible via `--tier=archived|all`
- **frozen** (default > 730 days) — cold storage; future auto-dreaming planned

Tiers are **computed on-the-fly** from a driving date field (`published_at` with
`ingested_at` fallback) — never stored as frontmatter, so threshold adjustments
are instant. A wiki page's tier = most-recent-tier of its cited sources. Manual
`tier_override:` frontmatter pins are respected. Use `wiki-tier` to view/adjust.

---

## External fallback plugins

`{wiki_path}/.wiki-plugins.yaml` registers CLI tools that `wiki-query` calls when
local search returns insufficient results. Each plugin declares an `argv:` list
(per-token, no shell — see `PLUGINS.md` for the v1.4 spec), a trigger condition
(`on_empty|on_low_confidence|on_request`), and safety settings.

**Flow:** wiki-query local miss → plugin command → stdout → `raw/external/` →
wiki-ingest → wiki pages → future queries hit local first. The external output
becomes a raw source and enters the full ingest pipeline.

Default is `auto_run: false` — the agent shows the command and waits for user
confirmation. See `PLUGINS.md` (or the `wiki-query` skill) for the full spec.

---

## Quick Start

1. Run `wiki-init` — it asks about your domain and proposes categories that fit
2. `git init` in the wiki path (suggested automatically at the end of init)
3. Drop a source in `raw/articles/` and run `wiki-ingest`
4. Run `wiki-digest` to see your compiled knowledge grow
5. Ask questions with `wiki-query`; answers file back and compound

---

<!-- BEGIN AUTOGENERATED skill-table -->

<!-- Generated by scripts/build_skill_md.py — do not edit manually. -->
<!-- Source: plugin/skills/*/SKILL.md frontmatter. -->

| Skill | Argument hint | Description |
|-------|---------------|-------------|
| `wiki-config` | `[--show] [--get <path>] [--set <path> <value>] [--explain <path>] [--validate]` | Unified read/write for SCHEMA.md config — show all settings in one place, get/set scalar values by… |
| `wiki-digest` | `[--since=7d] [--focus=<topic>] [--format=brief\|full] [--tier=active\|all\|archived\|frozen]` | Generate a digest of the wiki: recent activity summary, key themes by cluster, tier distribution (a… |
| `wiki-dream` | `[--since YYYY-MM-DD] [--strategy co-occurrence] [--apply --pages 1,2,3] [--explain <page>] [--out <file>]` | Auto-dreaming: re-evaluate frozen and archived pages against recent activity, surface candidates wh… |
| `wiki-federate` | `search <query> [--wiki=<path>] [--limit=10] [--peers=name1,name2] [--no-federate] \| peers [--wiki=<path>] \| resolve <kata://uri> [--wiki=<path>]` | Cross-wiki federation — query peer kata wikis via MCP and merge results with provenance. v1.12 Phas… |
| `wiki-graph` | `[--query=<expr>] [--neighbors=<page> --depth=N] [--shortest-path=<a>,<b>] [--hubs] [--orphans] [--cluster=<tag>] [--limit=20] [--format=text\|json\|mermaid] [--tier=active\|all\|archived\|frozen]` | Query the wiki as a graph without maintaining a graph DB. Structured frontmatter queries, neighbor… |
| `wiki-import` | `<source-path> [--format=folder\|obsidian\|notion\|confluence\|markdown] [--map=<mapping-file>] [--dry-run] [--resume] [--priority=recency\|links\|manual] [--set=key=value,...] [--per-file-prompt]` | Import an existing document system (folder tree, Obsidian vault, Notion/Confluence export, etc.) in… |
| `wiki-ingest` | `<url\|file\|text> [--batch] [--no-discuss] [--no-images] [--no-spec-preflight] [--set=key=value,...] [--page-type=<type>] [--proposed-path=<dest-path>] [--evidence-anchors=<comma-separated>]` | Ingest a source into the wiki: save raw content and referenced images, prompt the user for any cust… |
| `wiki-init` | `[--path=~/wiki] [--domain='AI research'] [--categories='a,b,c'] [--non-interactive] [--set-tags='a,b,c'] [--set-active-days=N] [--set-archived-days=N] [--set-driving-field=published_at\|ingested_at] [--set-dimension='name:type:required:refresh_on'] [--enable-dreaming] [--enable-sync] [--refresh-id [--force]]` | Interactive bootstrap for a new LLM wiki: ask about domain, propose categories that fit, write a cu… |
| `wiki-lint` | `[--fix] [--report-only] [--check=orphans\|links\|frontmatter\|stale\|index\|tags\|size\|gaps\|schema\|tiers\|dimensions]` | Health-check the wiki: structural checks (orphans, broken links, frontmatter, stale content, tier c… |
| `wiki-mcp-server` | `[--wiki=<path>] [--transport=stdio]` | Run a kata wiki as a Model Context Protocol (MCP) server over stdio. Any MCP-aware agent (Claude Co… |
| `wiki-query` | `<question> [--file] [--format=markdown\|table\|slides\|chart\|canvas] [--tier=active\|all\|archived\|frozen] [--external] [--no-external] [--auto-external]` | Answer a question using the wiki's compiled knowledge. Searches relevant pages, synthesizes with ci… |
| `wiki-search` | `<query> [--tag=<tag>] [--type=entity\|concept\|comparison\|query] [--limit=10] [--tier=active\|all\|archived\|frozen]` | Search the wiki by keyword, tag, topic, or type. Returns ranked results with page summaries and mat… |
| `wiki-session-ingest` | `[--session-id <id>] [--session-file <path>] [--cli <name>] [--max-tool-output-lines N] [--full] [--auto-trigger]` | Ingest the active AI CLI session into the wiki: detect which CLI you're in (Claude Code / Codex CLI… |
| `wiki-skill-create` | `[--pattern <issue-fix\|feature-build\|bug-debug\|custom>] [--supplement-action <source-search\|web-search\|doc-lookup\|custom>] [--name <skill-name>] [--target <claude-code\|codex\|wiki>] [--no-ingest-after]` | Generate a project-local skill that bridges kata's documentation loop (search/query/ingest) with th… |
| `wiki-spec` | `preflight --new-spec <path> [--wiki=<path>] [--limit=10] [--include-archived] [--enforce] [--enforce-threshold=<float>] [--enforce-mode=strict\|confirm]` | Spec history management. Before authoring a new spec (PRD / design / RFC / ADR / task-spec / decisi… |
| `wiki-sync` | `[--auto] [--dry-run]` | Multi-machine git sync for the wiki: pull, merge with custom drivers (log.md union+sort), push. Loc… |
| `wiki-tier` | `[--show] [--set-active=Nd] [--set-archived=Nd] [--set-field=published_at\|ingested_at] [--preview] [--pin=<page>:<tier>] [--unpin=<page>] [--list=<tier>] [--disable] [--enable]` | Inspect and manage the memory-tier system: view the active/archived/frozen distribution, preview a… |
| `wiki-watch` | `[--start [--poll N --debounce N]] [--stop] [--status] [--drain [--pages 1,2,3]] [--remove <id>]` | Watch raw/{articles,papers,transcripts,external}/ for new files, queue them, and let the user drain… |

<!-- END AUTOGENERATED skill-table -->

## Skills

### wiki-init (interactive)
**Trigger:** "create a wiki", "start my knowledge base", "initialize a wiki for {domain}"

**Do not hardcode categories.** Ask the user about their domain, propose a
category set that fits, let them edit.

1. Resolve path in this order: `--path` / `--wiki` argument →
   `WIKI_PATH` env → ancestor wiki root → `LLM_WIKI_PROJECT` under
   `LLM_WIKI_HOME` → nearest project binding file `.llm-wiki.yaml` /
   `.kata.yaml` (**single-path cache** — one wiki per file, innermost
   wins) → `~/.llm-wiki/registry.yaml` (the index for multi-wiki
   machines) → git root name as `~/.llm-wiki/{repo}` → legacy
   `~/.kata/config.yaml` → `~/.llm-wiki/common`.
2. Ask for domain (specific — "transformer ML research", "LoTR trilogy", etc.)
3. **Propose categories matching the domain**:
   - Research → `entities/`, `concepts/`, `comparisons/`, `queries/`
   - Book → `characters/`, `places/`, `events/`, `themes/`, `timeline/`, `chapters/`
   - Personal → `journal/`, `topics/`, `patterns/`, `queries/`
   - Business → `people/`, `projects/`, `customers/`, `decisions/`, `meetings/`
   - Competitive → `competitors/`, `features/`, `market/`, `comparisons/`
4. Walk through conventions (offer defaults, accept edits):
   - Frontmatter fields (default: title/created/updated/type/tags/sources)
   - Tag taxonomy (propose 10–20 domain-specific tags)
   - Page creation policy (default: "central to source OR mentioned in 2+ sources")
   - Cross-reference policy (default: "link wherever genuine; no minimum")
   - Page size limit (default: no limit)
   - Log rotation threshold (default: no rotation)
5. Create directory structure + `raw/articles/`, `raw/papers/`, `raw/transcripts/`, `raw/external/`, `raw/imported/`, `raw/assets/`
6. Write `SCHEMA.md` with everything chosen above — mark it "user-editable"
7. Write sectioned `index.md` (one section per category)
8. Write `log.md` with init entry
9. **Suggest `git init`** — the wiki is a git repo, version history for free
10. Report and suggest first ingest

---

### wiki-ingest (with image handling)
**Trigger:** "ingest this", "add this source", "read this and update the wiki"

**Arguments:** `<url|file|text>`, `--batch`, `--no-discuss`, `--no-images`

1. **Orient**: read SCHEMA.md, index.md, recent log.md
2. **Capture raw source**:
   - Save text to `raw/articles/` or `raw/papers/` — never modify raw files
   - **Download referenced images** to `raw/assets/{source-stem}-{name}` and
     rewrite the saved raw source to use local paths (URLs rot; local copies persist)
3. **Process order for multimodal sources** — read text first (chunking if long),
   identify informative images (diagrams, charts, screenshots — skip decorative),
   **then view those specific images separately** using image tools. LLMs can't
   consume markdown + inline images in one pass.
4. **Discuss takeaways** with user (skip if `--no-discuss`) — surface 3–5 insights
   and ask what to emphasize
5. **Check existing pages** — search index.md and wiki files for every entity/concept
6. **Write/update pages per SCHEMA.md policy**:
   - Only create a page if SCHEMA.md's creation policy is met
   - Use the frontmatter fields SCHEMA.md requires
   - Only use tags from SCHEMA.md's taxonomy — if you want a new one, **pause and
     propose adding it to SCHEMA.md** rather than drifting
   - Page type must match an existing category; new kinds → propose schema update
7. **Cross-reference both ways** — a page that exists but is never linked to is invisible
8. **Update index.md and log.md**: `## [YYYY-MM-DD] ingest | Source Title`
9. **Report** — list every file, note any schema proposals awaiting approval

A single ingest usually touches **10–15 pages**. That's the compounding effect.

---

### wiki-search ⭐ KEY SKILL
**Trigger:** "find pages about X", "search for Y", "what do we have on Z"

Three-pass scan. No orientation needed — runs cold.

**Arguments:** `<query>`, `--tag=<tag>`, `--type=<category>`, `--limit=10`

1. Parse query, tag/type filters
2. **Pass 1**: scan `index.md` (Karpathy: "reads the index first to find relevant pages")
3. **Pass 2**: scan page frontmatter for tag/title matches
4. **Pass 3** (if <3 results): full-text search across page bodies (exclude `raw/`)
5. Rank: title match > hub centrality > content frequency > recency
6. Return with excerpt, tags, related pages

**Scaling up:**
- < 100 pages → built-in 3-pass scan
- 100–500 pages → built-in scan + keep index.md current via `wiki-lint`
- 500–2000 pages → install [`qmd`](https://github.com/tobi/qmd) (hybrid BM25/vector
  with LLM re-rank); `wiki-search` auto-shells-out when `qmd` is in PATH
- 2000+ pages → `qmd` in MCP server mode; agent calls directly, bypassing built-in scan

Karpathy: _"You could also build something simpler yourself — the LLM can help you
vibe-code a naive search script as the need arises."_

---

### wiki-graph (structured graph queries)
**Trigger:** "neighbors of X", "shortest path between A and B", "which pages are hubs", "orphans", "Dataview-style filter"

**Arguments:** `[--query=<expr>]`, `[--neighbors=<page> --depth=N]`, `[--shortest-path=<a>,<b>]`, `[--hubs]`, `[--orphans]`, `[--cluster=<tag>]`, `[--limit=20]`, `[--format=text|json|mermaid]`

`wiki-search` handles **ranked text relevance**. `wiki-graph` handles **structural
queries over frontmatter and the [[wikilink]] graph** — with no persistent store.
Every call scans the markdown files fresh, builds an in-memory graph, runs the
query, and exits. The filesystem remains the only source of truth.

Modes:
- **`--query`** — Dataview-style frontmatter filter. Fields, comparisons on
  dates/numbers, `AND`/`OR`/`NOT`, parentheses.
  Example: `--query "type: entity AND tags contains transformer AND updated > 2025-01"`
- **`--neighbors <page>`** — BFS over `[[wikilinks]]` up to `--depth` (cap 4).
  Best way to see everything adjacent to a topic.
- **`--shortest-path <a>,<b>`** — surface **bridge concepts** between two
  entities. Often the highest-signal mode — finds connections the user didn't
  realize were there.
- **`--hubs`** — nodes ranked by `|in_edges| + 0.5·|out_edges|`. Inbound > outbound.
- **`--orphans`** — isolated nodes (no links at all) vs. leaves (inbound only).
  True orphans are usually ingest bugs; leaves are often intentional stubs.
- **`--cluster=<tag>`** — members, anchor, intra- vs. external edges, density.
  Answers _"is this tag a coherent topic or just a shelf?"_

Output formats: `text` (default), `json` (pipe-friendly), `mermaid` (paste
into Obsidian or a GitHub README — great for `--neighbors`, `--shortest-path`,
`--cluster`).

**Why no persistent graph:** a second data store drifts silently out of sync
the moment the agent updates a page and forgets to update the graph. Files-as-
truth is Karpathy's core discipline. Scanning several hundred pages takes
milliseconds — cheaper than keeping an index coherent.

---

### wiki-tier (memory-tier management)
**Trigger:** "show tier distribution", "push active window to 2 years", "pin this page as active", "which pages just aged out"

**Arguments:** `[--show]`, `[--set-active=Nd]`, `[--set-archived=Nd]`,
`[--set-field=published_at|ingested_at]`, `[--preview]`,
`[--pin=<page>:<tier>]`, `[--unpin=<page>]`, `[--list=<tier>]`,
`[--disable]`, `[--enable]`

Manages the three-tier aging system configured in SCHEMA.md `memory_tiers:`.

- **`--show`** (default) — print config + distribution table + recently aged-out
  pages + pinned overrides
- **`--set-active=Nd` / `--set-archived=Nd`** — stage a threshold change, show
  the delta ("31 pages move archived→active"), ask before writing SCHEMA.md
- **`--preview`** — dry-run a threshold change without writing
- **`--pin=<page>:<tier>` / `--unpin=<page>`** — write or clear `tier_override:`
  frontmatter on a specific page (for canonical references that shouldn't age out)
- **`--list=<tier>`** — list every page in a given tier
- **`--disable` / `--enable`** — toggle the tier system in SCHEMA.md

Tier changes are **safe** — they re-interpret existing dates, not mutate content.
Auto-dreaming for frozen content is planned for v2 but not implemented yet.

---

### wiki-digest ⭐ KEY SKILL
**Trigger:** "what's in the wiki?", "summarize what we know", "give me an overview"

**Arguments:** `--since=7d`, `--focus=<topic>`, `--format=brief|full`

1. Orient (SCHEMA.md + index.md + log.md)
2. **Activity** (from log.md): parse entries in time window, count by action
3. **Inventory** (from index.md): pages by type, most-linked hubs, orphans
4. **Theme clustering**: group by tags, find anchor pages, assess depth
5. **Coverage gaps**: missing synthesis pages, uncompared entities, unfiled queries
6. **Cross-cutting synthesis**: entities spanning clusters, latent contradictions
7. **Suggested next actions** with specific skill invocations

---

### wiki-query (filed answers compound)
**Trigger:** any question about the wiki's domain

**Arguments:** `<question>`, `--file`, `--format=markdown|table|slides|chart|canvas`

**Like ingestion, substantive query results compound back into the wiki.** When an
answer is worth keeping, it's filed as a wiki page and joins the knowledge base
just like sources do.

1. Orient; classify question (factual / comparative / synthesis / gap)
2. Find pages via `wiki-search`
3. Read relevant pages (prioritize: comparisons > concepts > entities > queries)
4. Synthesize with `[[wikilink]]` citations; be explicit about gaps; present
   contradictions honestly
5. Apply format:
   - **markdown** — prose + headers (default)
   - **table** — comparison table, rows = options, columns = dimensions
   - **slides** — Marp-compatible deck (`marp: true` frontmatter, `---` slide breaks)
   - **chart** — matplotlib via code execution → save PNG under `queries/`
   - **canvas** — Obsidian `.canvas` JSON (nodes = pages, edges = connections)
6. **Decide whether to file back** — file to `queries/{name}.md` if:
   - 4+ pages used (synthesis is valuable)
   - It's a comparison that didn't exist
   - It reveals an emergent insight
   - `--file` flag was passed
7. Update `log.md`: `## [YYYY-MM-DD] query | Question`

---

### wiki-lint (structure + content + evolution)
**Trigger:** "lint", "audit", "health-check", "clean up"

**Two layers** of checks. The content layer is where the LLM earns its keep.

**Structural checks** (the "well-formed?" layer):

| Severity | Check | Description |
|----------|-------|-------------|
| HIGH | Broken wikilinks | `[[links]]` pointing to non-existent pages |
| HIGH | Index gaps | Pages on filesystem not in index.md |
| MEDIUM | Orphan pages | Pages with no inbound links |
| MEDIUM | Contradictions | Unresolved `contradictions:` frontmatter flags |
| MEDIUM | Frontmatter | Missing fields per SCHEMA.md required list |
| LOW | Tag drift | Tags not in SCHEMA.md taxonomy |
| LOW | Stale content | `updated` older than newer sources mentioning same entities |
| LOW | Oversized pages | Over SCHEMA.md limit (default: no limit) |
| AUTO | Log rotation | Per SCHEMA.md threshold (default: no rotation) |

**Content checks** (the LLM layer — this is what Karpathy emphasized):

- **Content gaps**: entities mentioned in 3+ pages with no entity page; open
  questions in page text never filed as queries; 5+ co-occurring entities with
  no comparison page; clusters of 5+ tagged pages with no synthesis concept page
- **Web search suggestions**: for each gap, propose a specific web query that
  would fill it. Offer to run it and stage results for `wiki-ingest`.
- **Taxonomy evolution**: propose SCHEMA.md updates as diffs — tags to add,
  tags to retire, new categories, threshold adjustments. Apply with `--fix`
  or on user confirmation.

`--fix` applies safe automated fixes (index gaps, log rotation, approved
schema updates). `--report-only` is report-only (default).

---

### wiki-import (bulk migration)
**Trigger:** "import my existing docs", "migrate my vault", "bring in my whole folder"

**Arguments:** `<source-path>`, `--format=folder|obsidian|notion|confluence`,
`--map=<file>`, `--dry-run`, `--resume`, `--priority=recency|links|manual`

Five-phase import: **Discovery** → **Mapping** → **Deduplication** → **Processing
in waves of 20** → **Navigation update**. Checkpoint to
`.wiki-import-checkpoint.json` every 20 files; resume on interruption. Handles
Obsidian vaults, Notion/Confluence exports, or plain folders. For large imports
(hundreds of files).

See the full plugin skill for all details.

---

### wiki-watch (raw/ auto-ingest watcher)
**Trigger:** "watch raw/", "auto-detect new files", "what's pending to ingest", "drain the queue"

**Arguments:** `[--start [--poll N --debounce N]]`, `[--stop]`, `[--status]`,
`[--drain [--pages 1,2,3]]`, `[--remove <id>]`

Closes the "I dropped a file in `raw/articles/` and forgot to ingest it" gap.
A polling daemon (default 5 s) detects new files in
`raw/{articles,papers,transcripts,external}/`, debounces against in-progress
writes (default 5 s), and writes them to `.wiki-ingest-queue.json` with a
`pending` status. **The watcher never auto-runs `wiki-ingest`** — drain is
always explicit, so a misconfigured watcher cannot silently mutate wiki pages.

- **`--start`** — spawn the daemon for the resolved wiki. PID and log are
  per-project (`~/.kata/watcher-{slug}.pid`, …`.log`), so multiple
  project wikis (`~/.llm-wiki/necall`, `~/.llm-wiki/rtc`, …) can each run
  their own watcher concurrently.
- **`--status`** (default when no flag passed) — daemon liveness + queue
  summary (`pending / processed / failed / removed`). Works whether or not
  the daemon is running.
- **`--drain`** — for each `pending` entry in detection order: invoke
  `wiki-ingest <path>`, mark `processed` on success or `failed` on error.
  After the loop, append a single `## [date] watch | drained N files` log
  entry. `--drain --pages 1,3` processes only the listed indices.
- **`--remove <id|index>`** — drop an entry from the queue without ingesting.
  Use for WIP files you don't want in the wiki yet.
- **`--stop`** — clean SIGTERM to the daemon (TerminateProcess on Windows).

**When NOT to use:** for one-off ingestion of a known file → just run
`wiki-ingest <path>`. The watcher is for the steady-state drip workflow.
For bulk migration of an existing folder use `wiki-import`.

---

### wiki-dream (auto-dreaming)
**Trigger:** "what frozen pages just got relevant again", "dream", "re-promote old pages"

**Arguments:** `[--since YYYY-MM-DD]`, `[--strategy co-occurrence]`,
`[--apply --pages 1,2,3]`, `[--explain <page>]`, `[--out <file>]`

The only kata feature that runs without you. While you sleep, the dreamer
re-evaluates which `frozen` and `archived` pages have become relevant again
based on this period's ingests. Reads only the wiki filesystem (`log.md` +
page frontmatter dates `ingested_at` / `updated`) — **never reads chat
sessions, file mtimes, or any external state**. Frontmatter dates are
checked into git, so `git clone` reproduces dreamer behavior on any
machine; using mtimes would not (mtimes reset on checkout).

**How it scores** (v1.6 strategy: `co-occurrence`):
- **Entity overlap** (weight 0.5 default) — old page shares title / link
  targets with new ingests this period
- **Tag resurgence** (weight 0.2) — tag appears ≥ `min_count` times in fresh
  pages after being dormant for `dormancy_window_days`
- **Citation hit** (weight 0.4) — a fresh page directly `[[wikilinks]]` to
  the old page

Pages above `confidence_threshold` (default 0.6) become **candidates** —
surfaced for review, never auto-promoted. `--apply --pages 1,2,3` writes
`tier_override: active` plus a reason and timestamp to selected candidates.

- **Default mode** — emit candidate JSON + write a dated file at
  `dreaming/{YYYY-MM-DD}.md` for human review next morning. Caps at
  `max_repromote_per_run` (default 10).
- **`--explain <page>`** — score breakdown for one specific page (entity /
  tag / citation components). Useful for "why didn't X get promoted?"
- **`--apply`** — promotes named candidates and advances the `dream |`
  watermark in `log.md`.

**Schedule** weekly via Claude Code: `claude /schedule "0 23 * * 0"
"/kata:wiki-dream"`. Tune via `wiki-config --set dreaming.<key> <value>`.

---

### wiki-config (unified SCHEMA.md read/write)
**Trigger:** "show all config", "set dreaming threshold", "what does X mean", "validate SCHEMA.md"

**Arguments:** `[--show]`, `[--get <path>]`, `[--set <path> <value>]`,
`[--explain <path>]`, `[--validate]`

Generic path-based interface to SCHEMA.md tunables. Use this when there's no
domain-specific shortcut (e.g. `wiki-tier --set-active=540d` is better UX
for tier thresholds; `wiki-config` is for the long tail like dreaming
weights and resurgence params).

- **`--show`** — all config blocks at a glance (memory_tiers, dreaming,
  custom_dimensions, tag_taxonomy_count, categories)
- **`--get memory_tiers.active_days`** — read one dotted-path value
- **`--set dreaming.confidence_threshold 0.55`** — surgical line replacement
  that preserves comments, blank lines, and ordering. Validates after every
  write; **reverts SCHEMA.md if validation fails**, surfaces the validation
  errors verbatim.
- **`--explain dreaming.weights.entity`** — read the docstring for any
  documented key (kept in sync with TRD additions).
- **`--validate`** — run the full schema_validate pipeline (structural +
  cross-field rules).

**v1.6 limitations** (deliberate trade for safety):
- Edits existing scalars only — cannot add new keys or new YAML blocks.
- No list-index editing (`custom_dimensions[0].required` is unreachable).
- No multi-key transactions — each `--set` is independent.

For introducing a `dreaming:` block to a wiki initialized before v1.6, edit
SCHEMA.md by hand or re-run `wiki-init` with the dreaming flag.

---

### wiki-sync (multi-machine git sync — v1.8+)
**Trigger:** "sync the wiki", "pull from origin", "push my changes", "are my machines in sync"

**Arguments:** `[--auto]`, `[--dry-run]`

Pull-merge-push your wiki across machines. Custom merge driver
(`merge_log.py`) auto-merges `log.md` as a union+sort, deduplicating by
canonical hash and preserving body data on same-triple-different-body
divergence. Per-machine sync reports go to
`~/.kata/sync-reports/{slug}/` — **never inside the wiki repo**, so
they don't self-conflict on the next sync.

- **default (interactive)** — acquire local sync lock, stash dirty
  tree (with SHA capture), fetch, classify ancestry, merge with
  driver, push (bounded retry 3×). Cleanup in three-layer
  try/finally so lock always releases.
- **`--auto`** (cron mode) — any non-clean outcome exits non-zero so a
  chained `&& wiki-dream` doesn't run. Recommended cron line:
  `0 23 * * 0 wiki-sync --auto && wiki-dream`
- **`--dry-run`** — read-only preview; forks BEFORE side effects (no
  lock, stash, driver registration, or log mutation). Only `git fetch`
  runs (writes only to `.git/refs/remotes/`).

**Hard stops** (exit 1):
- Force-push detected — old origin SHA isn't an ancestor of new origin SHA
- Unrelated histories — first fetch and no merge-base with origin
- Identity mismatch — local `wiki_id` ≠ remote `wiki_id` from
  `git show origin/main:SCHEMA.md`
- Active wiki-import — `.wiki-import-lock` fresh OR
  `.wiki-import-checkpoint.json` present (`wiki-import` was interrupted)
- Local sync lock held by a live PID — same-machine reentrancy guard
- Merge / rebase / cherry-pick already in progress

**Conflicts** that the driver can't auto-resolve land as standard
unmerged paths (`<<<<<<<` / `>>>>>>>`); the conflict report includes
the recovery commands using stash SHA (not `stash@{0}` which can drift).

**v1.8 MVP limitations:**
- Only `merge_log.py` driver registered. `merge_index.py` is v1.8-full
  per PRD §13 phasing — until then `index.md` uses git's default 3-way.
- Push-race retry: bounded at 4 total attempts (1s/2s/4s backoff). Each
  retry re-fetches, re-classifies, and re-merges with the driver if the
  ancestry is still divergent. Out-of-retries → `race-exhausted`.

---

### wiki-spec (spec history management — v1.13+, Phase 0)
**Trigger:** "before authoring a new spec", "what prior specs relate to X", "any decisions overlapping this PRD draft"

**Arguments:** `preflight --new-spec <path>`, `[--wiki=<path>]`, `[--limit=N]`, `[--include-archived]`

Spec-aware authoring helper. SDD / superpowers-style flows generate many
specs over time; new specs frequently overlap, refine, or override older
ones, but most tools have no mechanism to make the new-spec author "answer
for" the older specs. `wiki-spec preflight` scans the wiki for related prior
specs (by tag overlap, title overlap, explicit wikilinks, hub centrality)
and surfaces them so the author can declare relationships before ingest.

**Phase 0 scope** (current):
- Preflight scan over **kata-managed pages** with `frontmatter.type` in
  `spec_authoring.spec_types` (default includes `decisions`, `prd`,
  `design`, `rfc`, `adr`, `task-spec`)
- Advisory output (JSON) — the author / agent reads candidates and decides
  whether to declare relationships in `spec_relationships:` frontmatter
- **No enforcement, no auto-propagation, no external sources** yet

**Roadmap (subsequent phases):**
- Phase 1 — extend preflight to `.wiki-plugins.yaml` external sources
  (`treatment: raw|frozen|active`) so a kata adoption can scan a 6-month
  historical SDD corpus without bulk-importing it
- Phase 2 — enforce `spec_relationships:` declaration; ingest rejects on
  missing relationship for above-threshold candidates
- Phase 3 — auto-propagation: superseded specs get banner + tier flip +
  reverse-link; integrates with v1.6 dreamer as a reject signal
- Phase 4 — `wiki-graph --spec-history <topic>` coherence view

**Configuration in SCHEMA.md** (all fields optional; defaults are sensible):

```yaml
spec_authoring:
  enabled: true
  spec_types: [decisions, prd, design, rfc, adr, task-spec]
  preflight: auto
  relationship_kinds: [supersedes, refines, extends, parallel, contradicts]
  enforce_relationship_declaration: false   # Phase 2 toggle
```

Per-spec frontmatter convention (Phase 0 manual, Phase 2 enforced):

```yaml
spec_relationships:
  - kind: supersedes
    target: decisions/F015-old-spec.md
    note: "F015's scope absorbed; F015 should be archived"
  - kind: extends
    target: decisions/F011-merge-back.md
```

`target` accepts a path relative to the wiki root, `[[wikilink]]`, bare
stem, or `kata://<peer>/<path>` federation URI — **absolute paths and
`..` segments are rejected** (path-traversal guard, hardened v2.13.1).

See `plugin/skills/wiki-spec/SKILL.md` for the full per-phase contract and
`docs/PRD-v1.13-spec-history-management.md` (forthcoming) for design.

---

### wiki-session-ingest (capture conversation-born knowledge — v1.11+)
**Trigger:** "capture what we just figured out", "distill this session into the wiki", "what did I learn today that isn't written down"

**Arguments:** `--session-id <id>`, `--session-file <path>`, `--cli <name>`,
`--max-tool-output-lines N`, `--full`, `--auto-trigger`

The other ingest skills handle artifacts — URLs, files, pasted text. This
one handles **the conversation itself**. The reasoning trail from a long
debug / design session compounds the same way a source does, if someone
writes it down before it's forgotten.

**Standalone adaptation:** the plugin ships a JSONL adapter that parses
Claude Code / Codex CLI transcript files directly and tracks a persistent
state file for incremental re-dumps across repeated calls. None of that
exists standalone — no adapter, no state file. Standalone mode always
follows the plugin's own manual fallback path (its answer for CLIs
without an adapter): you, the agent, write the summary yourself.

1. **Orient** — read SCHEMA.md, index.md, recent log.md
2. **Write the raw dump yourself** — summarize the conversation under four
   headings: `User questions`, `Decisions`, `Outcomes`, `Detailed
   turn-by-turn` (concise — enough to extract knowledge points from, not a
   verbatim transcript). Save to `raw/sessions/{context}-{date}-{slug}.md`.
   Every standalone run is a fresh, full write — there's no state file to
   make it incremental
3. **Extract knowledge-point candidates** — scan the dump plus index.md for
   confidently-answered questions, approved/rejected design proposals,
   diagnosed bugs with root cause, executed runbook steps, schema
   decisions. Filter out housekeeping and unresolved threads. Reject a
   candidate unless it can point to at least two distinct parts of the
   conversation backing it (hallucination guard) — cite specifics
4. **Multi-select with the user** — present up to 8 ranked candidates, ask
   which to keep; selecting none is a valid, zero-write outcome
5. **Distill selected candidates** — run each through the `wiki-ingest`
   steps above (SCHEMA.md-conformant page type, cross-links, index.md /
   log.md updates)

**Not available standalone:** CLI auto-detection (environment-variable and
transcript-path probing), the JSONL parse-and-render pipeline, and
incremental re-dump tracking are all adapter-script machinery with no
manual equivalent worth approximating — every standalone run is treated as
one full, hand-authored dump instead.

See `plugin/skills/wiki-session-ingest/SKILL.md` for the full adapter and
incremental-state contract.

---

### wiki-mcp-server (MCP server — plugin-only, not available standalone)
**Trigger:** "expose this wiki over MCP", "let Cursor/Continue query my wiki", "run the wiki as an MCP server"

**Arguments:** `--wiki=<path>`, `--transport=stdio`

In the plugin, this runs the wiki as a stdio JSON-RPC MCP server so any
MCP-aware client (Claude Code, Cursor, Continue, or another kata acting as
a federation client) can call read-only tools against it directly:
`wiki-search`, `wiki-graph` (read subset), `wiki-spec-preflight` (advisory
candidates only). Write skills are never exposed across the MCP boundary.

**Not available in standalone form.** This skill's entire job is being a
long-lived process that a client spawns over stdio and holds a JSON-RPC
session with. A standalone protocol paste is static text living inside
someone else's context — it cannot host a subprocess, accept a client
handshake, or stay resident between calls. There is no manual degradation
that preserves this behavior: either the real process is running, or the
capability doesn't exist here.

If another agent needs to query this wiki and installing the real kata
plugin isn't an option, give that agent direct file-read access to the
wiki directory (or a copy) plus this same document — it can then run the
`wiki-search` / `wiki-graph` steps above directly against the files. Same
read-only outcome, no MCP transport involved.

See `plugin/skills/wiki-mcp-server/SKILL.md` for the protocol surface, the
safety contract, and how to actually run the server.

---

### wiki-federate (cross-wiki federation — degrades to manual peer reads standalone)
**Trigger:** "check if other wikis have something on this", "query the federated wikis", "resolve this kata:// citation"

**Arguments:** `search <query> [--wiki=<path>] [--limit=10]
[--peers=name1,name2] [--no-federate]`, `peers [--wiki=<path>]`,
`resolve <kata://uri> [--wiki=<path>]`

In the plugin, this fans a query out to peer kata wikis listed in
`{wiki_path}/.federation.yaml`, spawning each peer's `wiki-mcp-server` as
a subprocess, verifying the peer's `wiki_id` before trusting it, and
merging ranked results with `kata://<peer>/<path>` provenance.

**Not available live, standalone.** Fan-out depends on peer
`wiki-mcp-server` processes actually running (plugin-only, see above) and
a client script to spawn and query them — neither exists here.

**Manual analog, if you have it:** when you (the agent) have direct
file-read access to a second wiki's directory — not via MCP, just a folder
you can read — you can reproduce the spirit of federation by hand: read
the peer's SCHEMA.md and confirm its `wiki_id` matches what you expect
(same identity-check discipline as the live version), run the
`wiki-search` steps above against the peer's files instead of your own,
and cite anything you use as `kata://<peer-name>/<path relative to the
peer's wiki root>` so provenance survives without the live protocol.
Ranking and merging across wikis is then a judgment call, not an
automatic score.

Without either a running peer server or direct file access to one,
there's nothing to federate against — say so rather than guessing.

See `plugin/skills/wiki-federate/SKILL.md` for the peer-registry format,
identity-check contract, and failure-mode table the live version
implements.

---

### wiki-skill-create (work-loop bridge — v1.15)
**Trigger:** "wire kata into this project's workflow", "create a project-local skill", "generate a fix-loop / feature-loop / debug-loop skill"

**Arguments:** `[--pattern <issue-fix|feature-build|bug-debug|custom>]`, `[--supplement-action <source-search|web-search|doc-lookup|custom>]`, `[--name <kebab>]`, `[--target <claude-code|codex|wiki>]`, `[--no-ingest-after]`

Generates a **project-local skill** that wraps kata's documentation loop
(search / query / ingest) with the project's actual work pipeline (code
edit / test / build / human verify) into one closed loop. The generated
skill is checked into the project repo and becomes the default entry
point for that kind of work in that project — consult-before /
file-back-after becomes structural, not a discipline.

**MVP patterns (4):**
- `issue-fix` — concrete bugfix or fix request; canonical 7-step loop
- `feature-build` — feature with design phase; couples with `wiki-spec`
  Phase 0+2 preflight; files back both spec AND impl learnings
- `bug-debug` — systematic investigation; reproduces, searches kata by
  symptom AND mechanism, files back lesson with root cause dominant
- `custom` — escape hatch; user describes the middle phases, kata wraps
  with query / human-gate / file-back bookends

**Supplement-action catalog (v2.15.1):** each pattern's "verify against
prior art" phase is parameterized, not hardcoded to a code repo —
`--supplement-action source-search` (Grep/Glob/Read, default),
`web-search` (WebSearch + WebFetch, for research/materials wikis),
`doc-lookup` (local `docs/` + authoritative external doc sites), or
`custom` (`{{CUSTOM_SUPPLEMENT_*}}` placeholders for a user-described
action). Each snippet self-encodes the hit/miss escalation: a Step 2
kata-wiki hit means verification mode; a miss means primary-discovery
mode and makes the file-back in the final phase higher-value.
`discover` suggests one based on detected tech-stack signals; the
orchestrator's Phase 2.5 asks the user to confirm or override.

**Discovery (automatic before render):**
- Project root + git root + project name (from `package.json.name`,
  `Cargo.toml [package].name`, `go.mod module`, or pyproject.toml
  `[project].name`; falls back to git root dir name)
- Tech stack: nodejs / typescript / python / rust / go / gradle / maven
- Default test / build / lint commands (read from package.json scripts
  if present; sensible defaults per stack otherwise)
- Kata wiki binding (same `find_wiki_root()` resolution as other kata
  skills; placeholder if unbound)
- Existing kata-generated skills (detected via the sentinel comment)

**Verification (9 static checks after render):**
frontmatter parses; required fields; name `^[a-z][a-z0-9-]*$`; ≤ 1024
chars frontmatter; description starts with "Use when"; third-person
only; sentinel comment present; no unresolved `{{VAR}}`; argument-hint
when user-invocable.

**Placement:**
- `--target claude-code` (default) → `<project>/.claude/skills/<name>/SKILL.md`
- `--target codex` → `~/.codex/skills/<name>/SKILL.md`
- `--target wiki` → `<wiki_path>/skills/<name>/SKILL.md` (rare)
- Or any explicit path

**Sentinel** in every generated SKILL.md:
`<!-- kata:generated-skill pattern=<p> kata_version=<v> generated_at=<iso> -->`

See `plugin/skills/wiki-skill-create/SKILL.md` for the orchestrator
contract, `plugin/skills/wiki-skill-create/templates/` for the four
pattern templates, and `docs/PRD-v1.15-work-loop-bridge.md` for the
strategic framing.

---

## Architecture

```
{wiki_path}/
├── SCHEMA.md           # Conventions, tag taxonomy, policies (USER-EDITABLE)
├── index.md            # Sectioned content catalog with one-line summaries
├── log.md              # Append-only chronological action log
├── raw/                # IMMUTABLE — source material, never modified
│   ├── articles/
│   ├── papers/
│   ├── transcripts/
│   ├── external/
│   ├── imported/
│   └── assets/         # Downloaded images and attachments
└── {categories}/       # Category directories — defined by SCHEMA.md
                        # e.g. entities/, concepts/, comparisons/, queries/
                        # or:  characters/, themes/, plot/, timeline/
                        # or:  people/, projects/, decisions/, meetings/
```

Starter structure ≠ law. Categories match the domain.

---

## Working with Obsidian

The wiki is a drop-in Obsidian vault:

- **`[[wikilinks]]`** render as clickable
- **Graph view** — the best way to see the shape of the wiki. When the user asks
  "what does my wiki look like?" and they have Obsidian open, point them there.
  Otherwise use `wiki-digest` for a text equivalent.
- **Dataview plugin** — runs queries over YAML frontmatter. Add rich frontmatter
  (tags, dates, source counts) and Dataview can generate dynamic tables.
- **Obsidian Web Clipper** — browser extension, converts web articles to markdown
  directly into `raw/articles/`. Fastest way to get sources in.
- **Images** — set Obsidian's attachment folder to `raw/assets/`; reference as
  `![[image.png]]`
- **Marp plugin** — renders `--format=slides` output inside Obsidian

---

## Git integration

The wiki is a git repo by default. `wiki-init` suggests `git init` as the final
step. Every `wiki-ingest` and `wiki-query --file` produces clean, reviewable
diffs. Team wikis can use branches for proposed changes before merging. `log.md`
gives the timeline; `git log` gives the diffs behind it.

---

## Guards (always enforced)

- **Immutability**: `raw/` is read-only. Write corrections to wiki pages, not sources.
- **Orientation**: Read SCHEMA.md + index.md + recent log.md before any
  ingest/query/lint/digest. Skipping this causes duplicates and missed cross-references.
- **Scope**: Confirm before touching 10+ existing pages in one operation.
- **Schema**: Before adding a tag not in the taxonomy or creating a new page type,
  **propose a SCHEMA.md update** rather than silently drifting.

---

## Pitfalls

- Don't hardcode rules the plugin shouldn't own — all policies live in SCHEMA.md
- Don't create pages for passing mentions — follow SCHEMA.md's creation policy
- Don't force artificial cross-references to hit a link count — link wherever
  there's a genuine connection
- Don't silently overwrite contradictions — note both, flag in frontmatter
- Don't skip orientation — it's the main thing preventing duplicates
- Don't forget to handle images — they rot when left as remote URLs
- Don't treat `wiki-lint` as a pure formatter — it should suggest content gaps
  and schema evolution, not just structural fixes
