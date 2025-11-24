## ADDED Requirements

### Requirement: Init SHALL check for existing MCP installation before prompting
The init command SHALL check if Cortext MCP is already registered with the agent before prompting the user to install it. Since MCP registration is global, there is no need to re-register for each workspace.

**ID:** `CLI-INIT-010` | **Priority:** High

#### Scenario: MCP already installed for Claude
- **WHEN** init runs and Cortext MCP is already registered with Claude Code
- **THEN** the MCP registration prompt SHALL be skipped
- **AND** a message SHALL inform the user that MCP is already configured
- **AND** no registration attempt SHALL be made

#### Scenario: MCP not installed for Claude
- **WHEN** init runs and Cortext MCP is not registered with Claude Code
- **THEN** the user SHALL be prompted to install MCP
- **AND** if user confirms, registration SHALL proceed with progress feedback

#### Scenario: MCP check for other agents
- **WHEN** init checks MCP status for Gemini or OpenCode
- **THEN** the existing configuration files SHALL be checked
- **AND** registration SHALL be skipped if already configured

---

### Requirement: Init SHALL display progress feedback during slow operations
The init command SHALL provide visual progress feedback when performing operations that may take more than 1 second, such as MCP server registration.

**ID:** `CLI-INIT-006` | **Priority:** High

#### Scenario: Progress feedback during MCP registration
- **WHEN** init registers MCP server with Claude Code
- **THEN** a spinner or status indicator SHALL be displayed
- **AND** the indicator SHALL show descriptive text (e.g., "Registering MCP server with Claude Code...")
- **AND** the indicator SHALL disappear when the operation completes

#### Scenario: Progress feedback during git operations
- **WHEN** init performs git commit operations
- **THEN** a status indicator MAY be displayed for operations taking more than 1 second

---

### Requirement: Init SHALL use reasonable timeouts for subprocess operations
The init command SHALL use appropriate timeout values for subprocess operations to balance reliability with responsiveness.

**ID:** `CLI-INIT-007` | **Priority:** Medium

#### Scenario: MCP registration timeout
- **WHEN** init calls `claude mcp add` to register the MCP server
- **THEN** the timeout SHALL be 10 seconds
- **AND** if timeout occurs, a clear error message SHALL explain the issue
- **AND** the error message SHALL provide the manual command to run

#### Scenario: Command availability check timeout
- **WHEN** init checks for `cortext-mcp` command availability
- **THEN** the timeout SHALL be 5 seconds

---

### Requirement: Init SHALL support quick mode for fast initialization
The init command SHALL support a `--quick` flag that skips optional time-consuming operations for faster initialization in scripts and CI.

**ID:** `CLI-INIT-008` | **Priority:** Medium

#### Scenario: Quick mode skips MCP registration prompt
- **GIVEN** user runs `cortext init --quick`
- **WHEN** the initialization runs
- **THEN** MCP registration SHALL be skipped by default
- **AND** no interactive prompts SHALL be displayed
- **AND** a message SHALL inform the user how to configure MCP later

#### Scenario: Quick mode with explicit MCP flag
- **GIVEN** user runs `cortext init --quick --mcp`
- **WHEN** the initialization runs
- **THEN** MCP registration SHALL be attempted without prompting
- **AND** progress feedback SHALL still be displayed

#### Scenario: Normal mode unchanged
- **GIVEN** user runs `cortext init` without `--quick`
- **WHEN** the initialization runs
- **THEN** interactive prompts SHALL be displayed as before
- **AND** MCP registration SHALL be attempted by default

---

### Requirement: Init SHALL cache expensive command checks
The init command SHALL cache the results of expensive command availability checks within a single init run.

**ID:** `CLI-INIT-009` | **Priority:** Low

#### Scenario: Single check for cortext-mcp availability
- **WHEN** init checks for `cortext-mcp` availability
- **THEN** the check SHALL be performed once
- **AND** the result SHALL be reused for all agents during that init run
