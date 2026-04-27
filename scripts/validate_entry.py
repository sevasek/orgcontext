#!/usr/bin/env python3
"""
Validate OrgContext entry files against the spec in docs/entry-format.md.

Usage:
    python scripts/validate_entry.py core/leadership-frameworks/servant-leadership.md
    python scripts/validate_entry.py --all
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────────────

REQUIRED_FRONTMATTER = ["id", "title", "category", "tags", "version", "last_updated"]
VALID_CATEGORIES = [
    "mission-vision",
    "roles-responsibilities",
    "leadership-frameworks",
    "governance",
    "culture-values",
    "strategy-execution",
]
REQUIRED_SECTIONS = [
    "Definition",
    "When to Apply",
    "Decision Heuristics",
    "Counter-Examples / Anti-Patterns",
    "Prompt Snippet",
    "See Also",
]
WORD_LIMITS = {
    "Definition": (50, 300),
    "Prompt Snippet": (30, 150),
}
TOTAL_WORD_LIMIT = (300, 1200)
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# ── Helpers ─────────────────────────────────────────────────────────────────────

def _parse_frontmatter(raw: str) -> tuple[dict, str]:
    match = re.match(r"^---\n(.*?)---\n", raw, re.DOTALL)
    if not match:
        return {}, raw
    fm_text = match.group(1)
    body = raw[match.end():]
    fm: dict = {}
    try:
        import yaml
        fm = yaml.safe_load(fm_text) or {}
    except ImportError:
        for line in fm_text.splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                fm[k.strip()] = v.strip()
    return fm, body


def _parse_sections(body: str) -> dict[str, str]:
    parts = re.split(r"^## (.+)$", body, flags=re.MULTILINE)
    sections = {}
    it = iter(parts[1:])
    for heading, content in zip(it, it):
        sections[heading.strip()] = content.strip()
    return sections


def _word_count(text: str) -> int:
    # Strip markdown syntax before counting
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"[#*`\[\]()>_~]", "", text)
    return len(text.split())


# ── Validation ──────────────────────────────────────────────────────────────────

def validate_file(path: Path) -> list[str]:
    """Return a list of error strings. Empty list = valid."""
    errors: list[str] = []
    raw = path.read_text(encoding="utf-8")
    fm, body = _parse_frontmatter(raw)

    # ── Frontmatter checks ──────────────────────────────────────────────────────
    if not fm:
        errors.append("MISSING frontmatter (expected --- ... --- block at top of file)")
        return errors  # can't validate further without frontmatter

    for field in REQUIRED_FRONTMATTER:
        if field not in fm or not fm[field]:
            errors.append(f"MISSING required frontmatter field: '{field}'")

    if "id" in fm and fm["id"] != path.stem:
        errors.append(
            f"MISMATCH: frontmatter id='{fm['id']}' but filename is '{path.stem}.md'"
        )

    if "category" in fm and fm["category"] not in VALID_CATEGORIES:
        errors.append(
            f"INVALID category '{fm['category']}'. Valid: {', '.join(VALID_CATEGORIES)}"
        )

    if "version" in fm and not SEMVER_RE.match(str(fm["version"])):
        errors.append(f"INVALID version '{fm['version']}': must be semver (e.g. 1.0.0)")

    if "last_updated" in fm and not DATE_RE.match(str(fm["last_updated"])):
        errors.append(
            f"INVALID last_updated '{fm['last_updated']}': must be YYYY-MM-DD"
        )

    # ── Section checks ──────────────────────────────────────────────────────────
    sections = _parse_sections(body)

    for section in REQUIRED_SECTIONS:
        if section not in sections:
            errors.append(f"MISSING required section: '## {section}'")
        elif not sections[section].strip():
            errors.append(f"EMPTY required section: '## {section}'")

    # Word count checks per section
    for section, (min_w, max_w) in WORD_LIMITS.items():
        if section in sections:
            # For Prompt Snippet, only count content inside the code block
            text = sections[section]
            if section == "Prompt Snippet":
                match = re.search(r"```[^\n]*\n(.*?)```", text, re.DOTALL)
                text = match.group(1) if match else text
            count = _word_count(text)
            if count < min_w:
                errors.append(
                    f"TOO SHORT '## {section}': {count} words (min {min_w})"
                )
            elif count > max_w:
                errors.append(
                    f"TOO LONG '## {section}': {count} words (max {max_w})"
                )

    # Total word count
    total = _word_count(body)
    if total < TOTAL_WORD_LIMIT[0]:
        errors.append(f"ENTRY TOO SHORT: {total} total words (min {TOTAL_WORD_LIMIT[0]})")
    elif total > TOTAL_WORD_LIMIT[1]:
        errors.append(
            f"ENTRY TOO LONG: {total} total words (max {TOTAL_WORD_LIMIT[1]}). "
            "Consider splitting into two entries."
        )

    # Prompt Snippet code block check
    if "Prompt Snippet" in sections:
        if "```" not in sections["Prompt Snippet"]:
            errors.append(
                "Prompt Snippet must contain a fenced code block (``` ... ```)"
            )

    return errors


# ── CLI ─────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Validate OrgContext entry files.")
    parser.add_argument("path", nargs="?", help="Path to a single .md file")
    parser.add_argument(
        "--all", action="store_true", help="Validate all entries in core/ and industry/"
    )
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    files: list[Path] = []

    if args.all:
        for d in ("core", "industry"):
            files.extend(sorted((repo_root / d).rglob("*.md")))
    elif args.path:
        files = [Path(args.path)]
    else:
        parser.print_help()
        sys.exit(0)

    total_errors = 0
    for f in files:
        errors = validate_file(f)
        rel = f.relative_to(repo_root)
        if errors:
            print(f"\n❌  {rel}")
            for e in errors:
                print(f"   • {e}")
            total_errors += len(errors)
        else:
            print(f"✅  {rel}")

    print(f"\n{'─' * 50}")
    if total_errors == 0:
        print(f"All {len(files)} entries valid.")
        sys.exit(0)
    else:
        print(f"{total_errors} error(s) across {len(files)} entries.")
        sys.exit(1)


if __name__ == "__main__":
    main()
