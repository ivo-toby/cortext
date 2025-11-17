# MCP Server Specification

**Capability:** `mcp-server`
**Version:** 1.0

---

## ADDED Requirements

### Requirement: Default conversation types SHALL be defined once
The MCP server SHALL define default conversation types in a single location (constant) to maintain a single source of truth and avoid duplication.

**ID:** `MCP-CONST-001` | **Priority:** Medium

#### Scenario: Constant definition
**Given** the MCP server needs default conversation types as fallback
**When** the registry is unavailable or cannot be read
**Then** a single constant (module or class level) SHALL provide the defaults
**And** the constant SHALL be named descriptively (e.g., `DEFAULT_CONVERSATION_TYPES`)
**And** all references SHALL use this constant with `.copy()` to avoid mutation

#### Scenario: Adding new default type
**Given** a developer needs to add a new default conversation type
**When** they modify the constant
**Then** only one location needs to be updated
**And** all fallback paths automatically use the new type

---

## Cross-References

- Related to conversation-management spec (conversation type definitions)
- Related to workspace-init spec (registry creation uses same types)
