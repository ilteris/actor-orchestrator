import subprocess
import os
import json

def test_robustness():
    # 1. Test update_task with fsync and artifact verification
    # Create a dummy task
    task_id = "test_eval_robustness"
    task_file = f"tasks/{task_id}.json"
    with open(task_file, "w") as f:
        json.dump({"id": task_id, "status": "todo"}, f)
    
    print("--- Test: Claim Task ---")
    res = subprocess.run(["python3", "soul/scripts/swarm_task.py", "claim", task_id], capture_output=True, text=True)
    print(res.stdout)
    assert res.returncode == 0
    assert os.path.exists(f"tmp/{task_id}/task.json")
    
    print("--- Test: Update Task (Missing Artifact) ---")
    res = subprocess.run(["python3", "soul/scripts/swarm_task.py", "update", f"tmp/{task_id}/task.json", "completed", "missing_file.txt"], capture_output=True, text=True)
    print(res.stdout)
    assert res.returncode != 0 # Should fail
    
    print("--- Test: Update Task (Success) ---")
    # Create the artifact
    with open("eval_artifact.txt", "w") as f: f.write("test")
    res = subprocess.run(["python3", "soul/scripts/swarm_task.py", "update", f"tmp/{task_id}/task.json", "completed", "eval_artifact.txt"], capture_output=True, text=True)
    print(res.stdout)
    assert res.returncode == 0
    
    print("--- Test: Finish Task ---")
    res = subprocess.run(["python3", "soul/scripts/swarm_task.py", "finish", task_id], capture_output=True, text=True)
    print(res.stdout)
    assert res.returncode == 0
    assert os.path.exists(f"tasks/{task_id}.json")
    assert not os.path.exists(f"tmp/{task_id}")
    
    # Cleanup
    os.remove(f"tasks/{task_id}.json")
    os.remove("eval_artifact.txt")
    print("All tests passed.")

if __name__ == "__main__":
    test_robustness()
