# Spec Delta: Conversation Workflows

**Capability:** conversation-workflows
**Change ID:** conversational-workflows

---

## ADDED Requirements

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

## Notes

### Container Communication Basics
[Claude adds this during initial discussion]

Each pod gets its own IP address. This enables direct
pod-to-pod communication without NAT...

[Later in conversation, Claude adds:]

### Overlay Networks
The overlay network (like Calico or Flannel) handles
routing between nodes. It creates a virtual network
layer that spans the cluster...

[Document grows as conversation continues]
```

#### Scenario: Debug session documents findings in real-time

**Given** a debug conversation is in progress
**When** Claude and user investigate an issue
**Then** Claude MUST document findings immediately as they're discovered
**And** Document MUST reflect the investigation process
**And** Claude MUST update document multiple times during session

---

### Requirement: Slash command instructions MUST emphasize ongoing dialogue
Conversation type slash commands SHALL explicitly instruct Claude to maintain dialogue flow and avoid completion mentality.

**ID:** `CONV-FLOW-003` | **Priority:** High

#### Scenario: Slash command instructs ongoing conversation

**Given** a slash command file for a conversation type
**When** the file contains Claude's instructions
**Then** it MUST include instructions to continue dialogue
**And** it MUST instruct use of Edit tool during conversation
**And** it MUST avoid "when complete" language that implies one-shot
**And** it MUST include prompts to keep conversation flowing

**Example - workspace_learn.md:**
```markdown
## Your Task

1. Ask what they're learning about
2. Create minimal document with topic
3. **Start exploring through conversation**
   - Ask about current understanding
   - Explain concepts through dialogue
   - Update document as insights emerge (use Edit tool)
   - Keep conversation going with follow-up questions
4. **Continue until user signals completion**
   - Don't rush to finish
   - Offer to explore related topics
   - Let user determine when they're satisfied
```

**Anti-pattern (avoid):**
```markdown
## Your Task

1. Ask what they're learning
2. Fill in template sections
3. When complete: Summarize and commit  ❌
```

---

### Requirement: Conversations SHALL have natural completion signals
Conversations MUST end naturally when user signals satisfaction, not based on template completion or step count.

**ID:** `CONV-FLOW-004` | **Priority:** Medium

#### Scenario: User signals natural completion

**Given** a conversation is in progress
**When** user says something indicating satisfaction
**Then** Claude MUST recognize completion signal
**And** Claude MUST offer to continue if more questions
**And** Claude MUST NOT force "summary and finish" pattern

**Completion signals:**
- "Thanks, I think I've got it"
- "That's enough for now"
- "I'm good, appreciate the help"
- "Let me try this and come back"

**Example:**
```
User: "Ah, that makes sense now. Thanks!"
Claude: "Glad it clicked! Is there anything else about
        Kubernetes networking you'd like to explore, or
        are you good to start experimenting?"
User: "I'm good for now"
Claude: "Sounds good! I've documented everything we
        discussed in your learning notes. Feel free to
        come back if questions come up."
```

---

## Implementation Notes

### Slash Command Pattern

All conversation type slash commands should follow this pattern:

```markdown
## Your Task

1. **Initialize conversation**
   - Ask user for topic/context
   - Run bash script to create conversation directory
   - Create minimal document

2. **Engage in dialogue**
   - Start conversation about the topic
   - Ask questions to understand context
   - Provide explanations and insights
   - Build on user's responses

3. **Document as you go**
   - Use Edit tool to add insights during conversation
   - Update document multiple times
   - Let structure emerge organically
   - Don't force rigid template

4. **Continue naturally**
   - Keep asking relevant questions
   - Offer to explore related areas
   - Let user signal when done
   - Don't rush to completion
```

### Edit Tool Usage

Claude should use Edit tool frequently:
- After explaining a key concept
- When user has an "aha!" moment
- After working through an example
- When discovering a solution (debug)
- As new ideas emerge (brainstorm)

Pattern:
```
Claude: [Explains concept]
        "Let me add that to your notes..."
        [Uses Edit tool to add explanation]
        "Now, building on that..."
```

### Avoiding Completion Mentality

**Remove these patterns from slash commands:**
- "When complete" sections
- Step counts that imply finite process
- "Summarize and finish" instructions
- Template completion as success criteria

**Add these patterns:**
- "Continue until user is satisfied"
- "Keep exploring through dialogue"
- "Update document during conversation"
- "Natural conversation flow"

---

## Testing

**Test Cases:**
1. Run `/workspace.learn`, verify extended dialogue beyond initial exchange
2. Check document is updated multiple times during conversation
3. Verify conversation doesn't end prematurely after template creation
4. Test natural completion signals are recognized
5. Verify Edit tool is used frequently during dialogue
6. Check all 6 conversation types follow dialogue pattern

---

## Migration

**No migration needed:**
- Existing conversations unaffected
- Only new conversations use updated workflow
- Bash scripts unchanged
- File structure unchanged
- Purely instruction/behavior change
