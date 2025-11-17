# conversation-workflows Specification

## Purpose
TBD - created by archiving change conversational-workflows. Update Purpose after archive.
## Requirements
### Requirement: Conversation commands SHALL initiate ongoing dialogue
Slash commands for conversation types SHALL instruct Claude to engage in extended dialogue with real-time documentation, not one-shot template generation.

**ID:** `CONV-FLOW-001` | **Priority:** High

#### Scenario: Learn command starts dialogue not template-filling

**Given** a user runs `/workspace.learn` command
**When** they specify a learning topic
**Then** Claude MUST start an exploratory conversation about the topic
**And** Claude MUST ask follow-up questions to understand user's context
**And** Claude MUST continue dialogue beyond initial exchange
**And** Claude MUST NOT treat initial response as "completion"

**Example:**
```
User: /workspace.learn
Claude: "What topic are you learning about?"
User: "Kubernetes networking"
Claude: "Great! Let's explore Kubernetes networking together.
        What's your current understanding? Are you familiar
        with how containers communicate?"
[Conversation continues...]
```

#### Scenario: Brainstorm command enables iterative ideation

**Given** a user runs `/workspace.brainstorm` command
**When** they specify a topic to brainstorm
**Then** Claude MUST engage in iterative idea generation
**And** Claude MUST build on ideas through dialogue
**And** Claude MUST continue generating until user signals completion
**And** Claude MUST NOT rush to "summarize and finish"

---

### Requirement: Documents MUST be updated during conversation
Claude SHALL edit conversation documents in real-time as insights emerge during dialogue, not just at initialization.

**ID:** `CONV-FLOW-002` | **Priority:** High

#### Scenario: Learning notes evolve during dialogue

**Given** a learning conversation is in progress
**When** Claude and user discuss a concept
**Then** Claude MUST use Edit tool to add insights to the document
**And** Updates MUST happen during conversation, not just at start/end
**And** Document MUST grow organically as dialogue progresses
**And** Claude MUST document key insights as they emerge

**Implementation:**
```markdown
# Learning Notes: Kubernetes Networking

**Date:** 2025-11-11

---

