import json
import os

def evaluate_016():
    task_id = "016"
    task_file = f"tasks/2026-02/system/{task_id}.json"
    report_file = "logs/016-e2e-ingestion-audit.md"
    
    evaluation = {
        "task_id": task_id,
        "status": "FAILED",
        "observations": [],
        "verdict": ""
    }
    
    if not os.path.exists(task_file):
        evaluation["observations"].append(f"Task file {task_file} missing.")
        return evaluation

    with open(task_file, 'r') as f:
        task_data = json.load(f)
        
    if task_data.get("status") != "completed":
        evaluation["observations"].append("Task status is not 'completed'.")
    
    # Check artifacts
    artifacts = task_data.get("metadata", {}).get("artifacts", [])
    for artifact in artifacts:
        if not os.path.exists(artifact):
            evaluation["observations"].append(f"Artifact missing: {artifact}")
    
    if not evaluation["observations"]:
        evaluation["status"] = "PASSED"
        evaluation["verdict"] = "E2E Ingestion Audit verified. All artifacts present and task metadata updated."
    else:
        evaluation["verdict"] = "; ".join(evaluation["observations"])
        
    return evaluation

if __name__ == "__main__":
    result = evaluate_016()
    print(json.dumps(result, indent=2))
    
    # Write report
    with open(f"logs/evaluations/evaluation_report_{result['task_id']}.md", "w") as f:
        f.write(f"# Evaluation Report for Task {result['task_id']}\n\n")
        f.write(f"**Status**: {result['status']}\n\n")
        f.write(f"## Observations\n")
        if result['status'] == "PASSED":
            f.write("- All artifacts verified successfully.\n")
            f.write("- Task completion status confirmed.\n")
        else:
            for obs in result['observations']:
                f.write(f"- {obs}\n")
        f.write(f"\n## Verdict\n{result['verdict']}\n")
