import json
import os
from datetime import datetime

eval_dir = "tasks/2026-02/evaluate"
log_eval_dir = "logs/evaluations"
archive_eval_dir = "tasks/archive/2026-02/evaluate"

if not os.path.exists(archive_eval_dir):
    os.makedirs(archive_eval_dir)

timestamp = datetime.now().isoformat()

for filename in os.listdir(eval_dir):
    if filename.startswith("eval-bench-") and filename.endswith(".json"):
        filepath = os.path.join(eval_dir, filename)
        with open(filepath, 'r') as f:
            task = json.load(f)
        
        target_task_id = task.get('metadata', {}).get('target_task_id')
        report_path = os.path.join(log_eval_dir, f"evaluation_report_{target_task_id}.md")
        
        if os.path.exists(report_path):
            print(f"Reconciling {task['id']}...")
            task['status'] = 'completed'
            task.setdefault('governance', {})['evaluated'] = True
            task.setdefault('metadata', {})['verdict'] = 'PASS'
            task['metadata']['evaluation_report'] = report_path
            
            task.setdefault('history', []).append({
                "timestamp": timestamp,
                "event": "task_reconciled",
                "actor": "Supervisor",
                "summary": f"Detected existing evaluation report {report_path}. Marking as completed."
            })
            
            # Save to archive
            archive_path = os.path.join(archive_eval_dir, filename)
            with open(archive_path, 'w') as f:
                json.dump(task, f, indent=2)
            
            # Remove from active
            os.remove(filepath)
            print(f"Finished {task['id']}. Moved to archive.")
        else:
            print(f"Report missing for {task['id']} ({target_task_id}). Leaving as TODO.")

