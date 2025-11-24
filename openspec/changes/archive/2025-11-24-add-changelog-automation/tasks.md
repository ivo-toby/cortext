# Tasks: Add Changelog Automation

## Implementation Tasks

- [x] **Add changelog generation step to workflow**
  - Collect commits since last tag using `git log`
  - Filter for feat/fix/docs prefixes
  - Parse commit messages to extract summaries

- [x] **Create changelog entry formatter**
  - Categorize commits into Added/Fixed/Changed sections
  - Format as bullet points with proper indentation
  - Generate version header with date

- [x] **Insert new section into CHANGELOG.md**
  - Find `## [Unreleased]` marker
  - Insert new version section below it
  - Preserve existing content

- [x] **Update commit step to include CHANGELOG.md**
  - Add CHANGELOG.md to git staging
  - Include in version bump commit

- [x] **Test changelog generation**
  - Verify entries are correctly categorized
  - Verify date format is correct
  - Verify existing content is preserved

## Dependencies

- Requires existing version-bump workflow
- Tasks are sequential
