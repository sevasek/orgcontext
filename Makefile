# OrgContext development shortcuts
# Usage: make test, make validate, make index, make cli, etc.

.PHONY: help test validate index cli clean install

help:
	@echo "OrgContext dev commands:"
	@echo "  make test       Run pytest"
	@echo "  make validate   Run entry validation on all entries"
	@echo "  make index      Rebuild docs/index.md"
	@echo "  make cli        Demo the CLI (list + get)"
	@echo "  make install    Install in editable mode with dev deps"
	@echo "  make clean      Remove __pycache__ and egg-info"

test:
	python -m pytest -q

validate:
	python scripts/validate_entry.py --all

index:
	python scripts/build_index.py

cli:
	python -m orgcontext.cli list --category governance
	@echo ""
	python -m orgcontext.cli get okrs | head -20

install:
	pip install -e ".[dev,mcp,yaml]"

clean:
	rm -rf __pycache__ orgcontext/__pycache__ tests/__pycache__ *.egg-info orgcontext.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
