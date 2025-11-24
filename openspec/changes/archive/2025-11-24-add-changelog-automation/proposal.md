# Proposal: Add Changelog Automation

## Summary

Extend the version-bump GitHub Actions workflow to automatically generate changelog entries from conventional commit messages when releasing a new version.

## Motivation

Currently, the CHANGELOG.md must be manually updated before releases. This is:
- Time-consuming and error-prone
- Easy to forget or miss commits
- Inconsistent in formatting

Automating changelog generation ensures every release has accurate, consistent documentation of changes.

## Scope

**In scope:**
- Parse commits since last tag for feat/fix/docs prefixes
- Generate Keep a Changelog formatted entries
- Insert new version section at top of CHANGELOG.md
- Include in the version bump commit

**Out of scope:**
- GitHub Releases creation
- Release notes beyond CHANGELOG.md
- Breaking change detection from commit body

## Approach

1. **Collect commits**: Get all commits between previous tag and HEAD
2. **Filter commits**: Include only `feat:`, `fix:`, and `docs:` prefixed commits
3. **Categorize**: Map to Keep a Changelog sections:
   - `feat:` → Added
   - `fix:` → Fixed
   - `docs:` → Changed
4. **Format entries**: Extract commit message summary as bullet point
5. **Generate section**: Create `## [version] - YYYY-MM-DD` section
6. **Update file**: Insert new section after `## [Unreleased]` header
7. **Commit together**: Include CHANGELOG.md in version bump commit

## Success Criteria

- CHANGELOG.md updated automatically on version bump
- Entries correctly categorized under Added/Fixed/Changed
- Date format matches Keep a Changelog (`YYYY-MM-DD`)
- Existing changelog content preserved
