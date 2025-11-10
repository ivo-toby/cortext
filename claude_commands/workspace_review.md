---
description: Conduct a code or design review
tags: [workspace, review, code-review]
---

# Workspace Review

You are helping the user conduct a code or design review in their Cortext workspace.

## Your Task

1. **Get the review title**
   - Ask what's being reviewed
   - Example: "What are you reviewing?"

2. **Run the review script**
   ```bash
   .workspace/scripts/bash/review.sh "<review-title>"
   ```

   This will:
   - Create a new conversation directory with auto-incremented ID
   - Create a git branch for this conversation
   - Copy the review template
   - Make an initial commit

3. **Conduct a thorough review**

   **Understand Context**
   - What's being reviewed and why
   - What are the goals
   - What should you focus on

   **Assess Quality**
   - Correctness and logic
   - Code quality (readability, naming, structure)
   - Performance implications
   - Security considerations
   - Testing coverage
   - Documentation clarity
   - Maintainability

   **Provide Feedback**
   - Categorize: Critical / Major / Minor
   - Be specific about location (file:line)
   - Explain the problem, not just point it out
   - Suggest concrete improvements
   - Provide examples when helpful
   - Balance criticism with recognition of strengths

   **Make Recommendations**
   - Must-have changes (blocking)
   - Should-have changes (strongly recommended)
   - Nice-to-have changes (optional improvements)

4. **Document the review**
   - Overall assessment and rating
   - Detailed feedback by category
   - Questions for the author
   - Alternative approaches if applicable
   - Learning points and positive patterns
   - Final verdict with conditions

## Review Principles

**Be Constructive**
- Focus on the code, not the person
- Assume good intent
- Explain "why" for feedback
- Suggest solutions, not just problems
- Recognize good work

**Be Specific**
- Reference exact locations
- Provide concrete examples
- Explain impact of issues
- Suggest specific improvements

**Be Balanced**
- Note strengths and areas for improvement
- Distinguish between opinions and best practices
- Prioritize feedback (not everything is critical)

## Review Checklist

**Code Reviews**
- [ ] Logic and correctness
- [ ] Edge cases handled
- [ ] Error handling
- [ ] Performance
- [ ] Security vulnerabilities
- [ ] Code style and conventions
- [ ] Naming and readability
- [ ] Tests and coverage
- [ ] Documentation

**Design Reviews**
- [ ] Meets requirements
- [ ] Architectural soundness
- [ ] Scalability considerations
- [ ] Security model
- [ ] API design
- [ ] Data model
- [ ] Dependencies
- [ ] Operational considerations

## When Complete

- Summarize overall assessment
- Provide clear verdict (approve/request changes)
- List must-do action items
- Commit the review
- Share feedback with author
- Follow up on changes if needed
