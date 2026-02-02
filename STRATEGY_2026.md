# STRATEGY_2026: The Unix-for-AI Ecosystem

## 1. Vision & Mandate
The 2026 Strategy transitions from "AI-as-a-Service" to "AI-as-Infrastructure." We are building **Soul OS**, a machine-agnostic, persistent, and hierarchical orchestration framework that treats LLMs as standard Unix processes.

## 2. Core Architecture: The Actor-Orchestrator
The system follows a pure **Actor Model** pattern, ensuring isolation, scalability, and deterministic state management.

### A. Execution Layer
- **Engine**: `gemini-cli` (High-fidelity agent logic).
- **Persistence**: `zmx` (Persistent terminal sessions with session-id management).
- **Isolation**: Unique workspace directories (`/tmp/<task-id>/`) to prevent filesystem crosstalk.

### B. Orchestration Layer
- **Supervisor**: The high-level governor that polls the blackboard and spawns specialized actors.
- **Worker**: Execution-focused agents that perform Atomic Contributions (Clone -> Branch -> Implement -> Verify -> PR).
- **Evaluator**: Heuristic termination gates that verify artifact fidelity before archival.

### C. State & Memory Layer
- **Blackboard**: `TODO.md` serves as the single source of truth for project state.
- **Inboxes**: Asynchronous signaling via `inboxes/supervisor.jsonl`.
- **Semantic Memory**: Episodic logs in `soul/memory/` providing a queryable history of system evolution.

## 3. Operational Protocols (The Soul Framework)
- **S1: Interleaved Reflection**: Mandatory audit blocks at the start of every turn to detect protocol drift.
- **S2: Glass Box Review**: Full transparency of command execution and artifact injection.
- **S3: Reaper Protocol**: Automated termination of `zmx` sessions upon task completion to maintain system hygiene.
- **S4: Shebang Portability**: Standardized execution environments via `soul_venv` alignment.

## 4. 2026 Milestones (Snapshot: 2026-02-01)
- **Benchmarking**: Successfully executed 74 parallel tasks with a **94.6% PASS rate**.
- **System Integrity**: Achieved **100% protocol adherence** as verified by the `system3_audit.py` engine.
- **Dormancy Management**: Implemented "Steady-State Dormancy" where the Supervisor operates at minimal overhead until a blackboard trigger occurs.

## 5. Roadmap: Q1-Q2 2026
1. **SwarmOS Kernel**: Native integration of `zmx` primitives into the `gemini-cli` toolset.
2. **Knowledge Graph Synthesis**: Automated transformation of `soul/memory/` into queryable Obsidian vaults.
3. **Force Multiplication**: Scaling the actor-orchestrator to handle multi-repository dependencies (FoG Infrastructure).

---
*Prepared by Worker-024 (Teddy Soul) for Sir.*
