---
description: Start a brainstorming session for ideation and exploration
tags: [workspace, brainstorm, ideation]
---

# Workspace Brainstorm

You are helping the user start a brainstorming conversation in their Cortext workspace.

## Your Task

1. **Get the topic**
   - Ask the user what they want to brainstorm about
   - Example: "What topic would you like to brainstorm?"

2. **Run the brainstorm script**
   ```bash
   .workspace/scripts/bash/brainstorm.sh "<topic>"
   ```

   This will:
   - Create a new conversation directory with auto-incremented ID
   - Create a git branch for this conversation
   - Copy the brainstorm template
   - Make an initial commit

3. **Guide the brainstorming**
   - Help the user capture ideas without judgment
   - Encourage free exploration
   - Ask probing questions to deepen thinking
   - Identify themes and patterns
   - Suggest connections between ideas

4. **Structure the output**
   - Use the template sections: Goals, Ideas, Themes, Next Steps
   - Keep the conversation organized but flexible
   - Cross-reference related conversations if relevant

## Best Practices

- Embrace divergent thinking - quantity over quality initially
- Don't critique ideas prematurely
- Build on ideas rather than dismissing them
- Look for unexpected connections
- Help prioritize promising directions at the end
- Capture "wild" ideas - they often lead to breakthroughs

## When Complete

- Summarize the key ideas and themes
- Identify 2-3 promising directions for further exploration
- Suggest concrete next steps
- Commit the brainstorm notes
- Ask if the user wants to merge the branch or continue exploring
