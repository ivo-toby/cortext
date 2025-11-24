# Proposal: Simplify Git Workflow to Main-Only

## Summary

Replace the branch-per-conversation model with a simpler main-only approach where all conversations commit directly to the main branch, with optional git tags to mark conversation boundaries.

## Motivation

The current implementation creates a new git branch for each conversation (`conversation/{ID}-{TYPE}-{TOPIC}`). This causes several problems:

1. **Branch fragmentation** - Branches are never merged back to main, leading to unbounded growth (potentially 1,000+ orphan branches per year)
2. **No cleanup mechanism** - No automation exists to merge or delete conversation branches
3. **Unnecessary complexity** - For single-user knowledge workspaces, branch isolation provides no real benefit
4. **User burden** - Users would need to manually merge branches, which defeats the purpose of automation

## Proposed Solution

### Main-Only Commits

All conversation scripts will:
1. Stay on the `main` branch (or create it if needed)
2. Commit conversation initialization directly to main
3. All subsequent conversation commits go to main

### Tag-Based Boundaries

To preserve the ability to identify conversation boundaries:
1. Create a git tag when a conversation starts: `conv-start/{ID}`
2. Optionally create a tag when archived: `conv-end/{ID}`
3. Tags are lightweight and don't cause fragmentation

### User Control

Users who need isolation can:
1. Manually create a branch before starting a conversation
2. Use standard git workflows for their specific needs

## Scope

### In Scope
- Modify all conversation bash scripts (brainstorm, debug, plan, learn, meeting, review)
- Update common.sh utility functions
- Update commit-session.sh to work on main
- Add optional tagging for conversation start
- Update workspace-status.sh to not depend on branches
- Update project documentation

### Out of Scope
- Migration of existing conversation branches (users can merge manually if desired)
- Changes to MCP server or RAG indexing
- Changes to conversation templates

## Benefits

1. **No fragmentation** - All commits on main, clean linear history
2. **Simpler mental model** - No branch management needed
3. **Always searchable** - All content immediately available in main
4. **RAG always current** - Embeddings reflect the single source of truth
5. **Easy navigation** - `git log` shows complete history

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| No isolation for experiments | Users can manually create branches when needed |
| Can't easily discard a conversation | Use `git revert` or tags to identify commit ranges |
| Concurrent sessions interleave | Rare for single-user; tag boundaries help identify |

## Success Criteria

1. Conversation scripts commit to main branch only
2. No new conversation branches are created automatically
3. Git tags mark conversation start points
4. All existing functionality (search, RAG indexing) continues to work
5. Documentation updated to reflect new workflow
