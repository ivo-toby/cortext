---
description: Create structured meeting notes with action items
tags: [workspace, meeting, notes]
---

# Workspace Meeting

You are helping the user document a meeting in their Cortext workspace.

## Your Task

1. **Get the meeting title**
   - Ask for the meeting name or purpose
   - Example: "What meeting are you documenting?"

2. **Run the meeting script**
   ```bash
   .workspace/scripts/bash/meeting.sh "<meeting-title>"
   ```

   This will:
   - Create a new conversation directory with auto-incremented ID
   - Create a git branch for this conversation
   - Copy the meeting notes template
   - Make an initial commit

3. **Capture meeting details**

   **Before/Start of Meeting**
   - List attendees and roles
   - Note the agenda
   - Record date, time, and duration

   **During Meeting**
   - Document discussion points by agenda item
   - Capture decisions made with context and rationale
   - Record action items with owners and deadlines
   - Note questions raised and answers given
   - Track blockers and concerns
   - Keep a "parking lot" for off-topic items

   **End of Meeting**
   - Summarize key takeaways
   - Review action items to ensure clarity
   - Plan next meeting if needed

4. **Structure action items clearly**
   - Each action should have an owner
   - Include deadlines or target dates
   - Prioritize (high/medium/low)
   - Make actions specific and measurable

## Best Practices

- Start with agenda - know what to cover
- Capture decisions with rationale, not just "what"
- Assign clear owners to action items
- Set realistic deadlines
- Note dissenting opinions if relevant
- Keep notes organized by agenda items
- Use the parking lot for tangents
- Review action items before closing
- Distribute notes promptly after meeting

## Meeting Types

**Standup/Status**
- Quick updates, blockers, plans
- Keep it brief and focused

**Planning**
- Goals, requirements, approach
- Break down into tasks
- Estimate and prioritize

**Retrospective**
- What went well, what didn't
- Action items for improvement
- Blameless post-mortem culture

**Review/Demo**
- Show completed work
- Gather feedback
- Plan next steps

## When Complete

- Summarize key decisions and actions
- Ensure all action items have owners and deadlines
- Commit the meeting notes
- Consider sharing notes with attendees
- Create follow-up tasks if needed
- Schedule next meeting if appropriate
