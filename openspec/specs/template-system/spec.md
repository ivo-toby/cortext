# template-system Specification

## Purpose
TBD - created by archiving change conversational-workflows. Update Purpose after archive.
## Requirements
### Requirement: Templates SHALL be minimal scaffolding not prescriptive forms
Conversation templates MUST provide basic structure without dictating specific fields or content organization.

**ID:** `TMPL-MIN-001` | **Priority:** High

#### Scenario: Learning template is minimal

**Given** a new workspace is initialized
**When** `templates/learning-notes.md` is created
**Then** the template MUST be less than 50 lines
**And** it MUST contain only essential sections (Title, Notes, References)
**And** it MUST NOT prescribe specific sub-fields
**And** it MUST allow organic content structure

**Example (minimal template):**
```markdown
# Learning Notes: [TOPIC]

**ID**: [ID]
**Date**: [DATE]
**Status**: In Progress

---

