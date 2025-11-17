# CLI Init Specification

**Capability:** `cli-init`
**Version:** 1.1

---

## ADDED Requirements

### Requirement: Each AI tool SHALL be configurable independently
The init command SHALL configure each AI tool independently without requiring other tools to be configured first. Each tool SHALL convert directly from source command templates.

**ID:** `CLI-INIT-005` | **Priority:** High

#### Scenario: Configure only Gemini
**Given** user runs `cortext init --ai=gemini`
**When** the initialization completes
**Then** the `.gemini/commands/` folder SHALL be created
**And** Gemini TOML command files SHALL be generated
**And** NO `.claude/` folder SHALL be created
**And** configuration SHALL NOT depend on Claude being configured first

#### Scenario: Configure only OpenCode
**Given** user runs `cortext init --ai=opencode`
**When** the initialization completes
**Then** the `.opencode/` folder SHALL be created
**And** configuration SHALL NOT depend on other tools

#### Scenario: Configure all tools
**Given** user runs `cortext init --ai=all`
**When** the initialization completes
**Then** all AI tool folders SHALL be created
**And** each tool SHALL be configured independently

---

## Cross-References

- Related to workspace-init spec (workspace structure)
- Modifies existing CLI-INIT requirements for AI tool configuration
