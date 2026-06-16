"""Tests for scripts/build_index.py frontmatter parsing.

The script is run from the repo root and depends on the package being
importable; these tests exercise only the parse_frontmatter helper, which
is the one piece of logic that silently dropped data on the previous
standalone parser.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


def _load_build_index():
    """Load build_index.py as a module so we can call parse_frontmatter().

    The script does `sys.path.insert(0, str(REPO_ROOT))` and then imports
    the package, so we replicate that setup here.
    """
    repo_root = Path(__file__).parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    spec = importlib.util.spec_from_file_location("build_index", SCRIPTS_DIR / "build_index.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def build_index_module():
    return _load_build_index()


class TestParseFrontmatter:
    def test_inline_list_preserved(self, build_index_module):
        fm = build_index_module.parse_frontmatter("---\nid: test\ntags: [a, b, c]\n---\n")
        assert fm["id"] == "test"
        assert fm["tags"] == ["a", "b", "c"]

    def test_multiline_list_preserved(self, build_index_module):
        # This is the regression: the previous standalone parser dropped
        # multi-line lists entirely. All three new industry entries use
        # multi-line `references:` blocks.
        fm = build_index_module.parse_frontmatter(
            "---\nid: test\nreferences:\n  - 'ref one'\n  - 'ref two'\n---\n"
        )
        assert fm["references"] == ["ref one", "ref two"]

    def test_mixed_list_shapes(self, build_index_module):
        # Inline + multi-line in the same frontmatter block.
        fm = build_index_module.parse_frontmatter(
            "---\n"
            "id: mixed\n"
            "tags: [inline]\n"
            "authors:\n  - 'Author One'\n  - 'Author Two'\n"
            "version: 1.0.0\n"
            "---\n"
        )
        assert fm["id"] == "mixed"
        assert fm["tags"] == ["inline"]
        assert fm["authors"] == ["Author One", "Author Two"]
        assert fm["version"] == "1.0.0"

    def test_real_industry_entry_parses_references(self, build_index_module):
        # Sanity check against an actual corpus file that uses multi-line
        # references — if the parser regresses, this would catch it.
        repo_root = Path(__file__).parent.parent
        path = repo_root / "core" / "industry" / "tech-startup" / "product-market-fit.md"
        content = path.read_text(encoding="utf-8")
        fm = build_index_module.parse_frontmatter(content)
        assert isinstance(fm.get("references"), list)
        assert len(fm["references"]) >= 1
        assert any("Andreessen" in r for r in fm["references"])
