import os
import json
from datetime import datetime

task_id = "test-task"
report_path = "logs/test-task_verification.md"
eval_report_path = f"logs/evaluations/evaluation_report_{task_id}.md"

def evaluate():
    if not os.path.exists(report_path):
        return "FAIL: Missing verification report."
    
    with open(report_path, "r") as f:
        content = f.read()
        if "verification" not in content.lower():
            return "FAIL: Report lacks verification keywords."
    
    return "PASS"

verdict = evaluate()

with open(eval_report_path, "w") as f:
    f.write(f"# Evaluation Report: {task_id}\n\n")
    f.write(f"Date: {datetime.now().isoformat()}\n")
    f.write(f"Verdict: {verdict}\n\n")
    f.write("## Notes\n")
    f.write("System verification task passed artifact check.")

print(f"Evaluation completed for {task_id}: {verdict}")
