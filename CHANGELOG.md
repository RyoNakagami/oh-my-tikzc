# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.1.0] - 2026-10-25

### Added

- `tikzc-architecture` skill that documents a repository as a `.omtkc/` tree of
  architectural perspectives and components, with editable TikZ diagrams
  rendered by tikzc, source evidence, and recursive drill-down.
- Bundled checker `omtkc.py` (`check`, `tree`, `stale`) that validates
  structure, links, sources, refs, and render freshness, and finds components
  whose sources changed since the last analysis. Runs with uv (PEP 723 inline
  metadata) or plain `python3` with a built-in YAML subset parser.
- Plugin marketplace manifests for Claude Code (`.claude-plugin/`) and Codex
  (`.codex-plugin/`), plus Codex UI metadata in `agents/openai.yaml`.
- Example output for tikzc v1.2.1 under `examples/tikzc/.omtkc/`.
- English and Japanese README, getting-started, and how-it-works guides with
  diagrams.
- Checker unit tests.
- GitHub Actions workflows for label management and tagged releases.
- MIT license with NOTICE attributing the workflow adapted from oh-my-mermaid.
