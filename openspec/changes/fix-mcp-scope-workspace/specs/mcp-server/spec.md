## ADDED Requirements

### Requirement: MCP tools SHALL accept workspace_path as optional parameter

All MCP tools SHALL accept an optional `workspace_path` parameter that specifies the Cortext workspace root directory, defaulting to the current working directory when not provided.

**ID:** `MCP-ARGS-001` | **Priority:** High

#### Scenario: Tool called with explicit workspace_path
- **GIVEN** an MCP tool is called with `workspace_path` parameter
- **WHEN** the tool executes
- **THEN** the tool SHALL use the provided path as the workspace root
- **AND** SHALL search/operate within that directory

#### Scenario: Tool called without workspace_path
- **GIVEN** an MCP tool is called without `workspace_path` parameter
- **WHEN** the tool executes
- **THEN** the tool SHALL use the current working directory as workspace root

#### Scenario: search_workspace tool signature
- **GIVEN** the search_workspace tool schema
- **THEN** it SHALL include `workspace_path` as optional string parameter
- **AND** the description SHALL indicate it defaults to current directory

#### Scenario: get_context tool signature
- **GIVEN** the get_context tool schema
- **THEN** it SHALL include `workspace_path` as optional string parameter
- **AND** the description SHALL indicate it defaults to current directory

#### Scenario: get_decision_history tool signature
- **GIVEN** the get_decision_history tool schema
- **THEN** it SHALL include `workspace_path` as optional string parameter
- **AND** the description SHALL indicate it defaults to current directory

---

### Requirement: MCP server SHALL NOT require WORKSPACE_PATH environment variable

The MCP server SHALL operate without the `WORKSPACE_PATH` environment variable, relying instead on tool arguments or current working directory.

**ID:** `MCP-NOENV-001` | **Priority:** High

#### Scenario: Server starts without WORKSPACE_PATH
- **GIVEN** the MCP server is started without `WORKSPACE_PATH` environment variable
- **WHEN** tools are called
- **THEN** the server SHALL function correctly using tool arguments or cwd

#### Scenario: Backward compatibility with WORKSPACE_PATH
- **GIVEN** the MCP server is started with `WORKSPACE_PATH` environment variable set
- **WHEN** tools are called without explicit workspace_path
- **THEN** the server MAY use WORKSPACE_PATH as fallback before cwd
- **AND** explicit tool arguments SHALL take precedence

---
