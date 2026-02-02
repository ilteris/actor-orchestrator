import json
import os
import time
import sys

TASK_DIR = "tasks"
INBOX_FILE = "inboxes/supervisor.jsonl"

def is_recursive_context():
    """Check if we are running inside a tmp directory already."""
    cwd = os.getcwd()
    # Simple check for 'tmp' in the path to avoid running inside worker workspaces
    if '/tmp/' in cwd or cwd.endswith('/tmp'):
        return True
    return False

def create_task(task_id):
    # Logic to prevent spawning tasks from inside a worker's tmp space
    if is_recursive_context():
        print(f"[!] Warning: Refusing to create task {task_id} from recursive context: {os.getcwd()}")
        return

    task = {
        "id": task_id,
        "title": f"Bench Task {task_id}",
        "description": f"Scaling benchmark sub-task {task_id}",
        "status": "pending",
        "contract": "explorer",
        "blocked_by": [],
        "priority": "low"
    }
    
    if not os.path.exists(TASK_DIR):
        os.makedirs(TASK_DIR)
        
    with open(f"{TASK_DIR}/{task_id}.json", "w") as f:
        json.dump(task, f, indent=2)
    
    # Signal supervisor
    if os.path.exists(INBOX_FILE):
        with open(INBOX_FILE, "a") as f:
            f.write(json.dumps({"type": "TASK_ADDED", "task_id": task_id}) + "\n")

def run_bench(count=10):
    if is_recursive_context():
        print(f"[!] Aborting: Benchmark execution detected inside recursive context: {os.getcwd()}")
        sys.exit(1)

    if not os.path.exists(TASK_DIR):
        os.makedirs(TASK_DIR)
    
    print(f"[*] Starting benchmark with {count} concurrent tasks...")
    start_time = int(time.time())
    
    for i in range(count):
        task_id = f"bench-{start_time}-{i}"
        create_task(task_id)
        print(f"  [+] Created task {task_id}")
    
    print(f"[*] All tasks injected. Monitor supervisor for execution.")

if __name__ == "__main__":
    count = 10
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            pass
    run_bench(count)