import json
import os
import re

LOG_FILE = "inboxes/supervisor.jsonl"
TASK_DIR = "tasks/archive/2026-02/bench"
EVAL_OUT_DIR = "tasks/2026-02/evaluate"

def get_verified_tasks():
    verified = set()
    if not os.path.exists(LOG_FILE):
        return verified
    
    with open(LOG_FILE, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get('status') == 'verified' or data.get('verdict') in ['PASS', 'FAIL']:
                    t_id = data.get('task_id')
                    if t_id:
                        verified.add(t_id)
            except:
                continue
    return verified

def spawn():
    verified = get_verified_tasks()
    print(f"Already verified: {len(verified)} tasks.")
    
    if not os.path.exists(EVAL_OUT_DIR):
        os.makedirs(EVAL_OUT_DIR)
    
    spawned_count = 0
    for f in os.listdir(TASK_DIR):
        if not f.endswith(".json"):
            continue
        
        task_id = f[:-5]
        if task_id in verified:
            continue
            
        # Check if already has an evaluator (even if not verified)
        # We'll just spawn if not verified to be safe, but we can check tasks/2026-02/evaluate
        if os.path.exists(os.path.join(EVAL_OUT_DIR, f"eval-{task_id}.json")):
            continue

        # Check the task status
        try:
            with open(os.path.join(TASK_DIR, f), 'r') as tf:
                task_data = json.load(tf)
                if task_data.get('status') != 'completed':
                    continue
        except:
            continue

        # Spawn evaluator
        eval_id = f"eval-{task_id}"
        eval_data = {
            "id": eval_id,
            "task_id": task_id,
            "subject": f"Evaluate Benchmark {task_id}",
            "status": "todo",
            "priority": "medium",
            "orchestration": {
                "team": "dotfiles",
                "role_contract": "evaluator"
            },
            "metadata": {
                "target_task_id": task_id
            }
        }
        
        with open(os.path.join(EVAL_OUT_DIR, f"{eval_id}.json"), 'w') as out:
            json.dump(eval_data, out, indent=2)
        spawned_count += 1
        print(f"Spawned evaluator for: {task_id}")

    print(f"Total spawned: {spawned_count}")

if __name__ == "__main__":
    spawn()
