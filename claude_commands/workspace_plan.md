---
description: Start a feature or project planning session
tags: [workspace, planning, features]
---

# Workspace Plan

You are helping the user plan a feature or project in their Cortext workspace.

## Your Task

1. **Get the feature/project name**
   - Ask what they want to plan
   - Example: "What feature or project are you planning?"

2. **Run the planning script**
   ```bash
   .workspace/scripts/bash/plan.sh "<feature-name>"
   ```

   This will:
   - Create a new conversation directory with auto-incremented ID
   - Create a git branch for this conversation
   - Copy the planning template
   - Make an initial commit

3. **Guide the planning process**

   **Phase 1: Define & Scope**
   - Clarify goals and success criteria
   - Identify requirements (functional & non-functional)
   - Define what's explicitly out of scope

   **Phase 2: Design**
   - Explore technical approaches
   - Discuss trade-offs and alternatives
   - Make architectural decisions
   - Consider dependencies and constraints

   **Phase 3: Break Down**
   - Divide into phases or milestones
   - Create concrete, actionable tasks
   - Estimate complexity and duration
   - Identify risks and mitigation strategies

   **Phase 4: Operationalize**
   - Define testing strategy
   - Plan rollout and monitoring
   - Document what needs documentation

4. **Document decisions**
   - Record key decisions with rationale
   - Capture alternatives considered
   - Note assumptions and constraints

## Best Practices

- Start with "why" - understand the motivation
- Define success metrics upfront
- Consider non-functional requirements early (performance, security, etc.)
- Break large features into shippable increments
- Identify dependencies and blockers early
- Think about testing and rollback from the start
- Document decisions and rationale, not just the plan
- Review the constitution for relevant working principles

## Questions to Ask

- What problem does this solve for users?
- What are the success criteria?
- What are the must-haves vs nice-to-haves?
- What are the risks and unknowns?
- What dependencies exist?
- How will we test this?
- How will we monitor this in production?
- What could go wrong?

## When Complete

- Summarize the plan and next steps
- Ensure all phases have clear deliverables
- Commit the planning document
- Consider creating follow-up tasks or issues
- Reference this plan in implementation work
