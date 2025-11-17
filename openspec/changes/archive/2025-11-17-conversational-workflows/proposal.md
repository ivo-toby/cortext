# Proposal: Conversational Workflows

**Change ID:** `conversational-workflows`
**Status:** Draft
**Created:** 2025-11-11
**Author:** User + System

---

## Why

**Current Problem**: Conversation workflows feel like **template-filling** instead of **conversation-documenting**.

When users run conversation commands like `/workspace.learn`, they experience:
1. Initial question: "What do you want to learn?"
2. One exchange
3. Claude generates a complete document from template
4. Conversation essentially ends ❌

**User Expectation**: An actual ongoing dialogue where:
1. User and Claude converse naturally about the topic
2. Document evolves organically during the conversation
3. Claude updates the file in real-time as insights emerge
4. Conversation continues until user signals completion

**Root Causes**:
- **Prescriptive templates**: 248-line learning template with specific fields to fill
- **One-shot mentality**: Slash commands treat initial response as "done"
- **No real-time documentation**: Claude creates document once, doesn't update during dialogue
- **Form-filling framing**: Instructions emphasize "structure" and "sections" over conversation

**Impact**:
- Poor user experience - feels mechanical, not collaborative
- Underutilized AI capability - Claude can have rich dialogue but isn't instructed to
- Templates dictate structure instead of enabling exploration
- No natural conversation flow

---

## What Changes

Transform conversation workflows from **template-filling** to **conversation-documenting**.

### New Conversation Flow

**Before:**
```
User: /workspace.learn
Claude: "What topic?"
User: "Kubernetes networking"
Claude: [Generates 248-line document with fields]
        "Done! I've created your learning notes."
[End]
```

**After:**
```
User: /workspace.learn
Claude: "What topic?"
User: "Kubernetes networking"
Claude: [Creates minimal document with topic]
        "Let's explore Kubernetes networking together!

        What's your current understanding? Are you familiar
        with how containers communicate?"
User: "I know Docker basics but networking is fuzzy"
Claude: [Updates document with context]
        "Perfect starting point. Each pod gets its own IP..."
        [Continues natural dialogue, updating document as we go]
User: "Ah, so the overlay network handles routing?"
Claude: [Adds insight to document]
        "Exactly! Now let's talk about Services..."
[Conversation continues until user is satisfied]
```

### Core Changes

**1. Simplify Templates (Minimal Scaffolding)**
- Remove prescriptive field structure
- Provide basic section headers only
- Let content emerge from conversation
- Maximum ~30 lines vs current 248

**2. Redesign Slash Commands (Conversation-First)**
- Instruct Claude to have ongoing dialogue
- Emphasize using Edit tool during conversation
- Remove "completion" mentality
- Add prompts to continue conversation naturally

**3. Real-Time Documentation Pattern**
- Update document during conversation (not just at start)
- Use Edit tool frequently to add insights
- Let structure emerge organically
- Document as you discuss

---

## Impact

### Files Affected

**Templates** (6 files - all conversation types):
- `templates/learning-notes.md` - Simplify from 248 to ~30 lines
- `templates/brainstorm.md` - Simplify to minimal scaffolding
- `templates/debug-session.md` - Simplify
- `templates/feature-planning.md` - Simplify
- `templates/meeting-notes.md` - Simplify
- `templates/review-template.md` - Simplify

**Slash Commands** (6 files):
- `claude_commands/workspace_learn.md` - Conversation-first instructions
- `claude_commands/workspace_brainstorm.md` - Ongoing dialogue emphasis
- `claude_commands/workspace_debug.md` - Investigative conversation pattern
- `claude_commands/workspace_plan.md` - Collaborative planning flow
- `claude_commands/workspace_meeting.md` - Document during discussion
- `claude_commands/workspace_review.md` - Back-and-forth feedback pattern

**Documentation** (2 files):
- `Docs/user-guide.md` - Explain conversation-first workflow
- `README.md` - Update examples to show dialogue pattern

**Not affected**:
- Bash scripts (no changes needed)
- Registry system
- MCP server
- Core CLI commands

### Breaking Changes

**No breaking changes** - This is a UX improvement:
- Existing templates still work (just verbose)
- Bash scripts unchanged
- File structure unchanged
- Only slash command instructions and templates change
- Users with custom conversation types unaffected

---

## Design Decisions

### Why Simplify Templates So Drastically?

**Current template** (learning-notes.md, 248 lines):
- Prescribes 20+ specific sections
- Each section has sub-fields to fill
- Feels like a questionnaire
- Structure dominates over content

**Proposed template** (~30 lines):
- Title and metadata
- 3-4 flexible section headers
- Mostly empty space for organic content
- Structure serves conversation, not vice versa

**Rationale**: Templates should be **scaffolding**, not **forms**. The conversation should determine content, not a pre-defined structure.

### Why Focus on Slash Commands?

Slash commands are the **primary interface** for starting conversations. They set expectations and guide Claude's behavior. By changing instructions from "fill template" to "have dialogue and document as you go," we transform the entire experience without touching bash scripts or infrastructure.

### What About "Done" Signals?

**Current**: Implicit - Claude stops after generating document
**Proposed**: Natural - Conversation flows until user says "that's enough" or "I'm good"

No explicit `/done` command needed. Claude should:
- Keep asking relevant questions
- Offer to explore related topics
- Let user signal completion naturally ("Thanks, I think I've got it")

### Template Philosophy

**Old philosophy**: "Provide comprehensive structure so users capture everything"
**New philosophy**: "Provide minimal scaffold so conversation can flow naturally"

Users don't need 20 sections predefined. They need:
1. Title/metadata (what is this?)
2. A place for notes (content)
3. A place for references (links/resources)
4. Flexibility to add sections as needed

---

## Acceptance Criteria

- ✅ All 6 conversation type templates simplified to ~30 lines
- ✅ All 6 slash commands rewritten with conversation-first instructions
- ✅ Slash commands instruct Claude to update documents during conversation
- ✅ Instructions emphasize ongoing dialogue over one-shot generation
- ✅ Documentation explains new conversation workflow
- ✅ Example conversations demonstrate dialogue pattern
- ✅ No changes to bash scripts or infrastructure

---

## Timeline

**Estimated Effort:** 3-4 hours
**Complexity:** Low (mostly content rewriting, no code changes)

---

## Related Specifications

This proposal affects:
- `conversation-workflows` (new spec) - How conversations should work
- `template-system` (new spec) - Template design philosophy
- No existing specs modified (no base specs exist yet)

---

## References

- Brainstorming document: `ideas/conversation-ux-redesign.md`
- Current learning template: `templates/learning-notes.md:1` (248 lines)
- Current learn command: `claude_commands/workspace_learn.md:1`
- All conversation types follow same pattern (6 total)

---

## Open Questions

1. **Should we provide example conversations in slash commands?**
   - Show before/after dialogue patterns
   - Help Claude understand desired flow

2. **How minimal is too minimal for templates?**
   - Just title + empty sections?
   - Keep some prompting text?

3. **Should we update custom type generation (`workspace_add.md`)?**
   - Same conversation-first pattern
   - Minimal template generation
