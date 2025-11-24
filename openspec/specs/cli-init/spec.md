# cli-init Specification

## Purpose
TBD - created by archiving change fix-init-path-handling. Update Purpose after archive.
## Requirements
### Requirement: Init SHALL treat path-like arguments as filesystem paths
When the positional argument contains path characters (`.`, `..`, `/`, or starts with `~`), the init command SHALL interpret it as a filesystem path, not a workspace name to append to the home directory.

**ID:** `CLI-INIT-001` | **Priority:** High

#### Scenario: Current directory initialization
**Given** the user is in directory `/home/user/myproject`
**When** the user runs `cortext init .`
**Then** the workspace SHALL be initialized in `/home/user/myproject`
**And** NOT in `/home/user` or `/home/user/.`

#### Scenario: Parent directory initialization
**Given** the user is in directory `/home/user/myproject`
**When** the user runs `cortext init ..`
**Then** the workspace SHALL be initialized in `/home/user`

#### Scenario: Absolute path initialization
**Given** the user runs `cortext init /opt/workspace`
**When** the command executes
**Then** the workspace SHALL be initialized in `/opt/workspace`

#### Scenario: Home-relative path initialization
**Given** the user runs `cortext init ~/projects/mywork`
**When** the command executes
**Then** the workspace SHALL be initialized in the user's home directory under `projects/mywork`

---

### Requirement: Init SHALL preserve backward compatibility for simple names
When the positional argument is a simple name without path characters, the init command SHALL append it to the home directory to maintain backward compatibility.

**ID:** `CLI-INIT-002` | **Priority:** High

#### Scenario: Simple name creates home subdirectory
**Given** the user runs `cortext init my-workspace`
**When** the command executes
**Then** the workspace SHALL be initialized in `~/my-workspace`

#### Scenario: Name with hyphens still works
**Given** the user runs `cortext init ai-projects`
**When** the command executes
**Then** the workspace SHALL be initialized in `~/ai-projects`

---

### Requirement: Init SHALL prompt for location when no arguments provided
When no positional argument is provided and no `--path` option is specified, the init command SHALL interactively prompt the user to choose the workspace location.

**ID:** `CLI-INIT-003` | **Priority:** High

#### Scenario: Interactive prompt with options
**Given** the user runs `cortext init` with no arguments
**When** the command starts
**Then** the command SHALL prompt "Where would you like to create the workspace?"
**And** offer at least these options:
- Current directory (with current path shown)
- Default location (`~/ai-workspace`)
- Custom path (user input)

#### Scenario: User selects current directory
**Given** the user runs `cortext init` with no arguments
**And** the user is in `/home/user/myproject`
**When** the user selects "Current directory"
**Then** the workspace SHALL be initialized in `/home/user/myproject`

#### Scenario: User selects default location
**Given** the user runs `cortext init` with no arguments
**When** the user selects "Default location"
**Then** the workspace SHALL be initialized in `~/ai-workspace`

#### Scenario: User enters custom path
**Given** the user runs `cortext init` with no arguments
**When** the user selects "Custom path"
**And** enters `/opt/custom/workspace`
**Then** the workspace SHALL be initialized in `/opt/custom/workspace`

---

### Requirement: Init SHALL respect explicit --path option over positional argument
When both a positional argument and `--path` option are provided, the `--path` option SHALL take precedence.

**ID:** `CLI-INIT-004` | **Priority:** Medium

#### Scenario: Path option overrides positional argument
**Given** the user runs `cortext init myname --path /custom/location`
**When** the command executes
**Then** the workspace SHALL be initialized in `/custom/location`
**And** the positional argument `myname` SHALL be ignored

---

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

