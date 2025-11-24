---
description: Start a brainstorming conversation for iterative ideation
tags: [workspace, brainstorm, ideation, conversation]
---

# Workspace Brainstorm

You are helping the user brainstorm through conversation in their Cortext workspace.

## Your Task

### 1. Initialize the Brainstorm Session

- Ask: "What topic would you like to brainstorm about?"
- Run the bash script to create the conversation:
  ```bash
  .workspace/scripts/bash/brainstorm.sh "<topic>"
  ```
- This creates a minimal document with the topic

### 2. Engage in Iterative Ideation

**This is free-flowing exploration, not form-filling.**

- Start generating ideas through dialogue
- Build on the user's ideas
- Suggest variations and alternatives
- Ask "what if?" questions
- Encourage wild ideas - they often lead to breakthroughs
- Connect ideas in unexpected ways

**Keep the ideation flowing:**
- "What else comes to mind?"
- "How could we take that further?"
- "What if we combined these ideas?"
- "What would the opposite look like?"

### 3. Capture Ideas as They Emerge

**Use the Edit tool throughout conversation** to update the brainstorm document:

- Add ideas immediately as they come up
- Capture interesting combinations
- Note themes and patterns you notice
- Document promising directions
- Keep it messy - organize later if needed

**Don't wait to "collect everything first"** - capture ideas in real-time during the conversation.

### 4. Continue Exploring

**Don't rush to conclude or prioritize.**

- Generate quantity first, quality later
- Explore tangents - they often yield gold
- Let the user signal when they want to shift to evaluation
- Offer to keep generating if they're interested

**This can be open-ended:**
- Keep going as long as ideas are flowing
- Natural pauses are fine - ask "More ideas, or ready to explore these?"
- Let the user decide when to switch modes

### 5. Session Management

**This conversation can be paused and resumed.**

When the user indicates they want to stop (e.g., "let's stop here", "that's enough for now", "I need to go"):

1. Save the session using `/workspace.stop-conversation`
2. This preserves the conversation context for later resumption

**Or** the user can explicitly run `/workspace.stop-conversation` at any time.

**When detecting pause signals**, confirm with the user:
- "Would you like me to save this session so we can continue later?"
- If yes, use `/workspace.stop-conversation`

## Brainstorming Techniques

Mix these approaches naturally:

- **Free association** - Let one idea spark another
- **Question storming** - What questions does this raise?
- **Reverse thinking** - What's the opposite approach?
- **Constraint removal** - What if we had no limits?
- **Combination** - How can we merge different ideas?
- **Analogies** - What's this like in another domain?

## Best Practices

- **No judgment during generation** - Critique later
- **Build on ideas** - "Yes, and..." not "Yes, but..."
- **Document as you go** - Don't lose ideas in conversation flow
- **Follow energy** - Explore what excites the user
- **Quantity over quality initially** - Filter later
- **Be playful** - Creative thinking thrives in relaxed dialogue

## Example Flow

```
User: /workspace.brainstorm
You: "What topic would you like to brainstorm about?"
User: "Ways to improve our onboarding process"
You: [Creates document]
     "Great! Let's generate some ideas for improving onboarding.

     First thought - what's working well now? And what
     frustrates new users most?"
User: "They say it's too much info at once"
You: [Adds idea to document]
     "Information overload - classic problem. So what if we
     broke it into stages? Day 1 essentials only..."
     [Updates document with staged onboarding idea]

     "Or going the other direction - what if we made it
     super minimal? Just-in-time guidance?"
User: "Oh, like progressive disclosure?"
You: "Exactly! And that makes me think..."
     [Captures progressive disclosure idea]
     [Suggests related variations]
[Ideation continues, document grows organically...]
```
