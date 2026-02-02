---
name: worker
description: Distributed Engineer with mandatory Git/PR lifecycle.
---

# SKILL: Worker (The Atomic Contributor)

## Operational Protocol
...
5. **GIT SUBMIT**:
   - `git push origin task-<ID>-<slug>`
   - **MANDATORY TOOL CALL**: `gh pr create ...`
   - **MANDATORY LOG OUTPUT**: You MUST print the URL of the created PR exactly as follows:
     `PULL_REQUEST_URL: <URL>`
...

## Constraints
- **FAILURE MODE**: If you finish a task without creating a PR, the task is incomplete.
- **DASHBOARD HOOK**: The system events scraper depends on the `PULL_REQUEST_URL: ` string.