#!/usr/bin/env python3
import json
import os
import subprocess
import glob
from datetime import datetime
import time
import sys
import select
import tty
import termios
import re

# --- High-Fidelity Styling ---
BOLD = "\033[1m"; ITALIC = "\033[3m"; CYAN = "\033[36m"; GREEN = "\033[32m"; YELLOW = "\033[33m"; GREY = "\033[90m"; LIGHT_GREY = "\033[37m"; RESET = "\033[0m"; CLEAR = "\033[2J\033[H"

PROJECT_DIR = os.getcwd()
SEEN_EVENTS = set() 
PULSATE = ["•", "•", "●", "●"] 

def log_event(msg):
    if msg in SEEN_EVENTS: return
    timestamp = datetime.now().strftime('%H:%M:%S')
    with open(f"{PROJECT_DIR}/swarm.log", "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    SEEN_EVENTS.add(msg)

def reconcile_state(tasks, active_sessions):
    updated = False
    for t in tasks:
        tid = t.get("id"); status = t.get("status"); worker_id = f"worker-{tid}"
        log_file = f"/tmp/actor-orchestrator/{worker_id}.log"
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    content = f.read()
                    match = re.search(r"https://github\.com/[^/]+/[^/]+/pull/\d+", content)
                    if match: log_event(f"🔗 Task {tid} PR: {match.group(0)}")
            except: pass
        if status == "in_progress" and worker_id not in active_sessions:
            is_complete = False
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    c = f.read()
                    if "STATUS: COMPLETED" in c or "Final report" in c or "###" in c: is_complete = True
            t["status"] = "completed" if is_complete else "failed"
            task_files = [f for f in os.listdir(f"{PROJECT_DIR}/.tasks/") if f.startswith(tid)]
            if task_files:
                with open(f"{PROJECT_DIR}/.tasks/{task_files[0]}", 'w') as f: json.dump(t, f, indent=2)
                log_event(f"✓ Task {tid} finalized ({t['status'].upper()})")
                updated = True
    return updated

def get_zmx_workers_data():
    try:
        output = subprocess.check_output(["zmx", "list"], text=True)
        workers = {}
        for line in output.splitlines():
            if "worker-" in line:
                name = line.split()[0].split('=')[1]; pid = line.split()[1].split('=')[1]
                log_file = f"/tmp/actor-orchestrator/{name}.log"; thoughts = []
                if os.path.exists(log_file):
                    try:
                        raw = subprocess.check_output(["tail", "-n", "10", log_file], text=True).splitlines()
                        thoughts = [l.strip()[:70] for l in raw if l.strip() and "Tool" not in l and "Loading" not in l][-2:]
                    except: pass
                workers[name] = {"pid": pid, "thoughts": thoughts}
        return workers
    except: return {}

CACHE = {"tasks": [], "workers": {}, "events": []}

def update_data():
    task_files = glob.glob(f"{PROJECT_DIR}/.tasks/*.json"); tasks = []
    for f in task_files:
        try:
            with open(f, 'r') as j: tasks.append(json.load(j))
        except: pass
    zmx_workers = get_zmx_workers_data()
    reconcile_state(tasks, list(zmx_workers.keys()))
    recent_events = []
    if os.path.exists(f"{PROJECT_DIR}/swarm.log"):
        raw_events = subprocess.check_output(["tail", "-n", "10", f"{PROJECT_DIR}/swarm.log"], text=True).splitlines()
        recent_events = list(reversed(raw_events))
    CACHE["tasks"] = tasks; CACHE["workers"] = zmx_workers; CACHE["events"] = recent_events

def render_dashboard(frame):
    sys.stdout.write(CLEAR)
    print(f"{BOLD}{CYAN}┌────────────────────────────────────────────────────────────────────────┐{RESET}")
    print(f"{BOLD}{CYAN}│  🤖 SOUL OS | SWARM COMMAND CENTER | {datetime.now().strftime('%H:%M:%S')}             │{RESET}")
    print(f"{BOLD}{CYAN}└────────────────────────────────────────────────────────────────────────┘{RESET}")
    print(f"\n{BOLD}👷 ACTIVE WORKSTREAMS{RESET}")
    if not CACHE["workers"]: print(f"  {GREY}└─ (Dormant - Monitoring Blackboard...){RESET}")
    else:
        pulse_char = PULSATE[frame % len(PULSATE)]
        for name, data in CACHE["workers"].items():
            print(f"  {LIGHT_GREY}{pulse_char} {name}{RESET} (PID:{data['pid']})")
            for line in data['thoughts']: print(f"    {ITALIC}{GREY}│ {line}{RESET}")
    print(f"\n{BOLD}📋 TASK LEDGER (LAST 10 ADDED){RESET}")
    print(f"  {'ID':<5} {'TITLE':<35} {'STATUS':<15} {'PRIO':<8}")
    print(f"  {GREY}" + "-" * 67 + f"{RESET}")
    status_map = {"IN-PROGRESS": 0, "IN_PROGRESS": 0, "BACKLOG": 1, "TODO": 1, "COMPLETED": 2, "FAILED": 3}
    # SORT: Active Tasks first, then highest ID (newest) first
    tasks = sorted(CACHE["tasks"], key=lambda x: (status_map.get(x.get('status', '').upper(), 4), -int(x.get('id', '0')) if x.get('id','').isdigit() else 0))
    # EXACT LIMIT: 10 items
    for t in tasks[:10]:
        tid = t.get('id', '???'); title = (t.get('title', '')[:32] + '..') if len(t.get('title', '')) > 32 else t.get('title', '')
        raw_status = t.get('status', '').upper(); icon = f"{GREY}○{RESET}"; color = RESET
        if "PROGRESS" in raw_status:
            icon = f"{LIGHT_GREY}{PULSATE[frame % len(PULSATE)]}{RESET}"
            color = LIGHT_GREY; status_text = "IN-PROGRESS"
        elif raw_status == "COMPLETED": icon = f"{GREEN}✓{RESET}"; color = GREEN; status_text = "COMPLETED"
        elif raw_status == "FAILED": icon = f"{YELLOW}!{RESET}"; color = YELLOW; status_text = "FAILED"
        else: status_text = "BACKLOG"
        print(f"  {icon} {tid:<4} {color}{title:<35}{RESET} {status_text:<15} {t.get('priority','').upper():<8}")
    print(f"\n{BOLD}🔔 SYSTEM EVENTS (LATEST FIRST){RESET}")
    for event in CACHE["events"]: print(f"  {GREY}• {event}{RESET}")
    print(f"\n  {BOLD}{CYAN}[S] STREAM LOG | [Q] QUIT | [R] REFRESH{RESET}")

def main():
    old_settings = termios.tcgetattr(sys.stdin); frame = 0; last_data_update = 0
    try:
        tty.setcbreak(sys.stdin.fileno())
        while True:
            if time.time() - last_data_update > 2: update_data(); last_data_update = time.time()
            render_dashboard(frame); frame += 1
            start_wait = time.time()
            while time.time() - start_wait < 0.25:
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    c = sys.stdin.read(1).lower()
                    if c == 'q': return
                    elif c == 'r': last_data_update = 0; break
                    elif c == 's':
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                        task_id = input(f"\n{BOLD}{CYAN}▶ Enter Task ID: {RESET}")
                        os.system(f"bash {os.path.dirname(os.path.abspath(__file__))}/swarm-stream {task_id}")
                        tty.setcbreak(sys.stdin.fileno()); last_data_update = 0; break
                time.sleep(0.05)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        print(f"\n{GREY}--- Swarm Command Center Offline --{RESET}\n")

if __name__ == "__main__":
    try: main() 
    except KeyboardInterrupt: sys.exit(0)