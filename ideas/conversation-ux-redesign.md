# Brainstorm: Conversation UX Redesign

**Date:** 2025-11-11
**Status:** Problem identified, needs OpenSpec proposal

---

## The Problem

Current conversation workflows are **template-filling**, not **conversation-documenting**.

### Current (Broken) Flow

1. Run `/workspace.learn`
2. "What do you want to learn?"
3. User answers
4. Claude generates a **static document** from a template
5. Conversation basically ends ❌

**Feels like:**
- "Fill out this form"
- One-shot generation
- Prescriptive structure
- No actual dialogue

### Desired Flow

1. Run `/workspace.learn`
2. "What do you want to learn?"
3. User answers
4. **User and Claude have an actual conversation about the topic**
5. **Claude documents insights in real-time as you discuss**
6. The document grows organically through dialogue
7. Natural back-and-forth until user is done ✅

**Should feel like:**
- "Let's explore this together"
- Living document that evolves
- Natural dialogue with documentation as a side-effect
- Continuous refinement

---

## Specific Issues

### Issue 1: One-Shot Generation
After initial template creation, the conversation ends. No ongoing dialogue.

### Issue 2: Template Over Conversation
Templates are too prescriptive. They define "fields to fill" instead of "sections to explore."

### Issue 3: No Real-Time Documentation
Claude should be updating the document **during** the conversation, not just at the start.

### Issue 4: Unclear "Done" Signal
No natural way to continue or signal completion. User has to explicitly ask to keep going.

---

## Proposed Solution

### 1. Redesign Slash Command Prompts

Change conversation type prompts (like `/workspace.learn`) to:

**Start a conversation, not fill a template:**
- Ask questions naturally
- Explore the topic together
- Let the dialogue flow
- Don't treat initial response as "done"

**Document as we go:**
- Update the learning notes file continuously during conversation
- Add insights when they emerge
- Refine and reorganize as discussion evolves
- Use Edit tool frequently to update document

**Keep it open-ended:**
- Keep asking follow-ups naturally
- Let user signal when finished
- Suggest related topics to explore
- Don't force rigid structure

### 2. Minimize Templates

Templates should be **minimal scaffolding**, not prescriptive forms:

**Current (too prescriptive):**
```markdown
## Topic
[Describe the topic]

## Key Concepts
[List key concepts]

## Examples
[Provide examples]
```

**Better (minimal scaffolding):**
```markdown
# Learning: [Topic]

**Date:** [DATE]

---

## Notes

[Document insights as we discuss...]

---

## References

```

### 3. Update Slash Command Behavior

Change slash commands to emphasize **conversation over generation**:

**Current instruction pattern:**
```markdown
1. Ask: "What would you like to learn?"
2. Create file from template
3. Fill in placeholders
4. Done
```

**Better instruction pattern:**
```markdown
1. Ask: "What would you like to learn?"
2. Create minimal document with topic
3. Start exploring the topic through questions
4. Document insights by editing the file as we talk
5. Keep going until user signals they're done
6. Natural conversation flow - don't rush to "complete" the document
```

---

## Affected Conversation Types

This issue affects **all** conversation types:

- ❌ **Learn**: One-shot template instead of exploratory dialogue
- ❌ **Brainstorm**: Should be iterative ideation, not form-filling
- ❌ **Debug**: Should be investigative conversation, not checklist
- ❌ **Plan**: Should be collaborative planning, not template completion
- ❌ **Meeting**: Should document during discussion, not after
- ❌ **Review**: Should be back-and-forth feedback, not one response

---

## Technical Changes Needed

### 1. Slash Command Files
**Files:** `.claude/commands/workspace_*.md`

Update all conversation type commands to:
- Emphasize ongoing dialogue
- Instruct to use Edit tool frequently during conversation
- Remove "completion" mentality
- Add prompts to keep conversation going

### 2. Templates
**Files:** `.workspace/templates/*.md`

Simplify all templates:
- Remove prescriptive field structure
- Provide minimal section headers
- Focus on flexibility
- Let content emerge from conversation

### 3. Bash Scripts
**Files:** `scripts/bash/*.sh`

No changes needed - scripts just create folders and copy templates.

### 4. Documentation
Update user guide to explain:
- Conversations are dialogues, not forms
- Documents evolve during discussion
- How to signal when done
- How to continue later

---

## Example: Redesigned Learn Flow

### Before (Template-Filling)
```
User: /workspace.learn
Claude: "What do you want to learn?"
User: "Kubernetes networking"
Claude: [Creates document with sections filled]
        "I've created your learning notes!"
[Conversation ends]
```

### After (Conversation-Documenting)
```
User: /workspace.learn
Claude: "What do you want to learn?"
User: "Kubernetes networking"
Claude: [Creates minimal document]
        "Great! Let's explore Kubernetes networking together.

        First, what's your current understanding? Are you familiar
        with how containers communicate?"
User: "I know Docker basics but networking is fuzzy"
Claude: [Updates document with initial context]
        "Perfect starting point. Let's start with pod-to-pod
        communication. Each pod gets its own IP address..."
        [Continues dialogue, updating document as insights emerge]
User: "Ah, so the overlay network handles routing between nodes?"
Claude: [Adds insight to document]
        "Exactly! Let me add a note about that. Now, have you
        worked with Services yet? They're how you expose pods..."
[Conversation continues naturally until user is satisfied]
```

---

## Next Steps

1. **Create OpenSpec proposal** for this redesign
2. **Prioritize conversation types** to update (start with Learn and Brainstorm)
3. **Redesign slash command prompts** with conversation-first approach
4. **Simplify templates** to minimal scaffolding
5. **Update documentation** to explain conversation workflow
6. **Test with real usage** and iterate

---

## Open Questions

- Should we provide explicit "continue" or "done" commands?
- How do we handle resuming a conversation in a later session?
- Should templates be even more minimal (just title + empty sections)?
- Do we need different instruction patterns for different conversation types?
- How do we guide Claude to update files frequently without being annoying?

---

## Related

- All conversation type slash commands need redesign
- Template philosophy needs rethinking
- User expectations vs actual behavior mismatch
