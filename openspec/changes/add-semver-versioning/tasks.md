# Tasks: Add SemVer Versioning

## Implementation Tasks

- [x] **Remove hardcoded versions from __init__.py files**
  - Remove `__version__` from `src/cortext_cli/__init__.py`
  - Remove `__version__` from `src/cortext_mcp/__init__.py`
  - Remove `__version__` from `src/cortext_rag/__init__.py`

- [x] **Add version callback to CLI**
  - Import `importlib.metadata` in `cli.py`
  - Create version callback function that prints `cortext {version}`
  - Add `-v/--version` option to typer app callback

- [x] **Create GitHub Actions workflow**
  - Create `.github/workflows/version-bump.yml`
  - Trigger on push to main branch
  - Parse commit messages for bump type (feat/fix/chore)
  - Use Python script or action to bump version in `pyproject.toml`
  - Commit and tag the new version
  - Configure to skip CI on version bump commits

- [x] **Test version display**
  - Verify `cortext -v` outputs correct version
  - Verify `cortext --version` works as alias
  - Verify version is read from package metadata

- [x] **Document versioning strategy**
  - Add section to README about version bumping
  - Document commit message conventions for version bumps

## Dependencies

- Tasks must be completed in order listed
- GitHub Actions workflow requires repository write permissions
