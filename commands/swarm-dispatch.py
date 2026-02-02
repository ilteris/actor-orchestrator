#!/usr/bin/env python3
import json
import os
import subprocess
import glob
from datetime import datetime

ORCHESTRATOR_DIR = "/Users/ilteris/Code/actor-orchestrator"
PROJECT_DIR = "/Users/ilteris/Code/swarm-test-bed"
TMP_DIR = "/tmp/actor-orchestrator"

os.makedirs(TMP_DIR, exist_ok=True)

def log_event(msg):
    timestamp = datetime.now().strftime('%H:%M:%S')
    with open(f"{PROJECT_DIR}/swarm.log", "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

def get_zmx_sessions():
    try:
        output = subprocess.check_output(["zmx", "list"], text=True)
        return [line.split()[0].split('=')[1] for line in output.splitlines() if "=" in line]
    except: return []

def reconcile():
    active_sessions = get_zmx_sessions()
    task_files = glob.glob(f"{PROJECT_DIR}/.tasks/*.json")
    for f_path in task_files:
        try:
            with open(f_path, 'r') as f: task = json.load(f)
            tid = task.get("id"); status = task.get("status"); worker_id = f"worker-{tid}"
            if status == "in_progress" and worker_id not in active_sessions:
                log_file = f"{TMP_DIR}/{worker_id}.log"
                is_complete = False
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        content = f.read()
                        if "STATUS: COMPLETED" in content or "Final report" in content or "###" in content:
                            is_complete = True
                task["status"] = "completed" if is_complete else "failed"
                with open(f_path, 'w') as f: json.dump(task, f, indent=2)
                log_event(f"✓ Task {tid} finalized ({task['status'].upper()})")
        except: pass

def dispatch():
    task_files = glob.glob(f"{PROJECT_DIR}/.tasks/*.json")
    for f_path in task_files:
        try:
            with open(f_path, 'r') as f: task = json.load(f)
            if task.get("status") == "backlog":
                tid = task.get("id")
                log_event(f"⚡ Dispatching Task {tid}...")
                task["status"] = "in_progress"
                with open(f_path, 'w') as f: json.dump(task, f, indent=2)
                
                script_path = f"{TMP_DIR}/runner_{tid}.sh"
                log_path = f"{TMP_DIR}/worker-{tid}.log"
                
                with open(script_path, 'w') as s:
                    s.write("#!/bin/bash\n")
                    s.write("export NODE_NO_WARNINGS=1\n") # Silence Node warnings
                    s.write(f"cd {PROJECT_DIR}\n")
                    
                    # SILENCE MODE: Use grep -v to strip out the visual noise
                    # We capture stdout/stderr, filter them, and send to the log
                    worker_cmd = (
                        f"echo 'ACTIVATE SKILL: worker. task {tid}.' | "
                        f"gemini --yolo --extensions actor-orchestrator --include-directories {ORCHESTRATOR_DIR} 2>&1 | "
                        f"grep -vE \"YOLO|Loading extension|already registered|punycode|DEP0040\" > {log_path}"
                    )
                    s.write(f"{worker_cmd}\n")
                    
                    # RELIABILITY: Give the system time to flush the log before killing
                    s.write("sleep 3\n")
                    s.write(f"rm -- \"$0\"\n")
                    s.write(f"zmx kill worker-{tid}\n")
                
                os.chmod(script_path, 0o755)
                subprocess.run(f"zmx run worker-{tid} {script_path}", shell=True)
                log_event(f"👷 worker-{tid} launched (Pristine Ghost Mode).")
        except Exception as e:
            log_event(f"❌ Dispatch Error {tid}: {str(e)}")

if __name__ == "__main__":
    reconcile()
    dispatch()
