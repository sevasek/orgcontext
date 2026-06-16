"""
OrgContext Python loader.

Usage:
    from orgcontext import load, inject, list_entries

    entry = load("servant-leadership")
    print(entry.definition)
    print(entry.prompt_snippet)

    context_block = inject(["okrs", "raci", "mission-alignment"])
"""

from __future__ import annotations

import re
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import yaml  # PyYAML, optional but recommended

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

__version__ = "0.2.0"
__all__ = [
    "load",
    "inject",
    "list_entries",
    "search_entries",
    "get_frontmatter",
    "OrgContextEntry",
]

# ── Path resolution ────────────────────────────────────────────────────────────


def _corpus_root() -> Path:
    """Return the path to the corpus root (the directory containing core/).

    Resolution order:
      1. The directory two levels up from this file (the repo root for
         source checkouts and editable installs).
      2. Fail loudly if core/ is not found at the expected location.

    A silent fallback to the installed package root was removed: it caused
    tests run from a different working directory (CI, sub-shells) to
    succeed against the installed package's bundled corpus instead of
    failing, masking real path issues.
    """
    root = Path(__file__).parent.parent
    if (root / "core").exists():
        return root
    raise RuntimeError(
        f"Could not locate OrgContext corpus root. Expected 'core/' at "
        f"{root}, but it was not found. If you are running tests from a "
        f"different working directory, pass corpus_root= explicitly."
    )


# ── Data model ─────────────────────────────────────────────────────────────────


@dataclass
class OrgContextEntry:
    id: str
    title: str
    category: str
    tags: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)
    version: str = "1.0.0"
    last_updated: str = ""
    authors: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    deprecated: bool = False
    raw_markdown: str = ""

    # Parsed sections (populated lazily)
    _sections: dict[str, str] = field(default_factory=dict, repr=False)

    # ── Section accessors ──────────────────────────────────────────────────────

    @property
    def definition(self) -> str:
        return self._section("Definition")

    @property
    def when_to_apply(self) -> str:
        return self._section("When to Apply")

    @property
    def decision_heuristics(self) -> str:
        return self._section("Decision Heuristics")

    @property
    def anti_patterns(self) -> str:
        return self._section("Counter-Examples / Anti-Patterns")

    @property
    def prompt_snippet(self) -> str:
        """Returns the content of the fenced code block inside ## Prompt Snippet."""
        raw = self._section("Prompt Snippet")
        # Strip outer fenced code block if present
        match = re.search(r"```[^\n]*\n(.*?)```", raw, re.DOTALL)
        return match.group(1).strip() if match else raw.strip()

    @property
    def see_also(self) -> str:
        return self._section("See Also")

    # ── Internal helpers ───────────────────────────────────────────────────────

    def _section(self, heading: str) -> str:
        if not self._sections:
            self._parse_sections()
        return self._sections.get(heading, "")

    def _parse_sections(self) -> None:
        """Split the markdown body into named sections."""
        # Strip YAML frontmatter
        body = re.sub(r"^---\n.*?---\n", "", self.raw_markdown, flags=re.DOTALL)
        # Split on ## headings
        parts = re.split(r"^## (.+)$", body, flags=re.MULTILINE)
        # parts alternates: [pre-heading text, heading1, content1, heading2, content2, ...]
        it = iter(parts[1:])  # skip pre-heading text
        for heading, content in zip(it, it):
            self._sections[heading.strip()] = content.strip()

    def to_dict(self, include_sections: bool = True) -> dict:
        """Return a JSON-serializable dict representation of the entry.

        Args:
            include_sections: If True, includes common section properties.
        """
        data = {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "tags": self.tags,
            "related": self.related,
            "version": self.version,
            "last_updated": self.last_updated,
            "authors": self.authors,
            "references": self.references,
            "deprecated": self.deprecated,
            "raw_markdown": self.raw_markdown,
        }
        if include_sections:
            data.update(
                {
                    "definition": self.definition,
                    "when_to_apply": self.when_to_apply,
                    "decision_heuristics": self.decision_heuristics,
                    "anti_patterns": self.anti_patterns,
                    "prompt_snippet": self.prompt_snippet,
                    "see_also": self.see_also,
                }
            )
        return data


# ── Core API ───────────────────────────────────────────────────────────────────


def _find_entry_path(entry_id: str, corpus_root: Path) -> Optional[Path]:
    """Search all subdirectories of core/ and industry/ for <entry_id>.md."""
    for md_file in corpus_root.rglob("*.md"):
        if md_file.stem == entry_id and any(part in ("core", "industry") for part in md_file.parts):
            return md_file
    return None


def _parse_frontmatter(raw: str) -> dict:
    """Extract YAML frontmatter from a markdown string."""
    match = re.match(r"^---\n(.*?)---\n", raw, re.DOTALL)
    if not match:
        return {}
    fm_text = match.group(1)
    if HAS_YAML:
        return yaml.safe_load(fm_text) or {}

    # Minimal fallback parser for key: value lines
    result = {}
    for line in fm_text.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            result[k.strip()] = v.strip().strip('"').strip("'")
    return result


