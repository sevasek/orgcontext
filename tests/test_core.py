"""Tests for orgcontext core package."""

import re
from pathlib import Path

import pytest

from orgcontext import (
    OrgContextEntry,
    get_frontmatter,
    inject,
    list_entries,
    load,
    search_entries,
)


CORPUS_ROOT = Path(__file__).parent.parent / "core"
# Mirrors DATE_RE in scripts/validate_entry.py. Kept in sync; if the
# validator's regex changes, update this too.
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class TestLoad:
    def test_load_servant_leadership(self):
        entry = load("servant-leadership", corpus_root=CORPUS_ROOT.parent)
        assert entry.id == "servant-leadership"
        assert entry.title == "Servant Leadership"
        assert entry.category == "leadership-frameworks"
        assert "leadership" in entry.tags
        assert len(entry.tags) >= 3

    def test_load_populates_sections(self):
        entry = load("servant-leadership", corpus_root=CORPUS_ROOT.parent)
        assert entry.definition
        assert len(entry.definition) > 50
        assert entry.when_to_apply
        assert entry.decision_heuristics
        assert entry.anti_patterns
        assert entry.prompt_snippet
        assert entry.see_also

    def test_load_file_not_found(self):
        with pytest.raises(FileNotFoundError, match="No entry found"):
            load("nonexistent-entry", corpus_root=CORPUS_ROOT.parent)

    def test_load_empty_entry_id(self):
        with pytest.raises(ValueError, match="entry_id must be a non-empty string"):
            load("", corpus_root=CORPUS_ROOT.parent)

    def test_load_none_entry_id(self):
        with pytest.raises(ValueError):
            load(None, corpus_root=CORPUS_ROOT.parent)  # type: ignore[arg-type]

    def test_load_okrs(self):
        entry = load("okrs", corpus_root=CORPUS_ROOT.parent)
        assert entry.id == "okrs"
        assert entry.category == "strategy-execution"

    def test_load_related_entries(self):
        entry = load("servant-leadership", corpus_root=CORPUS_ROOT.parent)
        assert "transformational-leadership" in entry.related
        assert "psychological-safety" in entry.related

    def test_load_version_and_date(self):
        entry = load("servant-leadership", corpus_root=CORPUS_ROOT.parent)
        assert entry.version == "1.0.0"
        assert DATE_RE.match(entry.last_updated), (
            f"last_updated '{entry.last_updated}' must match YYYY-MM-DD"
        )

    def test_load_authors_and_references(self):
        entry = load("okrs", corpus_root=CORPUS_ROOT.parent)
        assert entry.authors == ["Paul Seville"]
        assert len(entry.references) >= 1
        assert "Measure What Matters" in str(entry.references) or "John Doerr" in str(
            entry.references
        )
        assert entry.deprecated is False

    def test_to_dict_returns_expected_keys(self):
        entry = load("servant-leadership", corpus_root=CORPUS_ROOT.parent)
        d = entry.to_dict()
        for key in [
            "id",
            "title",
            "category",
            "authors",
            "version",
            "last_updated",
            "deprecated",
            "prompt_snippet",
        ]:
            assert key in d
        assert d["id"] == "servant-leadership"
        assert d["authors"] == ["Paul Seville"]
        assert DATE_RE.match(d["last_updated"]), (
            f"last_updated '{d['last_updated']}' must match YYYY-MM-DD"
        )

    def test_to_dict_without_sections(self):
        entry = load("raci", corpus_root=CORPUS_ROOT.parent)
        d = entry.to_dict(include_sections=False)
        assert "definition" not in d
        assert "prompt_snippet" not in d
        assert d["id"] == "raci"


class TestInject:
    def test_inject_returns_combined_snippets(self):
        result = inject(["okrs", "raci"], corpus_root=CORPUS_ROOT.parent)
        assert "okrs" in result.lower() or "OKR" in result
        assert "raci" in result.lower() or "RACI" in result
        assert "---" in result

    def test_inject_single_entry(self):
        result = inject(["mission-alignment"], corpus_root=CORPUS_ROOT.parent)
        assert result
        assert "---" not in result

    def test_inject_nonexistent_entry(self):
        with pytest.raises(FileNotFoundError):
            inject(["okrs", "nonexistent"], corpus_root=CORPUS_ROOT.parent)

    def test_inject_custom_separator(self):
        result = inject(["okrs", "raci"], separator="\n===\n", corpus_root=CORPUS_ROOT.parent)
        assert "===" in result
        assert "---" not in result


