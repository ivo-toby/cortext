# changelog-automation Specification

## Purpose
TBD - created by archiving change add-changelog-automation. Update Purpose after archive.
## Requirements
### Requirement: Automatic changelog generation on version bump

The version-bump workflow MUST automatically generate changelog entries from conventional commits when bumping the version.

#### Scenario: Feature commits added to changelog

**Given** commits exist since the last version tag
**When** the version bump workflow runs
**And** a commit message starts with `feat:` or `feat(`
**Then** the commit summary is added to the "Added" section of the new changelog entry

#### Scenario: Fix commits added to changelog

**Given** commits exist since the last version tag
**When** the version bump workflow runs
**And** a commit message starts with `fix:` or `fix(`
**Then** the commit summary is added to the "Fixed" section of the new changelog entry

#### Scenario: Docs commits added to changelog

**Given** commits exist since the last version tag
**When** the version bump workflow runs
**And** a commit message starts with `docs:` or `docs(`
**Then** the commit summary is added to the "Changed" section of the new changelog entry

#### Scenario: Other commits excluded from changelog

**Given** commits exist since the last version tag
**When** the version bump workflow runs
**And** a commit message starts with `chore:`, `refactor:`, `test:`, or `ci:`
**Then** the commit is not included in the changelog entry

### Requirement: Keep a Changelog format compliance

The generated changelog entries MUST follow the Keep a Changelog format.

#### Scenario: Version section header format

**Given** a new version is being released
**When** the changelog entry is generated
**Then** the section header follows format `## [version] - YYYY-MM-DD`
**And** the date is the current date in ISO format

#### Scenario: Category sections format

**Given** commits of multiple types exist
**When** the changelog entry is generated
**Then** categories appear as `### Added`, `### Fixed`, `### Changed`
**And** each commit appears as a bullet point under its category
**And** empty categories are omitted

### Requirement: Changelog file preservation

The workflow MUST preserve existing changelog content when inserting new entries.

#### Scenario: New entry inserted after Unreleased section

**Given** CHANGELOG.md contains an `## [Unreleased]` section
**When** the changelog entry is generated
**Then** the new version section is inserted after the Unreleased section
**And** all existing content below is preserved

#### Scenario: Changelog included in version commit

**Given** a changelog entry has been generated
**When** the version bump commit is created
**Then** CHANGELOG.md is included in the commit
**And** the commit message mentions the version bump

