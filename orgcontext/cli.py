"""Basic CLI for OrgContext.

Usage examples:
    orgcontext list
    orgcontext list --category governance
    orgcontext get okrs
    orgcontext search "leadership"
"""

from __future__ import annotations

import argparse
import sys

import orgcontext as oc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="orgcontext",
        description="OrgContext - LLM-native organizational context dictionary",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    list_parser = subparsers.add_parser("list", help="List available entries")
    list_parser.add_argument("--category", "-c", help="Filter by category (e.g. governance)")

    # get
    get_parser = subparsers.add_parser("get", help="Load and print a specific entry")
    get_parser.add_argument("id", help="Entry ID (e.g. okrs, servant-leadership)")

    # search
    search_parser = subparsers.add_parser("search", help="Search entries by keyword")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument(
        "--all",
        action="store_true",
        help="Return every entry (skip the empty-query guardrail). The Python "
        "API returns all entries for an empty query, but the CLI treats "
        "an empty query as a likely mistake.",
    )

    args = parser.parse_args(argv)

    if args.command == "list":
        entries = oc.list_entries(category=args.category)
        if not entries:
            print("No entries found.")
            return 0
        for e in entries:
            print(f"{e['id']}: {e['title']} ({e['category']})")
        print(f"\nTotal: {len(entries)}")
        return 0

    elif args.command == "get":
        try:
            entry = oc.load(args.id)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        print(f"# {entry.title}\n")
        print(f"Category: {entry.category}")
        print(f"Authors: {', '.join(entry.authors) if entry.authors else 'unknown'}")
        print(f"Last updated: {entry.last_updated}")
        if entry.deprecated:
            print("**DEPRECATED**")
        print("\n" + entry.prompt_snippet)
        return 0

    elif args.command == "search":
        if not args.query and not args.all:
            print(
                "Error: empty query would return every entry. "
                "Pass a search term, or use --all to list everything.",
                file=sys.stderr,
            )
            return 2
        # --all is "list everything" — route to list_entries() directly
        # rather than search_entries(""), which deliberately returns []
        # for empty queries (and would print "No matches" here).
        if args.all:
            results = oc.list_entries()
        else:
            results = oc.search_entries(args.query)
        if not results:
            print(f"No matches for '{args.query}'")
            return 0
        for e in results:
            print(f"{e['id']}: {e['title']} ({e['category']})")
        print(f"\nFound: {len(results)}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
