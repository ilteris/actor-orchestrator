
import os
import json
import glob

TASKS = [
    "remediate-bench-1769954124-5",
    "remediate-bench-1769954124-6",
    "remediate-bench-1769956087-1"
]

LOG_SEARCH_DIRS = [
    "logs/",
    "logs/archive/benchmark-sessions/"
]

def check_artifacts(bench_id):
    for base_dir in LOG_SEARCH_DIRS:
        bench_dir = os.path.join(base_dir, bench_id)
        if os.path.exists(bench_dir):
            # Check for standard or alternative names
            ls_files = glob.glob(os.path.join(bench_dir, "*ls*"))
            report_files = glob.glob(os.path.join(bench_dir, "*report*"))
            
            if ls_files and report_files:
                return True, bench_dir, ls_files, report_files
    return False, None, None, None

results = {}

for task_id in TASKS:
    # Extract bench_id from task_id (everything after 'remediate-')
    bench_id = task_id.replace("remediate-", "")
    success, path, ls, report = check_artifacts(bench_id)
    
    results[task_id] = {
        "success": success,
        "path": path,
        "artifacts": {
            "ls": ls,
            "report": report
        }
    }

print(json.dumps(results, indent=2))
