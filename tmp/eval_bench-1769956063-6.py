import json
import os

def evaluate():
    task_id = "bench-1769956063-6"
    report_path = "logs/archive/benchmark-sessions/bench-1769956063-6_report.md"
    ls_path = "logs/archive/benchmark-sessions/bench-1769956063-6_ls.txt"
    eval_report_path = f"logs/evaluations/evaluation_report_{task_id}.md"

    print(f"--- Evaluating {task_id} ---")
    
    # 1. Verify existence of artifacts
    if not os.path.exists(report_path):
        print(f"FAIL: Report not found at {report_path}")
        return False
    if not os.path.exists(ls_path):
        print(f"FAIL: LS output not found at {ls_path}")
        return False
    
    # 2. Basic content validation
    with open(report_path, 'r') as f:
        content = f.read()
        if "Execution Summary" not in content or "Observations" not in content:
            print("FAIL: Report content is incomplete.")
            return False
            
    print("PASS: Artifacts verified.")
    
    # 3. Write final evaluation report
    with open(eval_report_path, 'w') as f:
        f.write(f"# Evaluation Report: {task_id}\n\n")
        f.write("## Status: PASS\n")
        f.write("The benchmark task successfully captured the environment state and generated the required reports.\n")
        f.write(f"- Report verified: {report_path}\n")
        f.write(f"- LS verified: {ls_path}\n")
        
    return True

if __name__ == "__main__":
    if evaluate():
        print("Evaluation Successful")
    else:
        print("Evaluation Failed")
