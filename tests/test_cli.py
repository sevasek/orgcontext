"""Tests for the CLI entry point.

Covers the error-path contract: bad inputs should fail with a non-zero
exit code, and the empty-search guardrail should protect users from
accidentally dumping the entire corpus.
"""

from __future__ import annotations

import io
from contextlib import redirect_stderr, redirect_stdout

from orgcontext.cli import main as cli_main


def _run(argv: list[str]) -> tuple[int, str, str]:
    """Run the CLI with no-argparse-side-effects and return (rc, stdout, stderr)."""
    out = io.StringIO()
    err = io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        try:
            rc = cli_main(argv)
        except SystemExit as e:
            rc = e.code if e.code is not None else 0
    return rc if isinstance(rc, int) else 0, out.getvalue(), err.getvalue()


class TestCLIList:
    def test_list_default(self):
        rc, out, _ = _run(["list"])
        assert rc == 0
        assert "Total:" in out
        assert "okrs" in out

    def test_list_by_category(self):
        rc, out, _ = _run(["list", "--category", "governance"])
        assert rc == 0
        assert "raci" in out

    def test_list_empty_category(self):
        rc, out, _ = _run(["list", "--category", "no-such-thing"])
        assert rc == 0
        assert "No entries found" in out


class TestCLIGet:
    def test_get_existing_entry(self):
        rc, out, _ = _run(["get", "okrs"])
        assert rc == 0
        assert "OKRs" in out or "okrs" in out
        assert "Category: strategy-execution" in out

    def test_get_missing_entry_exits_nonzero(self):
        # Regression guard: the bare `except Exception` previously swallowed
        # KeyboardInterrupt; we now catch only (FileNotFoundError, ValueError).
        rc, out, err = _run(["get", "definitely-not-an-entry"])
        assert rc == 1
        assert "Error" in err
        assert "definitely-not-an-entry" in err

    def test_get_empty_id_exits_nonzero(self):
        # argparse rejects the missing positional at parse time, so this
        # surfaces as SystemExit(2) from argparse. Confirm we don't crash.
        rc, _, _ = _run(["get"])
        assert rc != 0


class TestCLISearch:
    def test_search_finds_known_term(self):
        rc, out, _ = _run(["search", "leadership"])
        assert rc == 0
        assert "servant-leadership" in out

    def test_search_no_matches(self):
        rc, out, _ = _run(["search", "xyzzy-no-match-expected"])
        assert rc == 0
        assert "No matches" in out

    def test_search_empty_query_blocked_by_default(self):
        # Empty query at the CLI must NOT silently dump every entry. The
        # guardrail asks the user to pass a term or opt in with --all.
        rc, out, err = _run(["search", ""])
        assert rc == 2
        assert "empty query" in err.lower() or "use --all" in err.lower()
        # stdout must be empty — the guardrail exits before printing results.
        assert "Found:" not in out

    def test_search_empty_query_with_all_flag(self):
        rc, out, _ = _run(["search", "", "--all"])
        assert rc == 0
        assert "Found: 34" in out or "Found: " in out  # corpus size may grow
        assert "okrs" in out