class TestListEntries:
    def test_list_all_entries(self):
        entries = list_entries(corpus_root=CORPUS_ROOT.parent)
        # Use >= (not ==) so adding entries doesn't break this test;
        # the explicit ID checks below verify which entries are present.
        assert len(entries) >= 34
        ids = {e["id"] for e in entries}
        # Core entries (sampled)
        assert "servant-leadership" in ids
        assert "okrs" in ids
        assert "raci" in ids
        # Industry-pack entries (regression guard for the feat/industry-packs commit)
        assert "product-market-fit" in ids
        assert "digital-transformation" in ids
        assert "theory-of-change" in ids

    def test_list_entries_by_category(self):
        entries = list_entries(category="governance", corpus_root=CORPUS_ROOT.parent)
        assert len(entries) == 5
        ids = [e["id"] for e in entries]
        assert "raci" in ids
        assert "decision-rights" in ids
        assert "escalation-path" in ids
        assert "steering-committee" in ids
        assert "working-group" in ids

    def test_list_entries_industry_tech_startup(self):
        entries = list_entries(category="tech-startup", corpus_root=CORPUS_ROOT.parent)
        ids = [e["id"] for e in entries]
        assert "product-market-fit" in ids
        assert len(entries) >= 1

    def test_list_entries_industry_enterprise(self):
        entries = list_entries(category="enterprise", corpus_root=CORPUS_ROOT.parent)
        ids = [e["id"] for e in entries]
        assert "digital-transformation" in ids
        assert len(entries) >= 1

    def test_list_entries_industry_nonprofit(self):
        entries = list_entries(category="nonprofit", corpus_root=CORPUS_ROOT.parent)
        ids = [e["id"] for e in entries]
        assert "theory-of-change" in ids
        assert len(entries) >= 1

    def test_list_entries_each_has_required_keys(self):
        entries = list_entries(corpus_root=CORPUS_ROOT.parent)
        for entry in entries:
            assert "id" in entry
            assert "title" in entry
            assert "category" in entry
            assert "tags" in entry
            assert "path" in entry
            assert "authors" in entry
            assert "version" in entry
            assert "last_updated" in entry
            assert "deprecated" in entry

    def test_list_entries_empty_category(self):
        entries = list_entries(category="nonexistent-category", corpus_root=CORPUS_ROOT.parent)
        assert len(entries) == 0


class TestOrgContextEntry:
    def test_prompt_snippet_strips_code_block(self):
        entry = OrgContextEntry(
            id="test",
            title="Test",
            category="governance",
            raw_markdown="""---
id: test
title: Test
category: governance
tags: [test]
version: 1.0.0
last_updated: 2026-01-01
---

## Prompt Snippet
```
This is the snippet content.
```
""",
        )
        snippet = entry.prompt_snippet
        assert "```" not in snippet
        assert "This is the snippet content." in snippet

    def test_prompt_snippet_without_code_block(self):
        entry = OrgContextEntry(
            id="test",
            title="Test",
            category="governance",
            raw_markdown="""---
id: test
title: Test
category: governance
tags: [test]
version: 1.0.0
last_updated: 2026-01-01
---

## Prompt Snippet
Plain snippet text without code fences.
""",
        )
        assert entry.prompt_snippet == "Plain snippet text without code fences."

    def test_section_returns_empty_for_missing(self):
        entry = OrgContextEntry(
            id="test",
            title="Test",
            category="governance",
            raw_markdown="""---
id: test
title: Test
category: governance
tags: [test]
version: 1.0.0
last_updated: 2026-01-01
---

## Definition
Some definition.
""",
        )
        assert entry.when_to_apply == ""
        assert entry.decision_heuristics == ""

    def test_default_field_values(self):
        entry = OrgContextEntry(id="test", title="Test", category="governance")
        assert entry.tags == []
        assert entry.related == []
        assert entry.version == "1.0.0"
        assert entry.last_updated == ""
        assert entry.authors == []
        assert entry.references == []
        assert entry.deprecated is False
        assert entry.raw_markdown == ""


