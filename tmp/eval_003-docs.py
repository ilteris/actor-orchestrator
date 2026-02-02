import os
import json
from datetime import datetime

task_id = "003-docs"
target_report = "logs/evaluations/evaluation_report_003-docs.md"

def evaluate():
    checks = []
    
    # Check 1: Files exist
    if os.path.exists("feature.py") and os.path.exists("README.md"):
        checks.append("Artifact check: PASS")
    else:
        return "FAIL: Missing artifacts."

    # Check 2: Content alignment
    with open("README.md", "r") as f:
        content = f.read()
        if "feature.py" in content or "hello_world()" in content:
            checks.append("Technical alignment: PASS")
        else:
            return "FAIL: README does not reflect feature implementation."

    return "PASS", checks

verdict, details = evaluate()

with open(target_report, "w") as f:
    f.write(f"# Evaluation Report: {task_id}\n\n")
    f.write(f"Date: {datetime.now().strftime('%a %b %d %H:%M:%S %Y')}\n")
    f.write(f"Verdict: {verdict}\n\n")
    f.write("## Notes\n")
    for detail in details:
        f.write(f"- {detail}\n")
    f.write("\nEvaluation performed via Agentic Evaluator command.")

print(f"Evaluation completed for {task_id}: {verdict}")

