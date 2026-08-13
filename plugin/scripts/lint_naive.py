#!/usr/bin/env python3
"""Structural lint checks for kata — the part that's mechanical.

The wiki-lint skill calls this script for the deterministic checks
(broken links, orphans, missing frontmatter, tag drift, stale content,
index gaps, page size). Content gaps and SCHEMA.md evolution remain LLM
tasks — the script does NOT attempt them.

Usage:
    lint_naive.py --wiki <path> [--check links,orphans,...] [--severity HIGH]
    lint_naive.py --wiki <path> --check all

Output: JSON with findings grouped by check name and severity.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

from wiki_lib import (
    Page,
    build_graph,
    compute_tier,
    discover_pages,
    emit,
    extract_links,
    find_wiki_root,
    is_structural_page,
    load_schema,
)

ALL_CHECKS = ("links", "index", "orphans", "frontmatter", "tags", "stale",
              "size", "tiers", "dimensions")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wiki", default=None)
    p.add_argument("--check", default="all",
                   help="Comma list or 'all'. Choices: " + ",".join(ALL_CHECKS))
    p.add_argument("--severity", default=None,
                   choices=["HIGH", "MEDIUM", "LOW"])
    p.add_argument("--stale-days", type=int, default=180,
                   help="Pages with `updated` older than N days are 'stale'")
    p.add_argument("--max-page-bytes", type=int, default=None,
                   help="Override SCHEMA.md page-size limit")
    args = p.parse_args()

    root = find_wiki_root(args.wiki)
    if not root.exists():
        emit({"error": f"wiki root not found: {root}"})
        return 2

    if args.check == "all":
        checks = list(ALL_CHECKS)
    else:
        checks = [c.strip() for c in args.check.split(",") if c.strip()]

    schema = load_schema(root)
    pages = discover_pages(root)
    id_map, dangling = build_graph(pages)

    findings: list[dict] = []

    if "links" in checks:
        for src_path, broken in dangling.items():
            for target in broken:
                findings.append({
                    "check": "links", "severity": "HIGH",
                    "page": src_path,
                    "message": f"broken wikilink [[{target}]] — no page resolves",
                    "target": target,
                })

    if "index" in checks:
        findings.extend(_check_index(root, pages))

    if "orphans" in checks:
        # SCHEMA.md / index.md / log.md (and dreaming/*.md) are bookkeeping,
        # not content — wiki-init writes all three on every wiki unconditionally,
        # and nothing is ever supposed to [[wikilink]] *to* them, so they show
        # zero in/out edges on every single wiki and would otherwise be
        # reported as "orphans" 100% of the time. That's noise, not a finding.
        # graph_query.py's `--mode orphans` already carries this exact
        # exemption (see wiki_lib.is_structural_page() for the full
        # rationale) — reuse it here rather than hand-rolling a second
        # exclusion list that can independently drift out of sync.
        for p_obj in pages:
            if is_structural_page(p_obj.path):
                continue
            if not p_obj.in_links and not p_obj.out_links:
                findings.append({
                    "check": "orphans", "severity": "MEDIUM",
                    "page": p_obj.path,
                    "message": "true orphan: no inbound or outbound wikilinks",
                })

    if "frontmatter" in checks:
        # Same exemption as the orphans check above (see is_structural_page):
        # SCHEMA.md/index.md/log.md don't carry the content-page frontmatter
        # shape (title/type/tags/...) that SCHEMA.md's own frontmatter_fields
        # policy is written to describe, so holding them to it is a false
        # positive on every wiki, not a real gap.
        required = schema.get("frontmatter_fields") or []
        if isinstance(required, list) and required:
            for p_obj in pages:
                if is_structural_page(p_obj.path):
                    continue
                missing = [f for f in required if f not in p_obj.frontmatter]
                if missing:
                    findings.append({
                        "check": "frontmatter", "severity": "MEDIUM",
                        "page": p_obj.path,
                        "message": f"missing required field(s): {missing}",
                        "missing": missing,
                    })

    if "tags" in checks:
        taxonomy = set(schema.get("tag_taxonomy") or [])
        if taxonomy:
            for p_obj in pages:
                tags = p_obj.frontmatter.get("tags") or []
                if isinstance(tags, list):
                    drift = [t for t in tags
                             if str(t).lower() not in {x.lower() for x in taxonomy}]
                    if drift:
                        findings.append({
                            "check": "tags", "severity": "LOW",
                            "page": p_obj.path,
                            "message": f"tag(s) not in SCHEMA.md taxonomy: {drift}",
                            "drift": drift,
                        })

    if "stale" in checks:
        cutoff = date.today() - timedelta(days=args.stale_days)
        for p_obj in pages:
            updated = p_obj.frontmatter.get("updated")
            if isinstance(updated, str):
                try:
                    upd = date.fromisoformat(updated[:10])
                except ValueError:
                    continue
            elif isinstance(updated, date):
                upd = updated
            else:
                continue
            if upd < cutoff:
                findings.append({
                    "check": "stale", "severity": "LOW",
                    "page": p_obj.path,
                    "message": f"updated {(date.today() - upd).days} days ago "
                               f"(threshold {args.stale_days})",
                    "updated": str(upd),
                })

    if "size" in checks:
        limit = args.max_page_bytes
        if limit is None:
            sl = schema.get("page_size_limit")
            if isinstance(sl, int):
                limit = sl
        if limit:
            for p_obj in pages:
                size = (root / p_obj.path).stat().st_size
                if size > limit:
                    findings.append({
                        "check": "size", "severity": "LOW",
                        "page": p_obj.path,
                        "message": f"page size {size}B > limit {limit}B",
                        "size": size, "limit": limit,
                    })

    if "tiers" in checks:
        # Pin override applied to a non-existent / disabled tier system
        mt = schema.get("memory_tiers")
        if isinstance(mt, dict) and mt.get("enabled") is False:
            for p_obj in pages:
                if "tier_override" in p_obj.frontmatter:
                    findings.append({
                        "check": "tiers", "severity": "LOW",
                        "page": p_obj.path,
                        "message": "tier_override set but memory_tiers.enabled is false",
                    })

    if "dimensions" in checks:
        dims = schema.get("custom_dimensions") or []
        for p_obj in pages:
            page_type = p_obj.frontmatter.get("type")
            for d in dims:
                if not isinstance(d, dict) or not d.get("required"):
                    continue
                applies = d.get("applies_to")
                if applies and page_type not in applies:
                    continue
                if d["name"] not in p_obj.frontmatter:
                    findings.append({
                        "check": "dimensions", "severity": "MEDIUM",
                        "page": p_obj.path,
                        "message": f"required dimension {d['name']!r} missing",
                        "dimension": d["name"],
                    })

    if args.severity:
        findings = [f for f in findings if f["severity"] == args.severity]

    summary: dict = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    by_check: dict = {}
    for f in findings:
        summary[f["severity"]] = summary.get(f["severity"], 0) + 1
        by_check[f["check"]] = by_check.get(f["check"], 0) + 1

    emit({
        "wiki": str(root),
        "checks_run": checks,
        "page_count": len(pages),
        "findings_total": len(findings),
        "by_severity": summary,
        "by_check": by_check,
        "findings": findings,
    })
    return 0 if not findings else 1


def _check_index(root: Path, pages: list[Page]) -> list[dict]:
    """Index gap = page exists on disk but isn't mentioned in index.md."""
    idx = root / "index.md"
    if not idx.exists():
        return [{
            "check": "index", "severity": "HIGH", "page": "index.md",
            "message": "index.md does not exist",
        }]
    text = idx.read_text(encoding="utf-8").lower()
    findings = []
    for p in pages:
        # index.md trivially can't reference itself, and log.md's own
        # append-only entries aren't meant to be catalogued in index.md
        # either. This used to be a two-name inline check (index.md, log.md)
        # that — being separate from the orphans/frontmatter exemptions —
        # simply forgot the third scaffold file, SCHEMA.md, which then
        # false-positived as an "unindexed page" on every wiki. Now sourced
        # from the one shared definition (see is_structural_page) so the
        # three checks can't drift relative to each other again.
        if is_structural_page(p.path):
            continue
        stem = Path(p.path).stem.lower()
        title = (p.title or "").lower()
        if stem not in text and (not title or title not in text):
            findings.append({
                "check": "index", "severity": "MEDIUM",
                "page": p.path,
                "message": f"page not referenced in index.md (stem={stem!r})",
            })
    return findings


if __name__ == "__main__":
    sys.exit(main())
