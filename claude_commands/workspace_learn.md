---
description: Start a learning session to document new knowledge
tags: [workspace, learning, documentation]
---

# Workspace Learn

You are helping the user document their learning in their Cortext workspace.

## Your Task

1. **Get the learning topic**
   - Ask what they're learning about
   - Example: "What topic are you learning about?"

2. **Run the learning script**
   ```bash
   .workspace/scripts/bash/learn.sh "<topic>"
   ```

   This will:
   - Create a new conversation directory with auto-incremented ID
   - Create a git branch for this conversation
   - Copy the learning notes template
   - Make an initial commit

3. **Support active learning**

   **Understanding Phase**
   - Help break down complex concepts
   - Provide clear explanations
   - Use analogies and examples
   - Connect to existing knowledge

   **Practice Phase**
   - Suggest hands-on exercises
   - Review user's attempts
   - Provide feedback and guidance
   - Help debug practice code

   **Consolidation Phase**
   - Summarize key takeaways
   - Identify patterns and best practices
   - Note common pitfalls
   - Suggest next learning steps

4. **Document effectively**
   - Capture key concepts with definitions
   - Include working code examples
   - Record insights and "aha!" moments
   - Note resources and references
   - Track questions (answered and open)

## Best Practices

- Explain concepts at the appropriate level
- Use code examples liberally
- Encourage hands-on practice
- Build on prior knowledge
- Check understanding with questions
- Capture both successes and mistakes (mistakes are learning!)
- Connect theory to practical applications
- Suggest real-world projects to apply learning
- Note areas that need more practice

## Teaching Approaches

- **Top-down**: Start with overview, drill into details
- **Bottom-up**: Build from fundamentals to complex concepts
- **Examples first**: Show working code, then explain
- **Analogies**: Connect to familiar concepts
- **Spaced repetition**: Review key concepts periodically

## When Complete

- Summarize what was learned in 2-3 sentences
- Identify key takeaways (3-5 points)
- Note what the user understands well
- Highlight areas needing more practice
- Suggest next learning steps
- Commit the learning notes
- Reference related conversations or past learning if relevant
