import asyncio
import websockets
import json
import os
import glob
from datetime import datetime

# Path Configuration
TASKS_DIR = ".tasks"
INBOX_DIR = "inboxes"
LOGS_DIR = "logs"

async def get_swarm_state():
    """Aggregates the current state of the swarm from the filesystem."""
    state = {
        "timestamp": datetime.now().isoformat(),
        "tasks": [],
        "workers": [],
        "events": []
    }
    
    # Load Tasks
    task_files = glob.glob(f"{TASKS_DIR}/*.json")
    for f in task_files:
        try:
            with open(f, 'r') as tf:
                state["tasks"].append(json.load(tf))
        except Exception as e:
            print(f"Error reading task {f}: {e}")

    # Load Inbox (Supervisor signaling)
    inbox_file = f"{INBOX_DIR}/supervisor.jsonl"
    if os.path.exists(inbox_file):
        try:
            with open(inbox_file, 'r') as f:
                lines = f.readlines()[-10:] # Last 10 events
                state["events"] = [json.loads(l) for l in lines]
        except Exception as e:
            print(f"Error reading inbox: {e}")

    return state

async def handler(websocket, path):
    """Handles WebSocket connections."""
    print(f"Client connected: {websocket.remote_address}")
    try:
        while True:
            state = await get_swarm_state()
            await websocket.send(json.dumps(state))
            await asyncio.sleep(2) # 2-second heartbeat
    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")

async def main():
    print("Starting Swarm Telemetry WebSocket Bridge on ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
