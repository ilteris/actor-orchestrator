import os
import json
import time
from datetime import datetime
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, Static, DataTable, Label, Log
from textual.reactive import reactive

class TaskRegistry:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.tasks_dir = project_dir / "tasks"

    def get_tasks(self):
        if not self.tasks_dir.exists():
            return []
        tasks = []
        for p in self.tasks_dir.glob("*.json"):
            try:
                with open(p, "r") as f:
                    data = json.load(f)
                    tasks.append({
                        "id": p.stem,
                        "title": data.get("title", p.stem),
                        "status": data.get("status", "pending"),
                        "updated": p.stat().st_mtime
                    })
            except:
                pass
        return sorted(tasks, key=lambda x: x["updated"], reverse=True)

class SwarmMonitor(App):
    TITLE = "🤖 SWARM MISSION CONTROL"
    CSS = """
    Screen {
        background: #1a1b26;
    }
    #main-container {
        layout: horizontal;
    }
    #left-pane {
        width: 40%;
        border-right: tall #414868;
        padding: 1;
    }
    #right-pane {
        width: 60%;
        padding: 1;
    }
    .status-completed { color: #9ece6a; }
    .status-in_progress { color: #e0af68; }
    .status-pending { color: #565f89; }
    
    #header-info {
        height: 3;
        background: #24283b;
        content-align: center middle;
        color: #7aa2f7;
        border-bottom: solid #414868;
    }
    """

    tasks = reactive([])
    current_focus = reactive(None)

    def __init__(self, project_dir: str):
        super().__init__()
        self.registry = TaskRegistry(Path(project_dir))
        self.log_dir = Path("/tmp/actor-orchestrator")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Supervisor: Monitoring Registry and Coordinating Swarm", id="header-info")
        with Container(id="main-container"):
            with Vertical(id="left-pane"):
                yield Label("📋 PROJECT BLACKBOARD")
                yield DataTable(id="task-table")
            with Vertical(id="right-pane"):
                yield Label("🐦 WORKER TELEMETRY")
                yield Log(id="worker-log")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#task-table", DataTable)
        table.add_columns("ID", "Status", "Task")
        table.cursor_type = "row"
        self.set_interval(1.0, self.refresh_data)

    def refresh_data(self) -> None:
        new_tasks = self.registry.get_tasks()
        table = self.query_one("#task-table", DataTable)
        
        # Simple reconciliation
        table.clear()
        for t in new_tasks:
            status_icon = "✓" if t["status"] == "completed" else "⠋" if t["status"] == "in_progress" else " "
            table.add_row(t["id"], status_icon, t["title"])
        
        if table.coordinate_to_cell_key:
             # Logic to update log if row is selected
             pass

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        row_data = event.data_table.get_row(event.row_key)
        self.current_focus = row_data[0]
        self.update_log_view()

    def update_log_view(self) -> None:
        log_widget = self.query_one("#worker-log", Log)
        log_widget.clear()
        log_file = self.log_dir / f"worker-{self.current_focus}.log"
        if log_file.exists():
            with open(log_file, "r") as f:
                content = f.readlines()[-20:]
                for line in content:
                    log_widget.write_line(line.strip())
        else:
            log_widget.write_line(f"(No log found for {self.current_focus})")

if __name__ == "__main__":
    import sys
    project_path = sys.argv[1] if len(sys.argv) > 1 else "."
    app = SwarmMonitor(project_path)
    app.run()
