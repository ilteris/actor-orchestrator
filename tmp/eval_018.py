import os
import sys

def evaluate():
    print("Starting evaluation for task: 018-telemetry-optimization")
    artifacts = ["soul/scripts/soul_remediate.py", "soul/scripts/telemetry_sync.py"]
    all_present = True
    for artifact in artifacts:
        if os.path.exists(artifact):
            print(f"[OK] Artifact found: {artifact}")
        else:
            print(f"[ERROR] Artifact missing: {artifact}")
            all_present = False
    if all_present:
        print("PASS: All artifacts present.")
        return True
    else:
        print("FAIL: Missing artifacts.")
        return False

if __name__ == "__main__":
    if evaluate():
        sys.exit(0)
    else:
        sys.exit(1)
