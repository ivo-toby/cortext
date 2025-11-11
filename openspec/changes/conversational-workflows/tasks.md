# Tasks: Conversational Workflows

**Change ID:** `conversational-workflows`

---

## Implementation Tasks

### Phase 1: Simplify Templates

- [x] **Simplify `templates/learning-notes.md`**
  - Reduce from 248 lines to ~30 lines
  - Keep: Title, metadata, Notes section, References section
  - Remove: All prescriptive sub-fields and detailed structure
  - Make sections flexible and open-ended
  - Verify: Template is clean and minimal

- [x] **Simplify `templates/brainstorm.md`**
  - Minimal scaffolding for ideation
  - Keep: Title, Goals, Ideas, Themes sections
  - Remove: Prescriptive subsections
  - Verify: Supports free-form brainstorming

- [x] **Simplify `templates/debug-session.md`**
  - Keep: Title, Problem, Investigation, Solution sections
  - Make sections open-ended for natural documentation
  - Remove: Rigid checklists and forms
  - Verify: Supports investigative conversation

- [x] **Simplify `templates/feature-planning.md`**
  - Keep: Title, Goals, Approach, Tasks sections
  - Remove: Prescriptive planning templates
  - Make flexible for collaborative planning
  - Verify: Supports iterative planning discussion

- [x] **Simplify `templates/meeting-notes.md`**
  - Keep: Title, Attendees, Notes, Actions sections
  - Remove: Rigid agenda structure
  - Support documentation during conversation
  - Verify: Works for real-time meeting capture

- [x] **Simplify `templates/review-template.md`**
  - Keep: Title, Overview, Feedback sections
  - Remove: Prescriptive review checklist
  - Support back-and-forth dialogue
  - Verify: Enables conversational review

### Phase 2: Redesign Slash Commands for Conversation-First

- [x] **Rewrite `claude_commands/workspace_learn.md`**
  - Change from "fill template" to "have dialogue"
  - Add instructions to update document during conversation
  - Emphasize ongoing exploration over completion
  - Add example of good dialogue pattern
  - Remove "when complete" section (conversation is ongoing)
  - Instruct to use Edit tool frequently during discussion
  - Verify: Instructions encourage natural dialogue

- [x] **Rewrite `claude_commands/workspace_brainstorm.md`**
  - Emphasize iterative ideation
  - Instruct to capture ideas as they emerge (use Edit tool)
  - Remove completion mentality
  - Add prompts to keep generating and exploring
  - Verify: Supports free-flowing brainstorm

- [x] **Rewrite `claude_commands/workspace_debug.md`**
  - Frame as investigative conversation
  - Instruct to document findings in real-time
  - Emphasize back-and-forth troubleshooting
  - Add prompts for continued investigation
  - Verify: Supports debugging dialogue

- [x] **Rewrite `claude_commands/workspace_plan.md`**
  - Frame as collaborative planning session
  - Instruct to refine plan during discussion
  - Remove one-shot generation mentality
  - Add prompts for iterative refinement
  - Verify: Supports planning conversation

- [x] **Rewrite `claude_commands/workspace_meeting.md`**
  - Frame as real-time documentation
  - Instruct to capture notes during discussion
  - Emphasize documenting as conversation happens
  - Add prompts for clarifying questions
  - Verify: Supports meeting conversation

- [x] **Rewrite `claude_commands/workspace_review.md`**
  - Frame as collaborative feedback session
  - Instruct to discuss and document feedback together
  - Remove prescriptive review structure
  - Add prompts for back-and-forth discussion
  - Verify: Supports review dialogue

### Phase 3: Update Custom Type Generation

- [x] **Update `claude_commands/workspace_add.md`**
  - Change template generation to minimal scaffolding
  - Update slash command generation for conversation-first pattern
  - Instruct generated commands to emphasize dialogue
  - Add guidance for minimal template design
  - Verify: Custom types follow conversation-first pattern

### Phase 4: Documentation Updates

- [x] **Update `Docs/user-guide.md`**
  - Add section on "Conversation Workflows"
  - Explain conversation-first approach
  - Show example before/after dialogue patterns
  - Explain how documents evolve during conversation
  - Add section on "How to Signal Completion"
  - Verify: Users understand new workflow

- [x] **Update `README.md` examples**
  - Change examples from template-filling to dialogue
  - Show conversation snippets instead of form-filling
  - Demonstrate document evolution during discussion
  - Verify: Examples reflect conversational approach

### Phase 5: Create Spec Deltas

- [x] **Create `specs/conversation-workflows/spec.md`**
  - Define requirements for conversation-first behavior
  - Specify how documents should evolve during dialogue
  - Define template minimalism requirements
  - Specify slash command instruction patterns
  - Verify: Spec captures all workflow requirements

- [x] **Create `specs/template-system/spec.md`**
  - Define template design philosophy (scaffolding not forms)
  - Specify maximum template complexity
  - Define required vs optional sections
  - Specify flexibility requirements
  - Verify: Spec guides template design

### Phase 6: Validation & Testing

- [x] **Manual Testing - Learn Workflow**
  - Run `/workspace.learn` command
  - Have extended conversation about a topic
  - Verify Claude continues dialogue naturally
  - Verify document updates during conversation
  - Verify no premature "completion"
  - Check final document quality

- [x] **Manual Testing - Brainstorm Workflow**
  - Run `/workspace.brainstorm` command
  - Generate ideas through dialogue
  - Verify iterative ideation works
  - Verify document captures ideas as they emerge
  - Check brainstorm feels collaborative

- [x] **Manual Testing - Other Workflows**
  - Test debug, plan, meeting, review workflows
  - Verify each follows conversation-first pattern
  - Verify documents evolve during dialogue
  - Check all feel natural and collaborative

- [x] **Template Validation**
  - Verify all templates are <50 lines
  - Check all templates are flexible and open-ended
  - Ensure no prescriptive field structures remain
  - Verify templates support organic content

- [x] **Slash Command Validation**
  - Check all commands emphasize ongoing dialogue
  - Verify instructions include Edit tool usage
  - Ensure no "completion" mentality remains
  - Check prompts encourage continued conversation

### Phase 7: Finalization

- [x] **Update CHANGELOG.md**
  - Document conversation workflow redesign
  - Explain template simplification
  - Note improved conversational experience
  - Mention no breaking changes

- [x] **Mark all tasks complete in tasks.md**
  - Check all items are verified
  - Ensure all changes tested
  - Confirm documentation updated

- [x] **Commit changes**
  - Use conventional commit format
  - Include comprehensive description
  - Reference conversation-first philosophy

---

## Validation Checklist

Before marking complete:

- [x] All 6 templates simplified to <50 lines
- [x] All 6 slash commands rewritten for conversation-first
- [x] Slash commands instruct to use Edit tool during conversation
- [x] Documentation explains new workflow
- [x] Manual testing shows improved conversation flow
- [x] No prescriptive field structures remain in templates
- [x] Instructions emphasize ongoing dialogue over completion
- [x] Example conversations demonstrate new pattern

---

## Dependencies

- **None** - This change is self-contained (only affects templates and slash commands)

## Parallel Work

- Phase 1 (6 template simplifications) can be done in parallel
- Phase 2 (6 slash command rewrites) can be done in parallel
- Phase 6 (testing) should be done after Phases 1-2 complete

---

## Rollback Plan

If issues arise:
1. Revert single commit containing all changes
2. Old templates and slash commands restore immediately
3. No data loss - only instruction/template changes
4. User conversations unaffected (bash scripts unchanged)
