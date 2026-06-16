#!/usr/bin/env python3
# Title: OrgContext Corpus Index Builder
# Purpose: Automatically scan core/ (and later industry/) directories, parse frontmatter, and generate docs/INDEX.md exactly matching Paul's requested style. Uses the package's own frontmatter parser for consistency with the runtime API.
"""
Build OrgContext Corpus Index
Usage:
    python scripts/build_index.py
"""

import sys
from collections import defaultdict
from pathlib import Path

# Make the package importable when this script is run directly.
sys.path.insert(0, str(Path(__file__).parent.parent))

from orgcontext import _parse_frontmatter  # noqa: E402

# ── Config ─────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
CORE_DIR = REPO_ROOT / "core"
INDUSTRY_DIR = CORE_DIR / "industry"
DOCS_DIR = REPO_ROOT / "docs"
OUTPUT_FILE = DOCS_DIR / "index.md"


# ── Helpers ────────────────────────────────────────────────────────────────────
def parse_frontmatter(content: str) -> dict:
    """Delegate to the package's own frontmatter parser.

    The package parser handles both single-line (`[a, b]`) and multi-line
    (`- a` / `- b`) YAML list shapes, which the previous standalone parser
    silently dropped for fields like `references:` and `related:`.
    """
    return _parse_frontmatter(content)


def build_index():
    """Scan entries and write docs/INDEX.md in the exact requested format."""
    entries_by_category = defaultdict(list)

    industry_by_sector = defaultdict(list)

    # Scan core/ — exclude industry/ subdirectory
    for md_file in sorted(CORE_DIR.rglob("*.md")):
        if INDUSTRY_DIR.exists() and md_file.is_relative_to(INDUSTRY_DIR):
            continue
        content = md_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        if not fm or not fm.get("id") or not fm.get("title"):
            continue
        rel_path = md_file.relative_to(REPO_ROOT)
        category = fm.get("category", "uncategorized")
        entries_by_category[category].append(
            {
                "id": fm["id"],
                "title": fm["title"],
                "tags": fm.get("tags", []),
                "path": str(rel_path),
            }
        )

    # Scan core/industry/ separately
    if INDUSTRY_DIR.exists():
        for md_file in sorted(INDUSTRY_DIR.rglob("*.md")):
            content = md_file.read_text(encoding="utf-8")
            fm = parse_frontmatter(content)
            if not fm or not fm.get("id") or not fm.get("title"):
                continue
            rel_path = md_file.relative_to(REPO_ROOT)
            sector = md_file.parent.name
            industry_by_sector[sector].append(
                {
                    "id": fm["id"],
                    "title": fm["title"],
                    "tags": fm.get("tags", []),
                    "path": str(rel_path),
                }
            )

    # Ensure docs/ exists
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    # Build markdown
    lines = [
        "# OrgContext Corpus Index",
        "",
        "> Auto-generated. Do not edit manually. Run `python scripts/build_index.py` to regenerate.",
        "",
    ]

    total = sum(len(v) for v in entries_by_category.values())
    lines.append(f"## Core Entries ({total})")
    lines.append("")

    # Preferred category order (matches your example)
    preferred_order = [
        "mission-vision",
        "leadership-frameworks",
        "roles-responsibilities",
        "governance",
        "culture-values",
        "strategy-execution",
    ]

    for cat in preferred_order:
        if cat not in entries_by_category:
            continue
        entries = entries_by_category[cat]
        if not entries:
            continue
        lines.append(f"### {cat}")
        lines.append("| ID | Title | Tags |")
        lines.append("|----|-------|------|")
        for e in entries:
            tags_str = ", ".join(e["tags"]) if e["tags"] else ""
            link = f"[{e['id']}]({e['path']})"
            lines.append(f"| {link} | {e['title']} | {tags_str} |")
        lines.append("")

    # Add any extra core categories that might appear (alphabetically)
    extra_cats = sorted(set(entries_by_category.keys()) - set(preferred_order))
    for cat in extra_cats:
        entries = entries_by_category[cat]
        lines.append(f"### {cat}")
        lines.append("| ID | Title | Tags |")
        lines.append("|----|-------|------|")
        for e in entries:
            tags_str = ", ".join(e["tags"]) if e["tags"] else ""
            link = f"[{e['id']}]({e['path']})"
            lines.append(f"| {link} | {e['title']} | {tags_str} |")
        lines.append("")

    # Industry entries section
    if industry_by_sector:
        industry_total = sum(len(v) for v in industry_by_sector.values())
        lines.append(f"## Industry Entries ({industry_total})")
        lines.append("")
        for sector in sorted(industry_by_sector.keys()):
            entries = industry_by_sector[sector]
            lines.append(f"### {sector}")
            lines.append("| ID | Title | Tags |")
            lines.append("|----|-------|------|")
            for e in entries:
                tags_str = ", ".join(e["tags"]) if e["tags"] else ""
                link = f"[{e['id']}]({e['path']})"
                lines.append(f"| {link} | {e['title']} | {tags_str} |")
            lines.append("")

    # Planned Entries section
    lines.append("---")
    lines.append("## Planned Entries (contributions welcome)")
    lines.append("")
    lines.append(
        "See [open issues labeled `new-entry`](https://github.com/sevasek/orgcontext/issues?q=label%3Anew-entry) for entries the community has proposed. The GitHub Issues list is the source of truth for planned work."
    )

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    industry_total = sum(len(v) for v in industry_by_sector.values())
    print(f"✅ Index generated successfully: {OUTPUT_FILE}")
    print(
        f"   Found {total} core entries and {industry_total} industry entries ({total + industry_total} total)"
    )


if __name__ == "__main__":
    if not CORE_DIR.exists():
        print("Error: core/ directory not found. Please run from the repository root.")
        sys.exit(1)
    build_index()