class TestAllEntriesValid:
    def test_all_core_entries_loadable(self):
        entries = list_entries(corpus_root=CORPUS_ROOT.parent)
        for entry_meta in entries:
            entry = load(entry_meta["id"], corpus_root=CORPUS_ROOT.parent)
            assert entry.id == entry_meta["id"]
            assert entry.prompt_snippet, f"Entry {entry_meta['id']} has empty prompt_snippet"
            assert entry.definition, f"Entry {entry_meta['id']} has empty definition"


class TestSearchAndMetadata:
    def test_search_entries_finds_by_title_and_tags(self):
        results = search_entries("leadership", corpus_root=CORPUS_ROOT.parent)
        ids = [e["id"] for e in results]
        assert "servant-leadership" in ids
        assert "transformational-leadership" in ids or "situational-leadership" in ids

    def test_search_entries_by_author(self):
        results = search_entries("Paul Seville", corpus_root=CORPUS_ROOT.parent)
        assert len(results) >= 1
        assert any(e["id"] == "okrs" for e in results)

    def test_search_entries_empty_query(self):
        # An empty query must return [], not "everything". Earlier
        # implementations returned every entry because Python's
        # `"" in s == True` made the predicate trivially true. To list
        # everything, call list_entries() directly.
        results = search_entries("", corpus_root=CORPUS_ROOT.parent)
        assert results == []

    def test_search_entries_whitespace_query(self):
        # Whitespace-only is also a "no query" case.
        results = search_entries("   ", corpus_root=CORPUS_ROOT.parent)
        assert results == []

    def test_list_entries_includes_metadata(self):
        entries = list_entries(corpus_root=CORPUS_ROOT.parent)
        sample = next(e for e in entries if e["id"] == "okrs")
        assert "authors" in sample
        assert "last_updated" in sample
        assert DATE_RE.match(sample["last_updated"]), (
            f"last_updated '{sample['last_updated']}' must match YYYY-MM-DD"
        )

    def test_get_frontmatter_returns_dict(self):
        fm = get_frontmatter("raci", corpus_root=CORPUS_ROOT.parent)
        assert fm["id"] == "raci"
        assert "authors" in fm
        assert "tags" in fm

    def test_deprecation_warning(self, recwarn):
        # Create a temporary deprecated entry for test? For now we test the warning path manually
        # Since no entries are currently deprecated, we just ensure the mechanism exists
        # by checking that load doesn't break and warning code is present
        entry = load("okrs", corpus_root=CORPUS_ROOT.parent)
        assert entry.deprecated is False  # current state
        # The warning logic was added in Win 3; this test documents expected behavior
        assert hasattr(entry, "deprecated")


class TestIndustryEntriesLoadable:
    """Regression guard for the feat/industry-packs commit.

    The industry/ subdirectory lives one level deeper than core/ category
    directories (core/<category>/<file>.md vs core/industry/<sector>/<file>.md).
    A path-resolution bug in load() that only handles the shallower layout
    would not be caught by the count-bump in test_list_all_entries; these
    tests force load() to actually open each new file.
    """

    def test_load_product_market_fit(self):
        entry = load("product-market-fit", corpus_root=CORPUS_ROOT.parent)
        assert entry.id == "product-market-fit"
        assert entry.category == "tech-startup"
        assert entry.definition
        assert entry.prompt_snippet
        # related link to an existing entry must parse as a list
        assert isinstance(entry.related, list)
        assert "north-star-metric" in entry.related
        assert "product-manager" in entry.related

    def test_load_digital_transformation(self):
        entry = load("digital-transformation", corpus_root=CORPUS_ROOT.parent)
        assert entry.id == "digital-transformation"
        assert entry.category == "enterprise"
        assert entry.definition
        assert entry.prompt_snippet
        assert "portfolio-management" in entry.related

    def test_load_theory_of_change(self):
        entry = load("theory-of-change", corpus_root=CORPUS_ROOT.parent)
        assert entry.id == "theory-of-change"
        assert entry.category == "nonprofit"
        assert entry.definition
        assert entry.prompt_snippet
        assert "organizational-purpose" in entry.related

    def test_load_nonexistent_industry_id(self):
        with pytest.raises(FileNotFoundError, match="No entry found"):
            load("nope-not-an-entry", corpus_root=CORPUS_ROOT.parent)


