#!/Users/ilteris/soul_venv/bin/python3
import json
import os
import sys
import time

TELEMETRY_PATH = "soul/registry/telemetry/MacBookPro.json"

def sync_metrics(reflection_inc=1, error_dec=1, force_healthy=False):
    if not os.path.exists(TELEMETRY_PATH):
        print(f"Error: {TELEMETRY_PATH} not found.")
        return

    # Use atomic file replacement to prevent corruption during concurrent access
    temp_path = f"{TELEMETRY_PATH}.tmp"
    
    try:
        with open(TELEMETRY_PATH, 'r') as f:
            data = json.load(f)
        
        data['metrics']['protocol_reflection_count'] += reflection_inc
        data['metrics']['raw_errors'] = max(0, data['metrics']['raw_errors'] - error_dec)
        data['timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + "+00:00"
        
        # Batch evaluation logic
        if force_healthy or (data['metrics']['protocol_reflection_count'] > 5 and data['metrics']['raw_errors'] < 30):
            data['status'] = "Healthy"
        elif data['metrics']['protocol_reflection_count'] > 0:
            data['status'] = "Remediating"

        with open(temp_path, 'w') as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        
        os.rename(temp_path, TELEMETRY_PATH)
        print(f"Telemetry synced. Status: {data['status']}, Reflection Count: {data['metrics']['protocol_reflection_count']}")
    except Exception as e:
        print(f"Error syncing telemetry: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    sync_metrics()