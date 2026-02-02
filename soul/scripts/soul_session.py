#!/Users/ilteris/soul_venv/bin/python3
import json
import os
import sys
from datetime import datetime

SESSION_LOG = "soul/registry/telemetry/sessions.json"

def log_session(task_id, status, verdict="PASS", artifact=""):
    session = {
        "timestamp": datetime.now().isoformat(),
        "task_id": task_id,
        "status": status,
        "verdict": verdict,
        "artifact": artifact
    }
    
    sessions = []
    if os.path.exists(SESSION_LOG):
        with open(SESSION_LOG, 'r') as f:
            try:
                sessions = json.load(f)
            except json.JSONDecodeError:
                pass
    
    sessions.append(session)
    
    os.makedirs(os.path.dirname(SESSION_LOG), exist_ok=True)
    with open(SESSION_LOG, 'w') as f:
        json.dump(sessions, f, indent=2)
    print(f"Session logged: {task_id} [{verdict}]")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        task_id = sys.argv[1]
        status = sys.argv[2]
        verdict = sys.argv[3] if len(sys.argv) > 3 else "PASS"
        artifact = sys.argv[4] if len(sys.argv) > 4 else ""
        log_session(task_id, status, verdict, artifact)
    else:
        # Default behavior for task 16 (legacy)
        log_session("16", "verified", "PASS", "soul/scripts/system3_audit.py")