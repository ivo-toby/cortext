---
description: Create a custom conversation type with AI assistance
tags: [workspace, extensibility, custom]
---

# Workspace Add - Create Custom Conversation Type

You are helping the user create a custom conversation type for their Cortext workspace.

## Your Task

Guide the user through an interview process to create a personalized conversation template.

### Step 1: Interview the User

Ask these questions one at a time:

1. **"What would you like to call this conversation type?"**
   - Example: "hobbies", "book-notes", "fitness-log"
   - Store as: `type_name`

2. **"What's the primary purpose of this conversation type?"**
   - Example: "Track hobby projects and progress"
   - Store as: `description`

3. **"What phases or sections should this conversation have?"**
   - Example: "Current project, goals, progress, challenges, next steps"
   - Store as: `sections` (list)

4. **"What kind of information needs to be captured?"**
   - Example: "Project details, materials, techniques, time spent"
   - Store as: `fields`

5. **"What outputs or artifacts do you expect?"**
   - Example: "Progress log, photo gallery, skill progression"
   - Store as: `outputs`

6. **"Any special requirements?"** (optional)
   - Example: "Links to resources, embedded images, code snippets"
   - Store as: `special_requirements`

### Step 2: Generate Template

Create a **minimal template** (target ~30 lines) following this philosophy:

**Template Philosophy**: Scaffolding, not forms. Flexible structure, not prescriptive fields.

```markdown
# {Type Name}: [TITLE]

**ID**: [ID]
**Date**: [DATE]
**Status**: In Progress

---

## {Section 1}

[Open-ended content area]

---

## {Section 2}

[Open-ended content area]

---

**Metadata**
- Created: [DATE]
- Tags: {type_name}, [custom-tags]
```

**Important**:
- Keep it under 50 lines total
- Use 3-5 broad sections maximum (based on user's needs)
- NO nested subsections or prescriptive fields
- Use generic placeholders like [Document here], not questionnaires
- Leave white space for organic content growth

### Step 3: Generate Bash Script

Create a bash script at `.workspace/scripts/bash/{type_name}.sh`:

```bash
#!/usr/bin/env bash
# Cortext {Type Name} Script

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

show_header "{Type Name}"

# Parse arguments
TITLE="$1"

if [ -z "$TITLE" ]; then
    print_error "Title is required"
    echo "Usage: $0 <title>" >&2
    exit 1
fi

# Check prerequisites
check_git_initialized

# Get next conversation ID
WORKSPACE_ROOT=$(get_workspace_root)
FOLDER=$(get_conversation_folder "{type_name}")
CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../${FOLDER}/$(date +%Y-%m-%d)"
mkdir -p "$CONVERSATIONS_DIR"

CONVERSATION_ID=$(get_next_id "$CONVERSATIONS_DIR")
TITLE_SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
CONVERSATION_NAME="${CONVERSATION_ID}-{type_name}-${TITLE_SLUG}"
CONVERSATION_DIR="${CONVERSATIONS_DIR}/${CONVERSATION_NAME}"

# Create conversation directory
mkdir -p "$CONVERSATION_DIR"

# Create git branch
BRANCH_NAME="conversation/${CONVERSATION_NAME}"
git checkout -b "$BRANCH_NAME" 2>/dev/null || git checkout "$BRANCH_NAME"

print_success "Created conversation: ${CONVERSATION_NAME}"
print_info "Branch: ${BRANCH_NAME}"

# Copy template
FILE="${CONVERSATION_DIR}/{type_name}.md"
copy_template "{type_name}.md" "$FILE"

# Update placeholders
update_date_in_file "$FILE"
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/\[TITLE\]/$TITLE/g" "$FILE"
    sed -i '' "s/\[ID\]/$CONVERSATION_NAME/g" "$FILE"
else
    sed -i "s/\[TITLE\]/$TITLE/g" "$FILE"
    sed -i "s/\[ID\]/$CONVERSATION_NAME/g" "$FILE"
fi

# Initial commit
print_step "Committing {type_name} session..."
git add "$CONVERSATION_DIR"
git commit -m "[conversation] Initialize {type_name}: ${TITLE}

Created conversation ${CONVERSATION_NAME}.

Type: {type_name}
Purpose: {description}
" 2>/dev/null || print_warning "Nothing new to commit"

# Display summary
echo "" >&2
print_success "{Type Name} session created!"
echo "" >&2
print_info "Conversation: ${CONVERSATION_NAME}"
print_info "File: ${FILE}"
echo "" >&2
```

Make it executable:
```bash
chmod +x .workspace/scripts/bash/{type_name}.sh
```

### Step 4: Generate Slash Command

Create `.claude/commands/workspace_{type_name}.md` with **conversation-first instructions**:

```markdown
---
description: {description}
tags: [workspace, {type_name}, conversation]
---

# Workspace {Type Name}

You are helping the user with a {type_name} conversation.

## Your Task

### 1. Initialize
- Ask what they want to work on
- Run: `.workspace/scripts/bash/{type_name}.sh "<title>"`
- Creates minimal document

### 2. Engage in Dialogue

**This is a conversation, not template-filling.**

- {Conversation approach based on type}
- Keep exploring through natural dialogue
- Build on user's responses
- Let conversation flow naturally

### 3. Document as You Go

**Use Edit tool frequently during conversation:**

- Update document as insights emerge
- Capture key points in real-time
- Don't wait until the end
- Let structure emerge organically

### 4. Continue Until Naturally Complete

- Don't rush to finish
- Keep conversation going
- Let user signal when satisfied
- Offer to explore further

## Best Practices

- Be conversational, not procedural
- Update document during dialogue
- Follow user's curiosity
- Natural completion, not forced
```

### Step 5: Update Registry

Add the new type to `.workspace/registry.json`:

```json
"{type_name}": {
  "name": "{Type Name}",
  "folder": "conversations/{type_name}",
  "template": ".workspace/templates/{type_name}.md",
  "command": "/workspace.{type_name}",
  "script": ".workspace/scripts/bash/{type_name}.sh",
  "built_in": false,
  "created": "{current_date}",
  "created_by": "user",
  "description": "{description}",
  "sections": [{sections}]
}
```

### Step 6: Commit Everything

```bash
git add .workspace/templates/{type_name}.md
git add .workspace/scripts/bash/{type_name}.sh
git add .claude/commands/workspace_{type_name}.md
git add .workspace/registry.json

git commit -m "[workspace] Add '{type_name}' conversation type

User-defined conversation type.

Purpose: {description}
Sections: {sections}"
```

### Step 7: Confirm

Show the user:

```
✅ Created new conversation type: "{type_name}"

Files created:
- Template: .workspace/templates/{type_name}.md
- Script: .workspace/scripts/bash/{type_name}.sh
- Slash command: /workspace.{type_name}

You can now use: /workspace.{type_name}

To edit the template later:
Edit .workspace/templates/{type_name}.md
```

## Best Practices

- Keep templates focused on a specific use case
- Provide helpful prompts and examples in templates
- Use clear section names
- Include metadata for searchability
- Make scripts reusable and clear

## Example Conversation

**AI**: What would you like to call this conversation type?
**User**: book-notes

**AI**: What's the primary purpose of this conversation type?
**User**: Track books I'm reading with notes and key takeaways

**AI**: What phases or sections should this conversation have?
**User**: Book info, reading progress, chapter notes, key insights, quotes, personal reflections, rating

[Continue through all questions, then generate all files]

**AI**: ✅ Created "book-notes" conversation type! Use `/workspace.book-notes` to start tracking a book.
