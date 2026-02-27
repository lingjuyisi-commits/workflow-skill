---
allowed-tools:
- Bash
- Read
- Glob
- Grep
argument-hint: <pr-number>
description: Review a GitHub pull request and provide structured feedback
name: review-pr
user-invocable: true
---

Review a GitHub pull request and provide structured feedback.

## Instructions

1. Use `gh pr view <number> --json title,body,files,additions,deletions` to get PR metadata.
2. Use `gh pr diff <number>` to get the full diff.
3. Analyze the changes for:
   - Correctness and potential bugs
   - Code style and consistency
   - Security concerns
   - Performance implications
   - Test coverage
4. Provide a structured review with sections:
   - **Summary**: Brief overview of changes
   - **Strengths**: What's done well
   - **Concerns**: Issues that should be addressed
   - **Suggestions**: Optional improvements
   - **Verdict**: Approve / Request Changes / Comment

## Rules

- Be constructive and specific — reference file names and line numbers.
- Distinguish between blocking issues and nice-to-haves.
- If the PR is small and clean, keep the review concise.
