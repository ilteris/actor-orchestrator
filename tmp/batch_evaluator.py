import json
import os
import subprocess
import time

MISSING_EVALS_FILE = "/tmp/final_missing_evals.txt"
TASK_ARCHIVE_DIR = "tasks/archive/2026-02/bench"
LOG_DIR = "/tmp/actor-orchestrator"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

with open(MISSING_EVALS_FILE, "r") as f:
    task_ids = [line.strip() for line in f if line.strip()]

print(f"Found {len(task_ids)} tasks missing evaluation.")

for task_id in task_ids:
    task_file = os.path.join(TASK_ARCHIVE_DIR, f"{task_id}.json")
    if not os.path.exists(task_file):
        print(f"Warning: Task file for {task_id} not found at {task_file}")
        continue
    
    # Spawn Evaluator
    session_name = f"eval-{task_id}"
    command = f"zmx run {session_name} cd {os.getcwd()} && gemini --yolo evaluator 'ACTIVATE SKILL: evaluator. task {task_id} contract evaluator'"
    log_file = os.path.join(LOG_DIR, f"{session_name}.log")
    
    print(f"Spawning evaluator for {task_id}...")
    full_command = f"{command} > {log_file} 2>&1"
    subprocess.Popen(["bash", "-c", full_command], preexec_fn=os.setpgrp)
    
    # Simple rate limiting to avoid overwhelming the system
    time.sleep(2)

print("Batch spawning complete.")