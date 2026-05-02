#!/usr/bin/env python3
"""
Set up GitHub labels for the OrgContext repository.
Uses the `gh` CLI. Run from the repo root.

Usage:
    python scripts/setup_labels.py
"""

import subprocess
import sys

LABELS = [
    # Category
    ("entry:new", "0e8a16", "Create a new OrgContext entry"),
    ("entry:fix", "fbca04", "Edit or improve an existing entry"),
    ("tooling", "1d76db", "Python code, scripts, integrations"),
    ("docs", "5319e7", "README, guides, templates"),
    ("infra", "e99695", "CI, repo config, project setup"),
    # Status
    ("status:ready", "0e8a16", "Scoped and ready to be claimed"),
    ("status:blocked", "d73a4a", "Agent cannot proceed, needs input"),
    ("needs-decision", "fbca04", "Ambiguity requires coordinator decision"),
    # Priority
    ("priority:0", "b60205", "Critical — blocks other work"),
    ("priority:1", "d93f0b", "Important — should be done soon"),
    ("priority:2", "fbca04", "Nice to have"),
    ("priority:3", "fef2c0", "Someday — no urgency"),
    # Special
    ("good-first-task", "7057ff", "Simple task for new agents"),
]


def run(cmd: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def main() -> None:
    # Check gh is available
    rc, _, _ = run(["gh", "--version"])
    if rc != 0:
        print("Error: `gh` CLI not found. Install from https://cli.github.com/")
        sys.exit(1)

    # Check authenticated
    rc, out, err = run(["gh", "auth", "status"])
    if rc != 0:
        print("Error: not authenticated with gh. Run `gh auth login`.")
        print(err)
        sys.exit(1)

    created = 0
    skipped = 0

    for name, color, desc in LABELS:
        rc, out, err = run(["gh", "label", "list", "--search", name, "--limit", "1"])
        if name in out:
            print(f"  ⏭  {name} — already exists")
            skipped += 1
            continue

        rc, _, _ = run([
            "gh", "label", "create", name,
            "--color", color,
            "--description", desc,
        ])
        if rc == 0:
            print(f"  ✅ {name} — created")
            created += 1
        else:
            print(f"  ❌ {name} — failed")

    print(f"\nDone. Created {created}, skipped {skipped}, total {len(LABELS)}.")


if __name__ == "__main__":
    main()
