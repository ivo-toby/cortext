# git-workflow Specification

## Purpose

Defines the git workflow for conversation management in Cortext workspaces, using a main-only branch approach with optional tagging for conversation boundaries.

## ADDED Requirements

### Requirement: Conversation scripts SHALL commit directly to main branch

All conversation initialization scripts MUST commit directly to the main branch instead of creating separate conversation branches.

**ID:** `GIT-001` | **Priority:** High

#### Scenario: Creating a new conversation commits to main

**Given** a user is on the main branch (or any branch)
**When** they run a conversation script (e.g., `brainstorm.sh "Topic"`)
**Then** the script MUST switch to main branch if not already on it
**And** the script MUST create the conversation directory
**And** the script MUST commit directly to main
**And** the script MUST NOT create a new conversation branch

**Example:**
```bash
# User runs brainstorm
./scripts/bash/brainstorm.sh "New Feature Ideas"

# Git state after:
# - Current branch: main
# - New commit on main with conversation initialization
# - No new branch created
```

#### Scenario: Main branch does not exist

**Given** a workspace where main branch does not exist
**When** a conversation script is run
**Then** the script MUST create the main branch
**And** proceed with conversation creation on main

---

### Requirement: Conversation scripts SHALL create git tags for conversation boundaries

Conversation scripts MUST create a lightweight git tag when initializing a conversation to mark the conversation start point.

**ID:** `GIT-002` | **Priority:** Medium

#### Scenario: Tag created on conversation initialization

**Given** a user creates a new conversation
**When** the conversation is initialized and committed
**Then** a git tag MUST be created with format `conv/{CONVERSATION_ID}`
**And** the tag MUST point to the initialization commit

**Example:**
```bash
# After running brainstorm script
git tag -l "conv/*"
# Output: conv/001-brainstorm-new-feature-ideas

# Tag points to the conversation initialization commit
git log --oneline conv/001-brainstorm-new-feature-ideas
# a1b2c3d [conversation] Initialize brainstorm: New Feature Ideas
```

#### Scenario: Listing conversation tags chronologically

**Given** multiple conversations have been created
**When** a user lists conversation tags
**Then** tags can be sorted to show conversation history

**Example:**
```bash
git tag -l "conv/*" --sort=-creatordate
# conv/003-plan-architecture
# conv/002-debug-auth-issue
# conv/001-brainstorm-new-feature-ideas
```

---

### Requirement: Users MAY create branches manually for isolation

The system SHALL NOT prevent users from creating their own branches when they need conversation isolation.

**ID:** `GIT-003` | **Priority:** Low

#### Scenario: User creates manual branch before conversation

**Given** a user wants to isolate a specific conversation
**When** they create a branch manually before running a conversation script
**Then** the conversation script SHOULD respect the current branch
**And** commit to the user's branch instead of switching to main

**Example:**
```bash
# User creates their own branch
git checkout -b experiment/risky-idea

# Run conversation script
./scripts/bash/brainstorm.sh "Risky Idea"

# Commits go to experiment/risky-idea branch
```

---

### Requirement: Commit session script SHALL work on any branch

The commit-session.sh script MUST commit conversation changes regardless of which branch is active.

**ID:** `GIT-004` | **Priority:** High

#### Scenario: Committing session on main branch

**Given** the user is on the main branch
**When** they run commit-session.sh
**And** there are uncommitted changes in conversations directory
**Then** the script MUST commit the changes
**And** MUST NOT exit early due to being on main

**Example:**
```bash
# On main branch with changes
git status
# modified: conversations/2025-11-20/001-brainstorm-topic/brainstorm.md

./scripts/bash/commit-session.sh
# Output: Session committed
```

#### Scenario: Committing session with no changes

**Given** the user runs commit-session.sh
**When** there are no uncommitted changes
**Then** the script MUST report "No changes to commit"
**And** exit gracefully

---
