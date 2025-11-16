# Spec Delta: Conversation Management

**Capability:** conversation-management
**Change ID:** refine-conversation-dating

---

## ADDED Requirements

### Requirement: Conversation Directory Structure SHALL use day-level granularity
The system MUST organize conversation directories by date with day-level granularity using the pattern `YYYY-MM-DD/###-type-topic/` to improve chronological navigation and organization.

**ID:** `CONV-001` | **Priority:** High

#### Scenario: Creating a new conversation

**Given** a user initializes a new conversation on November 10, 2025
**When** they run a conversation script (e.g., `brainstorm.sh "Topic"`)
**Then** a directory MUST be created at `conversations/2025-11-10/###-type-topic/`
**And** the conversation file MUST be placed inside that directory

**Example:**
```bash
# User runs on 2025-11-10
./scripts/bash/brainstorm.sh "New Feature Ideas"

# Creates:
conversations/2025-11-10/001-brainstorm-new-feature-ideas/brainstorm.md
```

#### Scenario: Multiple conversations on the same day

**Given** a user creates multiple conversations on the same day (2025-11-10)
**When** they run different conversation scripts throughout the day
**Then** all conversations for that day MUST be grouped in `conversations/2025-11-10/`
**And** each conversation MUST have a unique incrementing ID within that day's directory

**Example:**
```bash
# First conversation
conversations/2025-11-10/001-brainstorm-feature-a/

# Second conversation (same day)
conversations/2025-11-10/002-debug-auth-issue/

# Third conversation (same day)
conversations/2025-11-10/003-plan-refactoring/
```

#### Scenario: Conversations across multiple days

**Given** a user creates conversations on different days
**When** they create a conversation on November 10, then another on November 11
**Then** each day MUST have its own directory
**And** conversation IDs MAY restart from 001 in each new daily directory

**Example:**
```bash
conversations/2025-11-10/001-brainstorm-feature/
conversations/2025-11-11/001-debug-issue/  # ID can restart
```

---

### Requirement: Date Format Consistency - Scripts MUST use YYYY-MM-DD format
All conversation scripts SHALL use the `YYYY-MM-DD` date format consistently when creating conversation directories to ensure uniform temporal organization.

**ID:** `CONV-002` | **Priority:** High

#### Scenario: Bash script date generation

**Given** a conversation creation script is executed
**When** it generates the conversations directory path
**Then** it MUST use `date +%Y-%m-%d` command
**And** the resulting path MUST match pattern `conversations/YYYY-MM-DD/`

**Example:**
```bash
# In bash scripts
CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../conversations/$(date +%Y-%m-%d)"
# Results in: conversations/2025-11-10/
```

#### Scenario: Common utility function

**Given** the `get_current_conversation_dir()` function in `common.sh`
**When** it constructs the conversation directory path
**Then** it MUST use `$(date +%Y-%m-%d)` for the date portion
**And** the returned path MUST follow `conversations/YYYY-MM-DD/###-type-topic/` pattern

---

### Requirement: Backward Compatibility SHALL support mixed date formats
The system SHALL maintain backward compatibility by continuing to work with existing conversations in the old `YYYY-MM` format while creating all new conversations in the `YYYY-MM-DD` format.

**ID:** `CONV-003` | **Priority:** Medium

#### Scenario: Searching across both formats

**Given** a workspace contains conversations in both formats:
- `conversations/2025-11/001-brainstorm-feature/`
- `conversations/2025-11-10/001-debug-issue/`

**When** a user performs a workspace search
**Then** the search MUST find conversations in both directory formats
**And** results MUST be presented consistently regardless of format

#### Scenario: Workspace status with mixed formats

**Given** a workspace has conversations in old (`YYYY-MM`) and new (`YYYY-MM-DD`) formats
**When** the user runs `workspace-status.sh`
**Then** the script MUST count and display conversations from both formats
**And** the total count MUST be accurate across all formats

---

### Requirement: Status Display MUST show day-level information
The workspace status script SHALL provide enhanced temporal organization information by displaying day-level granularity in conversation counts and listings.

**ID:** `CONV-004` | **Priority:** Low

#### Scenario: Displaying current day's conversations

**Given** the user runs `workspace-status.sh` on 2025-11-10
**When** conversations exist for that date
**Then** the script SHOULD display "Today (2025-11-10): N conversations"
**And** it MAY also display month-level aggregates for context

#### Scenario: Displaying recent conversations

**Given** the user requests workspace status
**When** listing recent conversations
**Then** the display SHOULD show the date (YYYY-MM-DD) clearly for each conversation
**And** conversations SHOULD be sorted chronologically with most recent first

---

## Implementation Notes

### Affected Files

**Bash Scripts:**
- `scripts/bash/common.sh` - Core utility function
- `scripts/bash/brainstorm.sh` - Brainstorm conversations
- `scripts/bash/debug.sh` - Debug sessions
- `scripts/bash/plan.sh` - Planning sessions
- `scripts/bash/learn.sh` - Learning notes
- `scripts/bash/meeting.sh` - Meeting notes
- `scripts/bash/review.sh` - Review sessions
- `scripts/bash/workspace-status.sh` - Status display

**Change Pattern:**
```bash
# OLD:
CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../conversations/$(date +%Y-%m)"

# NEW:
CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../conversations/$(date +%Y-%m-%d)"
```

### Testing

**Manual Tests:**
1. Create conversation on specific date - verify directory is `YYYY-MM-DD`
2. Create multiple conversations same day - verify IDs increment
3. Create conversations across days - verify separate directories
4. Run status script - verify counts and display
5. Search old-format conversations - verify still found

**Edge Cases:**
- Conversation created at midnight (date boundary)
- First conversation of the day
- Last conversation of the month (month rollover)
- Workspace with only old-format conversations
- Workspace with only new-format conversations
- Mixed format workspace

---

## Migration Notes

**User Impact:**
- **Forward-only migration**: New conversations use new format
- **No data loss**: Old conversations remain accessible
- **No manual intervention required**: Change is transparent to users
- **Optional cleanup**: Users may manually reorganize old conversations if desired (not recommended)

**Future Enhancements:**
- Migration tool to convert old → new format (if users request)
- Configuration option to choose date granularity
- Support for custom date formats via configuration
