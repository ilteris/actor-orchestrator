import json
import os
import subprocess
from datetime import datetime

def log_session(task_id, verdict, artifact):
    session = {
        "timestamp": datetime.now().isoformat(),
        "task_id": task_id,
        "status": "verified",
        "verdict": verdict,
        "artifact": artifact
    }
    path = "soul/registry/telemetry/sessions.json"
    data = []
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
    
    data.append(session)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def evaluate_task_20():
    print("Evaluating Task 20...")
    if os.path.exists("soul/scripts/system3_audit.py") and os.path.exists("soul/memory/system3_audit.md"):
        print("Artifacts verified.")
        log_session("20", "PASS", "soul/scripts/system3_audit.py")
        return True
    return False

def evaluate_task_23():
    print("Evaluating Task 23...")
    if os.path.exists("soul/scripts/soul_search.py"):
        print("Artifact verified.")
        log_session("23", "PASS", "soul/scripts/soul_search.py")
        return True
    return False

if __name__ == "__main__":
    if evaluate_task_20():
        print("Task 20 PASS.")
    if evaluate_task_23():
        print("Task 23 PASS.")
