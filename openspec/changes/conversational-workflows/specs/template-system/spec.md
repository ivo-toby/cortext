# Spec Delta: Template System

**Capability:** template-system
**Change ID:** conversational-workflows

---

## ADDED Requirements

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

## Notes

[Document your learning here as conversation progresses]

---

## References

[Add resources and links]
```

**Anti-pattern (too prescriptive):**
```markdown
## Key Concepts

### Concept 1: [Name]
**Definition:** [What is it?]
**Explanation:** [How does it work?]
**Why It Matters:** [Significance]

[...20 more prescriptive sections]  ❌
```

#### Scenario: Brainstorm template supports free-form ideation

**Given** a brainstorm conversation is created
**When** the template is initialized
**Then** it MUST have open-ended sections for ideas
**And** it MUST NOT prescribe specific idea fields
**And** it MUST allow flexible organization
**And** it MUST be less than 50 lines

**Example:**
```markdown
# Brainstorm: [TOPIC]

**Date**: [DATE]

---

## Goals

[What are we exploring?]

---

## Ideas

[Capture ideas as they emerge]

---

## Themes

[Patterns and connections]

---

## Next Steps

[Promising directions]
```

---

### Requirement: Templates MUST support organic content growth
Templates SHALL enable content to emerge from conversation rather than fitting into predefined structures.

**ID:** `TMPL-MIN-002` | **Priority:** High

#### Scenario: Template allows custom sections

**Given** a conversation document is being updated
**When** Claude needs to add a new type of content
**Then** Claude MUST be able to add custom sections freely
**And** Template MUST NOT restrict to predefined sections only
**And** Document structure MUST adapt to conversation needs

**Example:**
```markdown
# Learning Notes: Kubernetes Networking

## Notes

### Pod-to-Pod Communication
[Explained during conversation]

### Services and Load Balancing
[Added when topic came up]

### Network Policies
[User asked about this, so we added section]

### Troubleshooting Common Issues
[Emerged from debugging discussion]

[New sections added organically as conversation flowed]
```

#### Scenario: Debug template adapts to investigation

**Given** a debug conversation is documenting an issue
**When** the investigation takes unexpected turns
**Then** document structure MUST adapt
**And** Template MUST NOT force rigid problem/solution format
**And** New sections MUST be addable as investigation proceeds

---

### Requirement: Templates MUST minimize prescribed structure
Templates SHALL contain maximum 6 main sections and no nested subsection templates.

**ID:** `TMPL-MIN-003` | **Priority:** Medium

#### Scenario: Template has minimal sections

**Given** any conversation template is created
**When** the template is reviewed
**Then** it MUST have no more than 6 main sections
**And** it MUST NOT include nested subsection templates
**And** Sections MUST be broad and flexible
**And** No section should prescribe specific fields to fill

**Current violations:**
- `learning-notes.md`: 20+ sections with nested fields ❌
- Multiple templates with subsection templates ❌

**Compliant structure:**
```markdown
# [Type]: [Topic]
[Metadata]
---
## [Section 1]
## [Section 2]
## [Section 3]
## [Optional: Section 4-6]
---
[Metadata footer]
```

Maximum sections examples:
- **Learn**: Title, Notes, References (3)
- **Brainstorm**: Title, Goals, Ideas, Themes, Next Steps (5)
- **Debug**: Title, Problem, Investigation, Solution (4)
- **Plan**: Title, Goals, Approach, Tasks (4)

---

### Requirement: Templates MUST use placeholder text not field prompts
Templates SHALL use neutral placeholders that don't impose structure on content.

**ID:** `TMPL-MIN-004` | **Priority:** Low

#### Scenario: Template uses simple placeholders

**Given** a template contains placeholder text
**When** the placeholder is for content areas
**Then** it MUST be generic and non-prescriptive
**And** it MUST NOT ask specific questions
**And** it MUST NOT define required information

**Good placeholders:**
```markdown
## Notes
[Document insights here]

## References
[Add links and resources]
```

**Bad placeholders (too prescriptive):**
```markdown
## Key Concepts
**Definition:** [What is it?]  ❌
**Explanation:** [How does it work?]  ❌
**Why It Matters:** [Significance and use cases]  ❌
```

---

## Implementation Notes

### Template Simplification Guidelines

When simplifying templates:

1. **Keep only essential sections**
   - What is this? (Title/Topic)
   - What did we learn/discuss? (Notes/Content)
   - What are the sources? (References)

2. **Remove all prescriptive subsections**
   - No "Definition:", "Explanation:", "Example:" templates
   - No nested field structures
   - No questionnaire-style prompts

3. **Use open-ended section headers**
   - "Notes" not "Key Concepts with Definitions"
   - "Ideas" not "Idea 1, Idea 2, Idea 3"
   - "Investigation" not "Steps Taken, Results, Analysis"

4. **Maximize white space**
   - Let content breathe
   - Don't fill with template text
   - Provide room for organic growth

### Before/After Examples

**Before (learning-notes.md, 248 lines):**
```markdown
## Key Concepts
### Concept 1: [Name]
**Definition:** [What is it?]
**Explanation:** [How does it work?]
**Why It Matters:** [Significance and use cases]
**Example:**
```
[Code example or illustration]
```

[...continues for 200+ more lines]
```

**After (learning-notes.md, ~30 lines):**
```markdown
# Learning Notes: [TOPIC]

**ID**: [ID]
**Date**: [DATE]
**Status**: In Progress

---

## Notes

[Document your learning here]

---

## Examples

[Add code examples if relevant]

---

## References

[Add resources and links]

---

**Metadata**
- Created: [DATE]
- Tags: learning, [topic]
```

### Template Philosophy

**Old**: "Provide comprehensive structure so users capture everything"
- Assumes users need detailed guidance
- Imposes organization from start
- Feels like a form to fill

**New**: "Provide minimal scaffold so conversation can flow naturally"
- Trusts conversation to generate structure
- Enables organic organization
- Feels like a canvas to paint

---

## Testing

**Template Validation:**
1. Check all templates are <50 lines
2. Verify no nested subsection templates exist
3. Ensure no prescriptive field structures
4. Confirm placeholders are generic
5. Verify flexibility for custom sections

**Conversation Validation:**
1. Use template in actual conversation
2. Verify easy to add custom sections
3. Check doesn't feel constraining
4. Confirm supports organic content flow

---

## Migration

**Existing workspaces:**
- Old verbose templates still work
- Users can manually simplify if desired
- No automatic template updates

**New workspaces:**
- All templates use minimal design
- Better conversation experience from start

**Custom types:**
- Not affected unless user regenerates
- `workspace_add.md` updated to generate minimal templates
