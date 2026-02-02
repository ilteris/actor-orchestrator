import json
import os
import subprocess

def evaluate_task_16():
    print("### [ Evaluation: Task 16 ]")
    
    # 1. Verify existence of script
    script_path = "soul/scripts/system3_audit.py"
    if os.path.exists(script_path):
        print(f"PASS: {script_path} exists.")
    else:
        print(f"FAIL: {script_path} missing.")
        return

    # 2. Check for audit output in memory
    audit_log = "soul/memory/system3_audit.md"
    if os.path.exists(audit_log):
        print(f"PASS: {audit_log} found.")
    else:
        print(f"FAIL: {audit_log} missing.")
        # We'll continue to see if we can run the script now.

    # 3. Execution Test (Dry Run / Help)
    try:
        result = subprocess.run(["python3", script_path, "--help"], capture_output=True, text=True)
        if result.returncode == 0:
            print("PASS: Script execution (help) successful.")
        else:
            print(f"FAIL: Script execution failed with code {result.returncode}")
            print(result.stderr)
    except Exception as e:
        print(f"FAIL: Execution error: {e}")

evaluate_task_16()
