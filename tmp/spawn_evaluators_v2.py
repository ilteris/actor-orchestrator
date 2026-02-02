import json
import os

tasks_to_eval = [
    {
        "id": "15",
        "subject": "Evaluate Soul Audit (Task 15)",
        "artifact": "soul/memory/audits/MacBookPro/2026-02-01.md"
    },
    {
        "id": "16",
        "subject": "Evaluate System 3 Audit (Task 16)",
        "artifact": "soul/memory/2026-02-01.md"
    },
    {
        "id": "21",
        "subject": "Evaluate Atomic Memory Correction (Task 21)",
        "artifact": "README.md"
    }
]

output_dir = "tasks/2026-02/evaluate"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for task in tasks_to_eval:
    eval_id = f"eval-{task['id']}"
    task_data = {
        "id": eval_id,
        "subject": task['subject'],
        "description": f"Evaluate the completion and quality of task {task['id']} based on {task['artifact']}",
        "pillar": "Systems Engineering",
        "status": "todo",
        "priority": "high",
        "orchestration": {
            "team": "dotfiles",
            "role_contract": "evaluator"
        },
        "metadata": {
            "target_task_id": task['id'],
            "target_artifact": task['artifact']
        }
    }
    
    file_path = os.path.join(output_dir, f"{eval_id}.json")
    with open(file_path, 'w') as f:
        json.dump(task_data, f, indent=2)
    print(f"Created evaluation task: {file_path}")
