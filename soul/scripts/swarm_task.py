#!/Users/ilteris/soul_venv/bin/python3
import os
import json
import sys
import shutil
import time

TASK_DIR = "tasks"
TMP_DIR = "tmp"

def claim_task(task_id):
    """
    Moves a task from the global tasks directory to a local temporary workspace.
    """
    # Find the task file in tasks/ or its subdirectories
    source = None
    for root, dirs, files in os.walk(TASK_DIR):
        if f"{task_id}.json" in files:
            source = os.path.join(root, f"{task_id}.json")
            break

    target_dir = os.path.join(TMP_DIR, task_id)
    target = os.path.join(target_dir, "task.json")

    if not source:
        # Check if already claimed
        if os.path.exists(target):
            print(f"Task {task_id} already claimed.")
            return True
        print(f"Error: Task {task_id} not found in {TASK_DIR}.")
        return False

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    try:
        shutil.move(source, target)
        print(f"Task {task_id} claimed successfully at {target}.")
        return True
    except Exception as e:
        print(f"Error claiming task: {e}")
        return False

def update_task(task_file, status, artifacts=None):
    """
    Updates the status and artifacts of a task file.
    """
    if not os.path.exists(task_file):
        print(f"Error: Task file {task_file} not found.")
        return False

    # 1. Verification Logic for 'completed' status
    if status == "completed" and artifacts:
        missing = []
        for art in artifacts:
            if not os.path.exists(art):
                missing.append(art)
        
        if missing:
            print(f"Error: Mandatory artifacts missing: {', '.join(missing)}")
            return False

    # 2. State Transition (Atomic Read-Modify-Write)
    try:
        with open(task_file, 'r+') as f:
            data = json.load(f)
            
            # Check if redundant
            if data.get('status') == 'completed' and status == 'completed':
                print(f"Task {os.path.basename(task_file)} is already completed.")
                return True

            data['status'] = status
            
            if 'metadata' not in data:
                data['metadata'] = {}
            
            data['metadata']['updated_at'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            
            if artifacts:
                if 'artifacts' not in data['metadata']:
                    data['metadata']['artifacts'] = []
                data['metadata']['artifacts'].extend(artifacts)
                # Deduplicate
                data['metadata']['artifacts'] = list(set(data['metadata']['artifacts']))

            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
            f.flush()
            os.fsync(f.fileno())
            print(f"Task {os.path.basename(task_file)} updated to {status}.")
            return True
    except Exception as e:
        print(f"Error updating task: {e}")
        return False

def finish_task(task_id):
    """
    Moves a completed task from the temporary workspace back to the tasks directory.
    """
    target_dir = os.path.join(TMP_DIR, task_id)
    source = os.path.join(target_dir, "task.json")
    
    # Default to tasks/ if we can't find original path (though usually we'd want to preserve structure)
    # For now, let's just put it in tasks/ (or we could store original path in metadata)
    target = os.path.join(TASK_DIR, f"{task_id}.json")

    if not os.path.exists(source):
        print(f"Error: Task file {source} not found.")
        return False

    with open(source, 'r') as f:
        data = json.load(f)
        if data.get('status') != 'completed':
            print(f"Error: Task {task_id} is not marked as 'completed'.")
            return False

    try:
        shutil.move(source, target)
        shutil.rmtree(target_dir)
        print(f"Task {task_id} finished. Task file moved back to {TASK_DIR}.")
        return True
    except Exception as e:
        print(f"Error finishing task: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  swarm_task.py claim <task_id>")
        print("  swarm_task.py update <task_file> <status> [artifact1,artifact2,...]")
        print("  swarm_task.py finish <task_id>")
        sys.exit(1)

    cmd = sys.argv[1]
    
    if cmd == "claim":
        if claim_task(sys.argv[2]):
            sys.exit(0)
    elif cmd == "update":
        t_file = sys.argv[2]
        t_status = sys.argv[3]
        t_artifacts = sys.argv[4].split(',') if len(sys.argv) > 4 and sys.argv[4] else None
        if update_task(t_file, t_status, t_artifacts):
            sys.exit(0)
    elif cmd == "finish":
        if finish_task(sys.argv[2]):
            sys.exit(0)
    else:
        print(f"Unknown command: {cmd}")
    
    sys.exit(1)
