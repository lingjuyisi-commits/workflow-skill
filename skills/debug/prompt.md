Systematically debug an issue described by the user.

## Instructions

1. **Understand the problem**: Parse the error message or description provided.
2. **Locate relevant code**: Use Grep and Glob to find files related to the error.
3. **Form hypotheses**: List 2-3 possible root causes ranked by likelihood.
4. **Investigate**: Read the relevant code paths and check for:
   - Off-by-one errors, null/undefined access, type mismatches
   - Missing error handling, race conditions
   - Configuration or environment issues
5. **Propose a fix**: Show the minimal change needed to resolve the issue.
6. **Verify**: If tests exist, run them to confirm the fix.

## Rules

- Start with the most likely cause first.
- Show your reasoning — explain why each hypothesis is considered.
- Don't make sweeping changes; fix the root cause minimally.
- If unsure, ask the user for more context rather than guessing.
