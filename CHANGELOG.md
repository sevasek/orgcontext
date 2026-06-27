# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] — 2026-06-22

### Added
- OpenAI Agents SDK integration (`orgcontext.integrations.openai_agents`)
- MCP server support via `orgcontext-mcp` CLI entry point
- Industry corpus packs: `tech-startup`, `enterprise`, `nonprofit` sectors
- `search_entries()` public API function with keyword search across title, tags, and authors
- `get_frontmatter()` public API function for lightweight metadata access
- `list_entries()` category filter parameter
- CI workflow running pytest across Python 3.9–3.12 on every push and PR
- Automated PyPI publish workflow triggered by version tags (`v*.*.*`)
- Cross-reference integrity check in `validate_entry.py --all` for `related` links

### Changed
- `load()` and `get_frontmatter()` now strip whitespace from `entry_id`
- Test suite covers industry-pack categories and uses `>= N` entry count assertions

### Fixed
- `get_frontmatter()` error type made consistent with `load()` (`FileNotFoundError`)

## [0.1.0] — 2026-04-28

### Added
- Initial public release
- 31 core entries across governance, leadership frameworks, mission-vision, roles-responsibilities, culture-values, and strategy-execution
- `load()`, `inject()`, `list_entries()` public API
- `OrgContextEntry` dataclass with `prompt_snippet`, `to_dict()`, `sections`
- CLI: `orgcontext list`, `orgcontext get`
- Entry validation script (`scripts/validate_entry.py`)
- Index builder (`scripts/build_index.py`)
- YAML frontmatter spec with semver versioning per entry

[Unreleased]: https://github.com/sevasek/orgcontext/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/sevasek/orgcontext/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/sevasek/orgcontext/releases/tag/v0.1.0
