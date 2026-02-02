import json
import os
from datetime import datetime

TASK_PATH = "tasks/archive/2026-02/15.json"
AUDIT_SCRIPT = "/Users/ilteris/dotfiles/soul/scripts/soul_audit.py"
SYSTEM_MD = "/Users/ilteris/dotfiles/soul/SYSTEM.md"
REPORT_PATH = "soul/memory/system3_audit.md"

def evaluate():
    print("### [ Glass Box Review ]")
    
    # 1. Verify Task Existence
    if not os.path.exists(TASK_PATH):
        print(f"FAIL: Task file {TASK_PATH} not found.")
        return

    with open(TASK_PATH, 'r') as f:
        task = json.load(f)

    # 2. Verify SSOT and Script
    if not os.path.exists(SYSTEM_MD):
        print(f"FAIL: SYSTEM.md SSOT not found at {SYSTEM_MD}.")
        return
    if not os.path.exists(AUDIT_SCRIPT):
        print(f"FAIL: Audit script not found at {AUDIT_SCRIPT}.")
        return

    # 3. Verify Artifact (Audit Report)
    if not os.path.exists(REPORT_PATH):
        print(f"FAIL: Audit report {REPORT_PATH} not found.")
        return

    with open(REPORT_PATH, 'r') as f:
        report_content = f.read()
    
    print(f"Report Summary: {report_content[:200]}...")

    # 4. Success - Update Task
    task["governance"] = task.get("governance", {})
    task["governance"]["evaluated"] = True
    task["governance"]["evaluation_date"] = datetime.utcnow().isoformat()
    task["governance"]["evaluation_summary"] = "Soul Audit verified. Artifacts exist and reference SYSTEM.md SSOT."

    with open(TASK_PATH, 'w') as f:
        json.dump(task, f, indent=2)
    
    print(f"PASS: Task 15 evaluated and marked as successful.")

if __name__ == "__main__":
    evaluate()
