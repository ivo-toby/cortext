# conversation-types Specification Delta

## ADDED Requirements

### Requirement: System SHALL provide a projectmanage conversation type with multi-document architecture

The system SHALL include a built-in `projectmanage` conversation type that enables AI assistants to act as project management partners, helping users capture ideas, track tasks and status, define goals and roadmaps, manage project documentation across multiple files, and maintain portfolio-level overview. The type SHALL support creating multiple documents organized in subfolders by type.

**ID:** `CONV-TYPE-001` | **Priority:** High

#### Scenario: Creating a new project management conversation

**Given** a user runs `/workspace.projectmanage` command
**When** they specify a project name (e.g., "Cortext Development")
**Then** a conversation directory MUST be created at `projectmanage/YYYY-MM-DD/###-projectmanage-<slug>/`
**And** the directory MUST contain a master `project-management.md` file
**And** the directory MUST contain an `index.md` file for document tracking
**And** the directory MUST contain a `docs/` subfolder for additional documents
**And** a git commit MUST be created with the conversation initialization
**And** a conversation tag MUST be created

**Example:**
```bash
# User runs on 2025-11-20
/workspace.projectmanage
Claude: "What project are you managing?"
User: "Cortext Development"

# Creates:
projectmanage/2025-11-20/001-projectmanage-cortext-development/
├── project-management.md    # Master status document
├── index.md                 # Document index
└── docs/                    # Subfolder for project documents
```

#### Scenario: Agent creates multiple documents with flexible categorization

**Given** a projectmanage conversation is active
**When** the user shares information that should be documented
**Then** Claude MUST categorize the content appropriately
**And** Claude MUST create a new document in the appropriate `docs/` subfolder
**And** Claude MUST use a descriptive filename based on content
**And** Claude MUST update `index.md` to include the new document

**Example Interactions:**
```
User: "We decided to use PostgreSQL for the database"
Claude: *Creates docs/decisions/database-selection.md*
        *Updates index.md*
        "I've documented that decision in docs/decisions/database-selection.md.
        Should I capture the reasoning behind choosing PostgreSQL?"

User: "Here are the requirements for user authentication"
Claude: *Creates docs/requirements/user-authentication.md*
        *Updates index.md*
        "I've created the authentication requirements document.
        Let me know if you want to add acceptance criteria."
```

#### Scenario: Projectmanage type appears in search filters

**Given** a workspace has projectmanage conversations
**When** a user searches with `type: "projectmanage"` filter
**Then** the search MUST return only projectmanage conversations
**And** the projectmanage type MUST be listed as a valid filter option

---

### Requirement: Agent SHALL proactively search workspace for relevant context

The AI assistant in projectmanage conversations SHALL actively use MCP search tools to find and surface relevant existing data from the workspace when discussing topics with the user.

**ID:** `CONV-TYPE-002` | **Priority:** High

#### Scenario: Agent searches for context when discussing topics

**Given** a projectmanage conversation is active
**When** the user mentions a topic or asks about something
**Then** Claude SHOULD use `search_workspace` or `get_context` MCP tools to find relevant existing data
**And** Claude SHOULD surface relevant findings to the user
**And** Claude SHOULD link to or reference the found information

**Example Interactions:**
```
User: "Let's discuss the authentication implementation"
Claude: *Uses search_workspace for "authentication"*
        "I found some relevant context from your workspace:
        - A brainstorm session on 2025-11-15 discussed OAuth vs JWT
        - There's a decision record about using session-based auth
        Would you like me to pull in that context?"

User: "What decisions have we made about the API?"
Claude: *Uses get_decision_history for "API"*
        "Here are the API-related decisions I found:
        1. RESTful design pattern (2025-11-10)
        2. JSON response format (2025-11-12)
        Want me to add these to our project documentation?"
```

#### Scenario: Agent retrieves context before creating documents

