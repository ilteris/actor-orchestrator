import os

def evaluate():
    report_path = "logs/archive/benchmark-sessions/bench-1769965536-0_report.md"
    ls_path = "logs/archive/benchmark-sessions/bench-1769965536-0_ls.txt"
    
    if not os.path.exists(report_path):
        return False, f"Missing report: {report_path}"
    
    if not os.path.exists(ls_path):
        return False, f"Missing ls log: {ls_path}"
    
    with open(report_path, 'r') as f:
        content = f.read()
        if "successfully" in content.lower() or "report" in content.lower():
            return True, "Task passed evaluation"
            
    return False, "Report content check failed"

if __name__ == "__main__":
    success, message = evaluate()
    print(message)
    exit(0 if success else 1)