def load(entry_id: str, corpus_root: Optional[Path] = None) -> OrgContextEntry:
    """
    Load a single OrgContext entry by ID.

    Args:
        entry_id: The slug ID of the entry (e.g. "servant-leadership").
        corpus_root: Optional override for the corpus root directory.

    Returns:
        OrgContextEntry with parsed frontmatter and section accessors.

    Raises:
        FileNotFoundError: If no entry with the given ID exists.
    """
    if not entry_id or not isinstance(entry_id, str):
        raise ValueError("entry_id must be a non-empty string")

    root = corpus_root or _corpus_root()
    path = _find_entry_path(entry_id, root)
    if path is None:
        raise FileNotFoundError(
            f"No entry found for '{entry_id}'. Run list_entries() to see available IDs."
        )
    raw = path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(raw)

    entry = OrgContextEntry(
        id=fm.get("id", entry_id),
        title=fm.get("title", entry_id),
        category=fm.get("category", ""),
        tags=fm.get("tags", []) or [],
        related=fm.get("related", []) or [],
        version=fm.get("version", "1.0.0"),
        last_updated=str(fm.get("last_updated", "")),
        authors=fm.get("authors", []) or [],
        references=fm.get("references", []) or [],
        deprecated=bool(fm.get("deprecated", False)),
        raw_markdown=raw,
    )

    if entry.deprecated:
        warnings.warn(
            f"Entry '{entry.id}' is marked as deprecated. "
            "Consider migrating to a newer alternative.",
            DeprecationWarning,
            stacklevel=2,
        )

    return entry


def inject(
    entry_ids: list[str],
    separator: str = "\n\n---\n\n",
    corpus_root: Optional[Path] = None,
) -> str:
    """
    Load multiple entries and return a combined prompt-ready block.

    Args:
        entry_ids: List of entry ID slugs to load.
        separator: String to join entries with (default: horizontal rule).
        corpus_root: Optional override for the corpus root directory.

    Returns:
        A single string containing all prompt snippets, ready to inject
        into a system prompt or agent context.
    """
    snippets = []
    for eid in entry_ids:
        entry = load(eid, corpus_root=corpus_root)
        snippets.append(entry.prompt_snippet)
    return separator.join(snippets)


def list_entries(
    category: Optional[str] = None,
    corpus_root: Optional[Path] = None,
) -> list[dict]:
    """
    List all available entries in the corpus.

    Args:
        category: Optional filter by category slug.
        corpus_root: Optional override for the corpus root directory.

    Returns:
        List of dicts with keys: id, title, category, tags, path, authors,
        version, last_updated, deprecated.
    """
    root = corpus_root or _corpus_root()
    results = []
    for md_file in sorted(root.rglob("*.md")):
        if not any(part in ("core", "industry") for part in md_file.parts):
            continue
        raw = md_file.read_text(encoding="utf-8")
        fm = _parse_frontmatter(raw)
        if not fm.get("id"):
            continue
        if category and fm.get("category") != category:
            continue
        results.append(
            {
                "id": fm.get("id", md_file.stem),
                "title": fm.get("title", fm["id"]),
                "category": fm.get("category", ""),
                "tags": fm.get("tags", []) or [],
                "path": str(md_file.relative_to(root)),
                "authors": fm.get("authors", []) or [],
                "version": fm.get("version", "1.0.0"),
                "last_updated": str(fm.get("last_updated", "")),
                "deprecated": bool(fm.get("deprecated", False)),
            }
        )
    return results


def search_entries(
    query: str,
    corpus_root: Optional[Path] = None,
) -> list[dict]:
    """
    Search entries by keyword across id, title, category, tags, and authors.

    Args:
        query: Search string (case-insensitive). An empty or whitespace-only
            query returns an empty list — use list_entries() to enumerate
            all entries. (Earlier implementations returned every entry for
            an empty query due to Python's ``"" in s == True`` semantics,
            which surprised callers.)
        corpus_root: Optional override for the corpus root directory.

    Returns:
        List of matching entry dicts (same structure as list_entries).
    """
    q = (query or "").strip().lower()
    if not q:
        return []
    all_entries = list_entries(corpus_root=corpus_root)
    matches = [
        e
        for e in all_entries
        if (
            q in e["id"].lower()
            or q in e["title"].lower()
            or q in e.get("category", "").lower()
            or any(q in (tag or "").lower() for tag in e.get("tags", []))
            or any(q in (str(a) or "").lower() for a in e.get("authors", []))
        )
    ]
    return matches


def get_frontmatter(
    entry_id: str,
    corpus_root: Optional[Path] = None,
) -> dict:
    """
    Return the raw frontmatter dictionary for a given entry ID.

    Useful for accessing all metadata without loading the full entry.

    Raises:
        FileNotFoundError: If no entry with the given ID exists. (Earlier
            versions raised KeyError; FileNotFoundError matches load()'s
            contract for the same condition.)
    """
    root = corpus_root or _corpus_root()
    # Find the file
    for md_file in root.rglob("*.md"):
        if not any(part in ("core", "industry") for part in md_file.parts):
            continue
        if md_file.stem == entry_id:
            raw = md_file.read_text(encoding="utf-8")
            return _parse_frontmatter(raw)
    raise FileNotFoundError(
        f"No entry found for '{entry_id}'. Run list_entries() to see available IDs."
    )
