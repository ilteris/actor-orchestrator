import os

def evaluate():
    report_path = "logs/bench-1769965536-1/report.md"
    ls_path = "logs/bench-1769965536-1/ls_recursive.txt"
    
    if not os.path.exists(report_path):
        return False, f"Missing report: {report_path}"
    
    if not os.path.exists(ls_path):
        return False, f"Missing ls log: {ls_path}"
    
    with open(report_path, 'r') as f:
        content = f.read()
        if "successfully" not in content.lower():
            return False, "Report does not indicate success"
            
    return True, "Task passed evaluation"

if __name__ == "__main__":
    success, message = evaluate()
    print(message)
    exit(0 if success else 1)
