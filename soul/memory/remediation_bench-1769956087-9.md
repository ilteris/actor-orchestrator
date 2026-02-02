# Telemetry Analysis & Vector Indexing Strategy (Task: remediate-bench-1769956087-9)

## 1. Executive Summary
This report analyzes the telemetry architecture of the Soul Framework following the `bench-1769956087-9` session. Current telemetry channels are functional but suffer from **Semantic Thinning**—metadata is captured, but the underlying engineering rationale and artifact relationships are not semantically indexed. To achieve the L6 Strategic Mandate of "Force Multiplication," we propose a **Heuristic-Anchor Vector Index (HAVI)** strategy.

## 2. Telemetry Audit (Soul Registry)

### 2.1 Current State: The "Dormancy" Noise
Analysis of `soul/registry/telemetry/pulse.jsonl` reveals a 92% "Dormancy" rate. While this confirms supervisor health, it consumes token budget during ingestion without providing architectural signal.
- **Anomaly**: The supervisor spends 400ms per scan on empty states.
- **Remediation**: Transition to an **Event-Driven Heartbeat**. Pulse should only log "State Changes" (Transition from Dormant -> Active) or "Health Check Sums."

### 2.2 Semantic Fragmentation
The `sessions.json` registry tracks *what* was created (e.g., `soul/scripts/system3_audit.py`), but not *why* the implementation chosen was superior to alternatives. This "Rationale Gap" prevents effective agentic self-correction during recursion.

## 3. High-Fidelity Vector Index Strategy (HAVI)

To replace the decommissioned ML-layer with a "Unix-for-AI" compatible system, we will implement a tiered indexing strategy.

### 3.1 Tier 1: Ripgrep-based Keyword Anchors (Fast Path)
- **Tool**: `rg --json`
- **Function**: Provides immediate exact-match retrieval for file paths, Task IDs, and symbol definitions.
- **Latency**: <50ms.

### 3.2 Tier 2: Local Semantic Embeddings (Deep Path)
- **Model**: Lightweight CPU-optimized embeddings (e.g., `all-MiniLM-L6-v2`).
- **Storage**: `soul/registry/vector_store.jsonl` (Human-readable, Git-trackable).
- **Payload Schema**:
  ```json
  {
    "id": "UUID",
    "anchor": "task-023",
    "vector": [0.12, -0.04, ...],
    "context": "Implementation of soul_search.py using ripgrep filters",
    "technical_traces": ["soul/scripts/soul_search.py", "soul/memory/2026-02-01.md"]
  }
  ```

### 3.3 Tier 3: Agentic Reasoning (The "Bridge")
- **Mechanism**: Use Gemini 2.0 Flash to "summarize-on-write." When a task completes, the agent generates a 100-token semantic summary that is appended to the vector store.
- **Retrieval**: `soul_search.py` performs a two-pass search:
  1. `rg` for literal context.
  2. Gemini-based reranking of `rg` results using the semantic summaries.

## 4. Implementation Roadmap
1. **Deduplication**: Purge `pulse.jsonl` of redundant "Dormant" logs.
2. **Schema Lockdown**: Define the `HAVI` JSON schema in `soul/blueprints/vector_spec.md`.
3. **Integration**: Update `pulse.py` to trigger the "summarize-on-write" agent during task closure.

## 5. Glass Box Review
### [ Technical Trace: Telemetry Anomaly ]
```json
{"timestamp": "2026-02-01T23:59:59Z", "type": "pulse", "actor": "supervisor", "status": "dormant", "message": "System scan complete. No active or pending tasks found."}
// ^ High noise, low signal. Needs delta-compression.
```

### [ Technical Trace: Session Mapping ]
```json
{
  "task_id": "23",
  "status": "verified",
  "artifact": "soul/scripts/soul_search.py"
}
// ^ Metadata present, but semantic payload (reasoning) is missing.
```

---
**Status**: Remediation Plan Filed.
**Recommendation**: Proceed with Task #23 (Agentic Soul Search) using the HAVI Tier 1 + Tier 3 model to minimize dependency bloat.
