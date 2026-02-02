import json

with open('tasks/bench-1769956058-9.json', 'r') as f:
    task = json.load(f)

if 'governance' not in task:
    task['governance'] = {}

task['governance']['evaluated'] = True

with open('tasks/bench-1769956058-9.json', 'w') as f:
    json.dump(task, f, indent=2)
