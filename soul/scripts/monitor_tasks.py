#!/Users/ilteris/soul_venv/bin/python3
import os
import json
import time

REGISTRY_PATH = "soul/registry/tasks"

def monitor():
    if not os.path.exists(REGISTRY_PATH):
        os.makedirs(REGISTRY_PATH)
        print(f"Created registry path: {REGISTRY_PATH}")
    
    print(f"Monitoring {REGISTRY_PATH} for new tasks...")
    # This is a stub for the monitoring logic mentioned in Task 14
    # In a real scenario, this would loop or be triggered by fs events.
    files = os.listdir(REGISTRY_PATH)
    if files:
        print(f"Found {len(files)} tasks.")
        for f in files:
            print(f" - {f}")
    else:
        print("No new tasks found.")

if __name__ == "__main__":
    monitor()
