import json
import os

tasks_to_eval = [
    "bench-1769956063-3", "bench-1769956063-8", "bench-1769956087-3",
    "bench-1769956058-5", "bench-1769956063-5", "bench-1769956087-9",
    "bench-1769956063-9", "bench-1769956087-2", "bench-1769954124-0",
    "bench-1769956063-4", "bench-1769956058-6", "bench-1769956087-0",
    "bench-1769956063-6", "bench-1769956063-0", "bench-1769963702-0",
    "bench-1769963707-0", "bench-1769963707-1", "bench-1769963707-2",
    "bench-1769963707-3", "bench-1769963707-4", "bench-1769963707-5",
    "bench-1769963707-9"
]

output_dir = "tasks/2026-02/evaluate"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for task_id in tasks_to_eval:
    eval_id = f"eval-{task_id}"
    report_path = f"logs/archive/benchmark-sessions/{task_id}_report.md"
    
    # Special case for bench-1769963702-0 retry
    if task_id == "bench-1769963702-0":
        report_path = f"logs/{task_id}_report.md"
        if not os.path.exists(report_path):
             report_path = f"logs/archive/benchmark-sessions/{task_id}_report.md"

    task_data = {
        "id": eval_id,
        "subject": f"Evaluate {task_id}",
        "description": f"Evaluate the completion and quality of {task_id} based on {report_path}",
        "pillar": "ML Infrastructure",
        "status": "todo",
        "priority": "medium",
        "orchestration": {
            "team": "dotfiles",
            "role_contract": "evaluator"
        },
        "metadata": {
            "target_task_id": task_id,
            "target_artifact": report_path
        }
    }
    
    file_path = os.path.join(output_dir, f"{eval_id}.json")
    with open(file_path, 'w') as f:
        json.dump(task_data, f, indent=2)
    print(f"Created evaluation task: {file_path}")
