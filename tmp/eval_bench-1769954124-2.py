import os
import json

task_id = "bench-1769954124-2"
task_path = f"tasks/archive/2026-02/bench/{task_id}.json"
report_path = f"logs/archive/benchmark-sessions/{task_id}_report.md"
eval_report_path = f"logs/evaluations/evaluation_report_{task_id}.md"

def evaluate():
    results = {
        "task_id": task_id,
        "criteria": {
            "artifact_existence": False,
            "report_content": False,
            "status_completed": False
        },
        "verdict": "FAIL"
    }

    if os.path.exists(task_path):
        with open(task_path, "r") as f:
            task = json.load(f)
            if task.get("status") == "completed":
                results["criteria"]["status_completed"] = True

    if os.path.exists(report_path):
        results["criteria"]["artifact_existence"] = True
        with open(report_path, "r") as f:
            content = f.read().strip()
            if content and "successfully" in content:
                results["criteria"]["report_content"] = True

    if all(results["criteria"].values()):
        results["verdict"] = "PASS"

    os.makedirs(os.path.dirname(eval_report_path), exist_ok=True)
    with open(eval_report_path, "w") as f:
        f.write(f"# Evaluation Report: {task_id}\n\n")
        f.write(f"Verdict: {results['verdict']}\n\n")
        f.write("## Criteria\n")
        for k, v in results["criteria"].items():
            f.write(f"- {k}: {'✅' if v else '❌'}\n")
    
    print(json.dumps(results))

if __name__ == "__main__":
    evaluate()
