"""Smoke tests for the integration packages.

These guard against the documented imports in the README going stale.
The integrations/ directory was previously missing __init__.py files
and was excluded from setuptools.packages.find, so the imports shown
in the README would fail. These tests confirm the path is wired up.
"""

from __future__ import annotations

import importlib

import pytest


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

    def test_openai_agents_module_imports(self):
        mod = importlib.import_module("orgcontext.integrations.openai_agents")
        assert hasattr(mod, "org_context_tool")
        assert hasattr(mod, "inject_system_prompt")

    def test_openai_agents_inject_system_prompt_returns_string(self):
        from orgcontext.integrations.openai_agents.tool import inject_system_prompt
        from pathlib import Path

        corpus_root = Path(__file__).parent.parent
        result = inject_system_prompt(["okrs"], corpus_root=corpus_root)
        assert isinstance(result, str)
        assert "ORGANIZATIONAL CONTEXT" in result
        assert len(result) > 50

    def test_openai_agents_tool_raises_without_package(self):
        """org_context_tool raises ImportError when openai-agents is not installed."""
        import sys
        import importlib

        # Temporarily hide the agents module if present so we can test the guard
        agents_mod = sys.modules.pop("agents", None)
        # Also reload the tool module with agents unavailable
        tool_mod_key = "orgcontext.integrations.openai_agents.tool"
        original_tool = sys.modules.pop(tool_mod_key, None)
        try:
            tool_mod = importlib.import_module(tool_mod_key)
            if not tool_mod.HAS_OPENAI_AGENTS:
                from pathlib import Path
                corpus_root = Path(__file__).parent.parent
                with pytest.raises(ImportError, match="openai-agents"):
                    tool_mod.org_context_tool(["okrs"], corpus_root=corpus_root)
            # If agents IS installed, just confirm the function is callable
            else:
                assert callable(tool_mod.org_context_tool)
        finally:
            # Restore original module state
            if agents_mod is not None:
                sys.modules["agents"] = agents_mod
            if original_tool is not None:
                sys.modules[tool_mod_key] = original_tool
