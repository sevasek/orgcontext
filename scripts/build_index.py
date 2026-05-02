# Title: OrgContext Corpus Index Builder
# Purpose: Automatically scan core/ (and later industry/) directories, parse frontmatter, and generate docs/INDEX.md exactly matching Paul's requested style. Pure stdlib, no external dependencies.

#!/usr/bin/env python3
"""
Build OrgContext Corpus Index
Usage:
    python scripts/build_index.py
"""

from pathlib import Path
import re
import sys
from collections import defaultdict

# ── Config ─────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
CORE_DIR = REPO_ROOT / "core"
INDUSTRY_DIR = REPO_ROOT / "industry"
DOCS_DIR = REPO_ROOT / "docs"
OUTPUT_FILE = DOCS_DIR / "index.md"

# ── Helpers ────────────────────────────────────────────────────────────────────
def parse_frontmatter(content: str) -> dict:
    """Extract YAML-style frontmatter using regex (no PyYAML dependency)."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fm_text = match.group(1)
    fm = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith('#') or ':' not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'").strip()
        # Simple list handling
        if value.startswith("[") and value.endswith("]"):
            items = [item.strip().strip('"').strip("'") for item in value[1:-1].split(",") if item.strip()]
            fm[key] = [i for i in items if i]
        else:
            fm[key] = value
    return fm


def build_index():
    """Scan entries and write docs/INDEX.md in the exact requested format."""
    entries_by_category = defaultdict(list)

    # Scan core/
    for md_file in sorted(CORE_DIR.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        if not fm or not fm.get("id") or not fm.get("title"):
            continue
        rel_path = md_file.relative_to(REPO_ROOT)
        category = fm.get("category", "uncategorized")
        entries_by_category[category].append({
            "id": fm["id"],
            "title": fm["title"],
            "tags": fm.get("tags", []),
            "path": str(rel_path)
        })

    # Ensure docs/ exists
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    # Build markdown
    lines = [
        "# OrgContext Corpus Index",
        "",
        "> Auto-generated. Do not edit manually. Run `python scripts/build_index.py` to regenerate.",
        ""
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
        "strategy-execution"
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

    # Add any extra categories that might appear (alphabetically)
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

    # Planned Entries section
    lines.append("---")
    lines.append("## Planned Entries (contributions welcome)")
    lines.append("")
    lines.append("See [open issues labeled `new-entry`](https://github.com/sevasek/orgcontext/issues?q=label%3Anew-entry) for entries the community has proposed.")
    lines.append("")
    lines.append("High-priority gaps:")
    lines.append("**mission-vision:** `bhag`, `organizational-purpose`")
    lines.append("**leadership-frameworks:** `adaptive-leadership`, `distributed-leadership`")
    lines.append("**roles-responsibilities:** `product-manager`, `cto`, `chief-of-staff`, `engineering-manager`")
    lines.append("**governance:** `steering-committee`, `working-group`")
    lines.append("**culture-values:** `belonging`, `team-norms`")
    lines.append("**strategy-execution:** `portfolio-management`, `change-management`")

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Index generated successfully: {OUTPUT_FILE}")
    print(f"   Found {total} entries")


if __name__ == "__main__":
    if not CORE_DIR.exists():
        print("Error: core/ directory not found. Please run from the repository root.")
        sys.exit(1)
    build_index()