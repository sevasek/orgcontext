"""Smoke tests for the integration packages.

These guard against the documented imports in the README going stale.
The integrations/ directory was previously missing __init__.py files
and was excluded from setuptools.packages.find, so the imports shown
in the README would fail. These tests confirm the path is wired up.
"""

from __future__ import annotations

import importlib


class TestIntegrationImports:
    def test_integrations_package_imports(self):
        # The parent package must import without triggering the optional
        # dependencies (langgraph, crewai-tools) to load.
        mod = importlib.import_module("orgcontext.integrations")
        assert mod is not None

    def test_langgraph_module_imports(self):
        # Importing the module body should not require langgraph to be
        # installed — only constructing OrgContextNode does.
        mod = importlib.import_module("orgcontext.integrations.langgraph")
        assert hasattr(mod, "OrgContextNode")
        assert hasattr(mod, "inject_state")

    def test_crewai_module_imports(self):
        mod = importlib.import_module("orgcontext.integrations.crewai")
        assert hasattr(mod, "org_context_tool")
        assert hasattr(mod, "inject_agent_context")
