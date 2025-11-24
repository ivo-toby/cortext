# Proposal: Add Project Management Conversation Type

## Summary

Add a new `projectmanage` conversation type to Cortext that enables AI assistants to act as project management partners - capturing ideas, tracking tasks and status, defining goals and roadmaps, breaking down work, managing project documentation, and providing portfolio-level overview to users. The assistant actively leverages LLM categorization strengths to organize project data and proactively retrieves relevant context from the workspace.

## Motivation

Currently, Cortext has a `plan` conversation type focused on **single feature/project planning** - the ideation and design phase. However, there's a gap for **ongoing project execution tracking**:

- **plan**: "What should we build and how?" (design phase)
- **projectmanage**: "What's the status and what's next?" (execution phase)

When managing a project like building Cortext with Cortext, users need:
- A place to capture ideas as they emerge
- Task tracking with status updates
- Goal and milestone visibility
- Roadmap overview across multiple work items
- Ability to see the "big picture" of ongoing work
- **Organized project documentation** (requirements, notes, decisions, research)
- **Proactive context retrieval** - AI finds relevant existing data

The `projectmanage` type complements `plan` by providing a persistent hub for execution tracking rather than a one-time planning conversation. A key differentiator is the **multi-document architecture** where the agent creates and manages multiple specialized documents within the project, leveraging LLM categorization to organize information appropriately.

## Scope

### In Scope

- New `projectmanage` conversation type with template, script, and slash command
- Registry entry for the new type
- **Multi-document architecture** with subfolders by document type
- **Auto-maintained index.md** that tracks all project documents with links
- **Flexible document types** - agent categorizes and creates documents based on content (requirements, notes, decisions, research, etc.)
- Claude command that instructs AI to:
  - Behave as project management assistant
  - **Actively search workspace** for relevant existing data using MCP tools
  - Create and manage multiple documents with meaningful filenames
  - Maintain the index file automatically
- Document evolution during conversation (real-time updates)

### Out of Scope

- Cross-conversation aggregation or dashboard views
- Automated task dependency tracking
- Integration with external project management tools
- Timeline visualization or Gantt charts
- Team/resource allocation tracking
- Predefined fixed document types (agent decides organically)

## Approach

Follow the established pattern for conversation types with enhanced multi-document support:

1. **Template** (`templates/project-management.md`): Master document with Goals, Roadmap, Tasks, Status Updates
2. **Index template** (`templates/project-index.md`): Auto-maintained document index
3. **Bash script** (`scripts/bash/projectmanage.sh`): Creates conversation directory with subfolder structure, copies templates, commits to git
4. **Slash command** (`claude_commands/workspace_projectmanage.md`): Instructs Claude to act as PM assistant with focus on documentation, context retrieval, and multi-document management
5. **Registry entry**: Add to default types in `init.py`

### Directory Structure

```
projectmanage/2025-11-20/001-projectmanage-cortext/
├── project-management.md    # Master status/tasks document
├── index.md                 # Auto-maintained document index
└── docs/
    ├── requirements/        # Requirements documents
    ├── notes/               # Meeting notes, research notes
    ├── decisions/           # Decision records
    └── ...                  # Agent creates subfolders as needed
```

### Agent Behaviors

The Claude command will instruct the agent to:

1. **Proactive context retrieval**: Use MCP tools (`search_workspace`, `get_context`, `get_decision_history`) to find relevant existing data when discussing topics
2. **Intelligent categorization**: Decide document type based on content (e.g., "this sounds like a requirement" → create in `docs/requirements/`)
3. **Meaningful filenames**: Create documents with descriptive names (e.g., `user-authentication-requirements.md`, not `doc-001.md`)
4. **Index maintenance**: Update `index.md` whenever documents are created/modified
5. **Document linking**: Cross-reference related documents within the project

### Document Flexibility

The agent decides what type of document to create based on content:
- User describes a requirement → `docs/requirements/<descriptive-name>.md`
- User shares meeting notes → `docs/notes/<meeting-topic>.md`
- User makes a decision → `docs/decisions/<decision-topic>.md`
- User shares research → `docs/research/<research-topic>.md`

This leverages LLM categorization strengths rather than forcing rigid templates.

## Risks and Considerations

### Risk: Overlap with plan type
**Mitigation**: Clear differentiation - `plan` is for single-feature design, `projectmanage` is for ongoing execution tracking with multi-document support. They complement each other.

### Risk: Document sprawl
**Mitigation**: Auto-maintained index provides overview. Agent uses clear categorization to keep documents organized in appropriate subfolders.

### Risk: Index getting out of sync
**Mitigation**: Claude command explicitly instructs agent to update index.md after every document creation/modification. Index includes last-updated timestamps.

### Risk: Unclear categorization
**Mitigation**: Agent explains categorization decisions and can recategorize if user disagrees. Flexibility is a feature - agent learns user's preferences through conversation.

### Risk: MCP search overhead
**Mitigation**: Agent uses targeted searches, not broad queries. Caches relevant context during conversation to avoid repeated searches.

## Success Criteria

- User can create a projectmanage conversation via `/workspace.projectmanage`
- Claude behaves as PM assistant: asking about status, capturing ideas, updating tasks
- **Agent creates multiple documents** with meaningful filenames organized in subfolders
- **Agent maintains index.md** automatically as documents are created/updated
- **Agent proactively searches** workspace for relevant context during conversations
- Agent categorizes information appropriately (requirements, notes, decisions, etc.)
- Type integrates with existing MCP search (filter by `projectmanage` type)
- Existing conversation types remain unchanged
