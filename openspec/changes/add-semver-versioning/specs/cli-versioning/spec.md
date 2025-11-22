# CLI Versioning

## ADDED Requirements

### Requirement: Version display option

The CLI MUST provide a version display option that shows the current installed version.

#### Scenario: User checks version with short flag

**Given** Cortext is installed
**When** the user runs `cortext -v`
**Then** the CLI prints the version in format `cortext {version}` (e.g., `cortext 0.2.0`)
**And** exits with code 0

#### Scenario: User checks version with long flag

**Given** Cortext is installed
**When** the user runs `cortext --version`
**Then** the CLI prints the version in format `cortext {version}`
**And** exits with code 0

### Requirement: Single source of truth for version

The version MUST be defined in a single location to prevent sync issues.

#### Scenario: Version is read from package metadata

**Given** the version is defined only in `pyproject.toml`
**When** the CLI displays the version
**Then** it reads the version from installed package metadata using `importlib.metadata`
**And** no `__version__` variables exist in source code

### Requirement: Automated version bumping

Version bumping MUST be automated on merge to main branch.

#### Scenario: Feature commit triggers minor bump

**Given** a PR is merged to main
**When** the commit message contains `feat:` or `feat(`
**Then** the GitHub Actions workflow bumps the minor version (e.g., 0.1.0 → 0.2.0)
**And** creates a git tag `v{new_version}`

#### Scenario: Fix commit triggers patch bump

**Given** a PR is merged to main
**When** the commit message contains `fix:` or `fix(`
**Then** the GitHub Actions workflow bumps the patch version (e.g., 0.1.0 → 0.1.1)
**And** creates a git tag `v{new_version}`

#### Scenario: Breaking change triggers major bump

**Given** a PR is merged to main
**When** the commit message contains `BREAKING CHANGE:` or `!:`
**Then** the GitHub Actions workflow bumps the major version (e.g., 0.1.0 → 1.0.0)
**And** creates a git tag `v{new_version}`
