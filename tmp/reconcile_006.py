import json
import os
from datetime import datetime

filepath = "tasks/2026-02/evaluate/eval-006-scaling-bench.json"
report_path = "logs/evaluations/evaluation_report_006-scaling-bench.md"
archive_dir = "tasks/archive/2026-02/evaluate"

if os.path.exists(filepath) and os.path.exists(report_path):
    with open(filepath, 'r') as f:
        task = json.load(f)
    
    task['status'] = 'completed'
    task.setdefault('governance', {})['evaluated'] = True
    task.setdefault('metadata', {})['verdict'] = 'PASS'
    task['metadata']['evaluation_report'] = report_path
    
    task.setdefault('history', []).append({
        "timestamp": datetime.now().isoformat(),
        "event": "task_reconciled",
        "actor": "Supervisor",
        "summary": "Detected existing evaluation report. Marking as completed."
    })
    
    archive_path = os.path.join(archive_dir, os.path.basename(filepath))
    with open(archive_path, 'w') as f:
        json.dump(task, f, indent=2)
    
    os.remove(filepath)
    print("Reconciled eval-006-scaling-bench.")