**Given** a user asks Claude to create a document on a topic
**When** related information exists in the workspace
**Then** Claude SHOULD search for existing relevant content first
**And** Claude SHOULD incorporate or reference found information
**And** Claude SHOULD avoid duplicating existing documentation

---

### Requirement: Agent SHALL maintain an auto-updated document index

The AI assistant SHALL maintain an `index.md` file that tracks all documents in the project, updating it automatically whenever documents are created or modified.

**ID:** `CONV-TYPE-003` | **Priority:** High

#### Scenario: Index is updated when document is created

**Given** a projectmanage conversation is active
**When** Claude creates a new document in `docs/`
**Then** Claude MUST add an entry to `index.md`
**And** the entry MUST include the document path
**And** the entry MUST include a brief description
**And** the entry MUST include a timestamp

**Example Index Entry:**
```markdown
## Documents

### Requirements
- [User Authentication](docs/requirements/user-authentication.md) - Authentication requirements and acceptance criteria (2025-11-20)

### Decisions
- [Database Selection](docs/decisions/database-selection.md) - Decision to use PostgreSQL (2025-11-20)
```

#### Scenario: Index reflects current document state

**Given** a user asks for project overview
**When** Claude provides the overview
**Then** Claude MUST reference `index.md` for document listing
**And** the index MUST accurately reflect all documents in `docs/`

---

### Requirement: Projectmanage master template SHALL support iterative project tracking

The master `project-management.md` template SHALL provide minimal structure that grows organically through conversation, with sections optimized for ongoing execution tracking.

**ID:** `CONV-TYPE-004` | **Priority:** High

#### Scenario: Master template sections cover execution tracking needs

**Given** a new projectmanage conversation is created
**When** the template is generated
**Then** the template MUST include a "Goals" section for success criteria
**And** the template MUST include a "Roadmap" section for phases/milestones
**And** the template MUST include a "Tasks" section for work items with status
**And** the template MUST include a "Status Updates" section for progress log

**Example Template Structure:**
```markdown
# Project Management: [PROJECT NAME]

**ID**: [ID]
**Date**: [DATE]
**Status**: Active

---

## Goals

[What does success look like?]

---

## Roadmap

[High-level phases or milestones]

---

## Tasks

[Current work items with status: TODO / IN PROGRESS / DONE]

---

## Status Updates

[Chronological log of progress and decisions]

---
```

#### Scenario: Tasks support status markers

**Given** a projectmanage conversation is tracking tasks
**When** Claude adds or updates a task
**Then** the task MUST have a status marker (TODO, IN PROGRESS, DONE)
**And** Claude MUST update status markers as work progresses
**And** status updates MUST be reflected in the Status Updates section

**Example:**
```markdown
## Tasks

- [x] DONE: Set up hooks system
- [ ] IN PROGRESS: Add documentation system
- [ ] TODO: Implement RAG pipeline improvements
```

---

### Requirement: Projectmanage SHALL integrate with existing registry system

The projectmanage conversation type SHALL be registered in the workspace registry following the established pattern for built-in conversation types.

**ID:** `CONV-TYPE-005` | **Priority:** Medium

#### Scenario: Init creates projectmanage folder

**Given** a user runs `cortext init`
**When** the workspace is initialized
**Then** a `projectmanage/` folder MUST be created at the workspace root
**And** the registry.json MUST include the projectmanage type definition

#### Scenario: Registry entry follows convention

**Given** the workspace registry is created
**When** projectmanage is added to the registry
**Then** the entry MUST include name, folder, template, command, script, description, and sections fields
**And** the entry MUST have `built_in: true`

**Example Registry Entry:**
```json
{
  "projectmanage": {
    "name": "Project Manage",
    "folder": "projectmanage",
    "template": ".workspace/templates/project-management.md",
    "command": "/workspace.projectmanage",
    "script": ".workspace/scripts/bash/projectmanage.sh",
    "built_in": true,
    "description": "Project management and tracking",
    "sections": ["goals", "roadmap", "tasks", "status", "index"]
  }
}
```
