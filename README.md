# Swarm Test Bed

This project is a demonstration of the **Actor-Orchestrator** infrastructure.

## Features

### Mock Feature (`feature.py`)
A simple Python script that demonstrates cross-task implementation and documentation.
- **hello_world()**: Prints a greeting from the Swarm Actor-Orchestrator.

## Orchestration Details
The project is managed via a hierarchical swarm of agents:
- **Supervisor**: Monitors the `tasks/` directory and delegates work.
- **Workers**: Execute specific tasks (Audit, Feature Implementation, Documentation).

## Usage
To run the mock feature:
```bash
python3 feature.py
```
