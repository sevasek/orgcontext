"""Tests for orgcontext core package."""

from pathlib import Path

import pytest

from orgcontext import OrgContextEntry, inject, list_entries, load


CORPUS_ROOT = Path(__file__).parent.parent / "core"


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
        assert entry.last_updated == "2026-04-27"


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
        assert len(entries) == 17
        ids = [e["id"] for e in entries]
        assert "servant-leadership" in ids
        assert "okrs" in ids
        assert "raci" in ids

    def test_list_entries_by_category(self):
        entries = list_entries(category="governance", corpus_root=CORPUS_ROOT.parent)
        assert len(entries) == 3
        ids = [e["id"] for e in entries]
        assert "raci" in ids
        assert "decision-rights" in ids
        assert "escalation-path" in ids

    def test_list_entries_each_has_required_keys(self):
        entries = list_entries(corpus_root=CORPUS_ROOT.parent)
        for entry in entries:
            assert "id" in entry
            assert "title" in entry
            assert "category" in entry
            assert "tags" in entry
            assert "path" in entry

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
        assert entry.raw_markdown == ""


class TestAllEntriesValid:
    def test_all_core_entries_loadable(self):
        entries = list_entries(corpus_root=CORPUS_ROOT.parent)
        for entry_meta in entries:
            entry = load(entry_meta["id"], corpus_root=CORPUS_ROOT.parent)
            assert entry.id == entry_meta["id"]
            assert entry.prompt_snippet, f"Entry {entry_meta['id']} has empty prompt_snippet"
            assert entry.definition, f"Entry {entry_meta['id']} has empty definition"
