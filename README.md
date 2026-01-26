# Actor-Orchestrator: Agentic Swarm Infrastructure

A "Unix-for-AI" architecture for managing concurrent, autonomous agent workstreams using `gemini-cli` and `zmx`.

## What is it?
The Actor-Orchestrator is a hierarchical agentic system that transforms a flat `TODO.md` file into an active project blackboard. It uses an **Actor Model** pattern to delegate tasks to isolated sub-agents (Workers) that operate in their own persistent terminal sessions.

## Why use it?
- **Cognitive Multiplier**: Offload high-throughput implementation "slop" to parallel agents while you maintain high-level architectural oversight.
- **Physical Isolation**: Each worker runs in its own `zmx` pane with a unique temporary workspace, preventing file-system conflicts and logical crosstalk.
- **Human-in-the-Loop**: Integrated PR-based review gates ensure no code is merged without your approval.
- **Zero Zombies**: The "Reaper" protocol automatically terminates terminal sessions as soon as an agent completes its task.

## The Hierarchy
1. **Meta-Orchestrator (Teddy)**: Bootstraps the environment and launches the Supervisor.
2. **Supervisor Actor**: Reads the `TODO.md` blackboard and delegates tasks to Workers.
3. **Worker Actors**: Execute specific tasks (Clone -> Branch -> Implement -> Verify -> PR).

---

## Step-by-Step Instructions

### 1. Installation & Setup
Ensure you have the core dependencies installed:
```bash
# Install zmx (The persistent terminal layer)
brew tap neurosnap/tap && brew install zmx

# Install gemini-cli (The agent logic)
brew install gemini-cli

# Pre-authorize tools (Important for headless automation)
# Ensure your ~/.gemini/settings.json includes these in tools.core:
# "run_shell_command", "write_todos", "read_file", "list_files", "delegate_to_agent"
```

### 2. Linking the Extension
Link the orchestrator logic from your Soul to the Gemini CLI:
```bash
gemini extensions link ~/dotfiles/soul/projects/actor-orchestrator
```

### 3. Launching a Swarm
To start a swarm in any project directory:

1. **Create a Blackboard**:
   Create a `TODO.md` in your project root with your tasks:
   ```markdown
   # Project Tasks
   - [ ] Implement user authentication.
   - [ ] Generate API documentation.
   ```

2. **Trigger Orchestration**:
   ```bash
   gemini --yolo "Activate the orchestrate skill. Bootstrap the project and launch the swarm."
   ```

### 4. Monitoring & Review
- **Monitor Supervisor**: `zmx attach supervisor`
- **Monitor Workers**: `zmx list` to see active workers, then `zmx attach <worker-id>`.
- **Review Work**: Once a worker finishes, it will append a Pull Request link to your `TODO.md`. Review and merge the PR via `gh pr view`.

---

## Technical Specs
- **Isolation Layer**: `./tmp/<task-id>/`
- **Signaling**: Synchronous tool returns + asynchronous `TODO.md` polling.
- **Verification**: Built-in support for Google Chrome MCP for UI testing.
