import json
import os

def evaluate():
    report_path = "logs/bench-1769963707-3_report.md"
    ls_path = "logs/bench-1769963707-3_ls.txt"
    task_path = "tasks/2026-02/eval-bench-1769963707-3.json"
    
    if not os.path.exists(report_path):
        return False, "Report missing"
    if not os.path.exists(ls_path):
        return False, "LS artifact missing"
    
    with open(report_path, 'r') as f:
        content = f.read()
        if "bench-1769963707-3" not in content:
            return False, "Incorrect Task ID in report"
        if "Explorer" not in content:
            return False, "Missing Contract info"
            
    return True, "Evaluation passed"

passed, reason = evaluate()
print(json.dumps({"passed": passed, "reason": reason}))