class TestRelatedLinkIntegrity:
    """Every entry declared in `related` must resolve to an existing corpus entry.

    Catches typos and references to planned-but-not-yet-added entries before
    a traversal feature (e.g. recursive inject) hits FileNotFoundError.
    """

    def test_no_broken_related_links(self):
        all_ids = {e["id"] for e in list_entries(corpus_root=CORPUS_ROOT.parent)}
        # Mirror the same loading path the validator uses, then check each
        # entry's related list against the global ID set.
        broken: list[tuple[str, str]] = []
        for eid in sorted(all_ids):
            entry = load(eid, corpus_root=CORPUS_ROOT.parent)
            for target in entry.related:
                if target not in all_ids:
                    broken.append((entry.id, target))
        assert not broken, f"Broken related links: {broken}"


class TestDeprecationWarning:
    """Regression guard: the deprecation warning must actually fire on load().

    Previously the warning block sat after an unconditional return in load()
    (dead code), so deprecated entries would load silently. This test loads a
    synthetic in-memory entry via the parser path that the API uses, to
    confirm the warning is emitted when deprecated=True.
    """

    def test_load_warns_when_entry_is_deprecated(self, tmp_path, recwarn):
        # Build a minimal corpus with one deprecated entry on disk, since
        # load() resolves entries by file path (not by ID lookup table).
        deprecated_id = "deprecated-fixture"
        (tmp_path / "core").mkdir(parents=True)
        (tmp_path / "core" / "mission-vision").mkdir()
        (tmp_path / "core" / "industry").mkdir()
        entry_path = tmp_path / "core" / "mission-vision" / f"{deprecated_id}.md"
        entry_path.write_text(
            "---\n"
            f"id: {deprecated_id}\n"
            "title: Deprecated Fixture\n"
            "category: mission-vision\n"
            "tags: [fixture]\n"
            "version: 1.0.0\n"
            "last_updated: 2026-01-01\n"
            "deprecated: true\n"
            "---\n\n"
            "## Definition\nFixture for testing the deprecation warning path on load().\n\n"
            "## When to Apply\nUse only in test contexts.\n\n"
            "## Decision Heuristics\nNone — this is a fixture.\n\n"
            "## Counter-Examples / Anti-Patterns\nN/A for this fixture.\n\n"
            "## Prompt Snippet\n```\nFixture snippet — not for production use.\n```\n\n"
            "## See Also\nNone.\n",
            encoding="utf-8",
        )

        with pytest.warns(DeprecationWarning, match=deprecated_id):
            load(deprecated_id, corpus_root=tmp_path)


class TestCorpusRootResolver:
    """Regression guard: the resolver must fail loudly when core/ is missing.

    The previous implementation silently fell back to the installed package
    root when `core/` was not found at the expected location. That made
    tests run from an unexpected working directory (CI sub-shells, etc.)
    succeed against stale bundled data instead of failing — masking real
    path issues. Run this test from a tmp directory to confirm the loud
    failure path.
    """

    def test_resolver_raises_when_core_missing(self, tmp_path, monkeypatch):
        # Move the orgcontext package's __file__ into a directory tree that
        # has no sibling `core/` folder, then confirm _corpus_root() raises.
        from orgcontext import _corpus_root

        # Simulate "core/ not present at expected location" by patching the
        # candidate root the function will check. We use monkeypatch on
        # __file__ via the package's __init__ module — simpler: just point
        # Path(__file__).parent.parent at a location without core/.
        import orgcontext as _oc_pkg

        original_file = _oc_pkg.__file__
        fake_init = tmp_path / "orgcontext" / "__init__.py"
        fake_init.parent.mkdir(parents=True)
        fake_init.write_text("", encoding="utf-8")
        try:
            monkeypatch.setattr(_oc_pkg, "__file__", str(fake_init))
            with pytest.raises(RuntimeError, match="Could not locate OrgContext corpus root"):
                _corpus_root()
        finally:
            monkeypatch.setattr(_oc_pkg, "__file__", original_file)
