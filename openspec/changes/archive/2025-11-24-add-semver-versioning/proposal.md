# Proposal: Add SemVer Versioning

## Summary

Implement semantic versioning (SemVer) for Cortext with a single source of truth in `pyproject.toml`, a `cortext -v` CLI option to display version, and GitHub Actions automation to bump versions on merge to main.

## Motivation

Currently, Cortext has version `0.1.0` hardcoded in multiple files (`pyproject.toml` and three `__init__.py` files), but:
- No CLI option to check the installed version
- No automated version bumping on releases
- Version duplication creates sync issues

Users need to know which version they're running for bug reports and compatibility checks.

## Scope

**In scope:**
- Single source of truth: version in `pyproject.toml` only
- CLI `-v/--version` option using `importlib.metadata`
- GitHub Actions workflow to bump version on merge to main
- Remove hardcoded `__version__` from `__init__.py` files

**Out of scope:**
- Changelog generation
- Release notes automation
- PyPI publishing

## Approach

1. **Version source**: Use `importlib.metadata.version()` to read version at runtime from installed package metadata
2. **CLI option**: Add `--version` callback to typer app
3. **GitHub Actions**: Workflow triggered on push to main that:
   - Determines bump type from commit messages (feat=minor, fix=patch)
   - Updates version in `pyproject.toml`
   - Creates git tag and commits the change

## Success Criteria

- `cortext -v` prints version (e.g., `cortext 0.2.0`)
- `cortext --version` works as alias
- Version automatically increments on merge to main
- Single version definition in `pyproject.toml`
