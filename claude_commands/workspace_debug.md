---
description: Start a debugging session for problem solving and troubleshooting
tags: [workspace, debug, troubleshooting]
---

# Workspace Debug

You are helping the user debug an issue in their Cortext workspace.

## Your Task

1. **Understand the problem**
   - Ask the user to describe the issue
   - Gather context: when it started, what changed, impact
   - Example: "What issue are you trying to debug?"

2. **Run the debug script**
   ```bash
   .workspace/scripts/bash/debug.sh "<issue>"
   ```

   This will:
   - Create a new conversation directory with auto-incremented ID
   - Create a git branch for this conversation
   - Copy the debug template
   - Make an initial commit

3. **Systematic investigation**
   - Help document observed vs expected behavior
   - Gather reproduction steps
   - Collect logs, error messages, and evidence
   - Form and test hypotheses
   - Rule out causes systematically
   - Identify root cause

4. **Document the solution**
   - Record the fix and verification steps
   - Capture learnings and prevention measures
   - Update relevant documentation
   - Commit the findings

## Best Practices

- Use the scientific method: hypothesize, test, observe, conclude
- Document everything - even dead ends are valuable
- Verify the fix actually works
- Think about prevention, not just fixing
- Consider similar issues that might exist
- Update monitoring and alerting if relevant

## Debugging Strategies

- Binary search: divide problem space in half
- Add logging/instrumentation
- Reproduce in isolation
- Compare working vs broken states
- Check recent changes (git log)
- Review assumptions
- Rubber duck debugging

## When Complete

- Summarize the root cause and solution
- Document lessons learned
- Identify prevention measures
- Commit the debug session
- Update any relevant guides or documentation
