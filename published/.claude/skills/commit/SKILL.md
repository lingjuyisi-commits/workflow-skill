---
allowed-tools:
- Bash
- Read
- Glob
- Grep
argument-hint: '[message]'
description: Create well-formatted git commits with conventional commit messages
name: commit
user-invocable: true
---

Create a git commit for the current staged changes.

## Instructions

1. Run `git status` to see the current state of the working tree.
2. Run `git diff --cached` to review staged changes.
3. If no changes are staged, inform the user and suggest staging changes first.
4. Analyze the staged changes and generate a commit message following the Conventional Commits format:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `refactor:` for code refactoring
   - `test:` for adding or updating tests
   - `chore:` for maintenance tasks
5. If the user provided a message hint via the argument, use it as guidance for the commit message.
6. Create the commit using `git commit -m "<message>"`.
7. Show the result with `git log --oneline -1`.

## Rules

- Keep the subject line under 72 characters.
- Use imperative mood in the subject line (e.g., "add feature" not "added feature").
- Do not amend existing commits unless explicitly asked.
- Always show the diff summary before committing.
