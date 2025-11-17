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

