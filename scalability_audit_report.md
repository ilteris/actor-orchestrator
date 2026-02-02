# Scalability and Performance Audit Report
Task: 007-scalability-audit
Date: 2026-02-01

## 1. Executive Summary
The scalability benchmark revealed critical failure modes in the SwarmOS Actor-Orchestrator when handling concurrent tasks. While the system successfully processed 50% of the initial high-volume batch (`bench-1769954124`), it exhibited "Ghost Completions" (status marked completed without artifacts) and "Paradoxical Non-Existence" (workers unable to find their own task files) in subsequent batches.

## 2. Identified Bottlenecks & Anomalies

### A. Ghost Completions (Race Conditions)
- **Observation**: Tasks `bench-1769954124-2`, `5`, `6`, `7`, and `8` were moved to the archive and marked as `completed` in the JSON state, but no physical artifacts (logs/reports) were created.
- **Hypothesis**: The worker's "Task Finish" logic likely updates the JSON and moves the file to `archive/` before ensuring file buffers are flushed or before the cleanup protocol erroneously deletes un-synced data.
- **Impact**: High. False positives in task completion status break the reliability of the blackboard system.

### B. State Desynchronization (File System Latency)
- **Observation**: Batch `bench-1769954158` saw multiple worker failures where workers reported: *"Task file tasks/bench-1769954158-x.json not found."*
- **Hypothesis**: `scaling_bench.py` appends to `inboxes/supervisor.jsonl` immediately after writing the `.json` file. On high-concurrency or specific OS configurations, the Supervisor may trigger a worker before the filesystem has fully committed the `.json` file, or the Supervisor moves the file to `tmp/` while the worker is still initializing.
- **Impact**: Critical. Prevents horizontal scaling.

### C. Supervisor Saturation
- **Observation**: Timestamps in `evaluation_report_bench-1769954124-*` show a processing spread from 09:08 to 09:14 for 10 tasks.
- **Hypothesis**: The Supervisor appears to be processing evaluations/task moves sequentially rather than in parallel, or the overhead of `zmx` session creation is significant.
- **Impact**: Moderate. limits "burst" capacity.

## 3. Suggested Architectural Improvements

### 1. Robustness: "Commit-then-Signal" Protocol
- **Change**: Implement a mandatory `fsync()` or a brief verification loop after creating task files before signaling the Supervisor.
- **Verification**: Workers should verify the presence of their assigned task file in multiple locations (`tasks/`, `tmp/<id>/`) before failing.

### 2. Isolation: Worker-Owned State
- **Change**: Instead of the Supervisor moving files to `tmp/`, the Worker should be responsible for "claiming" a task by moving it to its own isolated workspace. This reduces the Supervisor's role to a pure dispatcher.

### 3. Reliability: Mandatory Artifact Check
- **Change**: The `update_task` tool should require a list of `produced_artifacts` (file paths). If these files do not exist, the tool should refuse to set the status to `completed`.

### 4. Monitoring: Swarm Table Refinement
- **Change**: Add a "Ghost Detection" column to the `swarm-table` that flags tasks marked `completed` that lack expected artifacts in the `logs/` directory.

## 4. Conclusion
The Actor-Orchestrator is currently "unstable" at concurrency levels >= 10. The priority for the next iteration must be **State Reliability** over **Feature Expansion**.

---
*Audit performed by Teddy (Architect)*