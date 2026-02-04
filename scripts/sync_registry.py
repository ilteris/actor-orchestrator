import json
import os
from pathlib import Path

def sync_registry():
    # Identify the project root
    target_root = Path(__file__).parent.parent
    
    skills_dir = target_root / "skills"
    manifest_path = target_root / "gemini-extension.json"
    
    if not manifest_path.exists():
        print(f"Error: {manifest_path} not found.")
        return

    # 1. Load existing manifest
    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    # 2. Discover Skills
    skills = []
    if skills_dir.exists():
        skills = [d.name for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
    skills.sort()
    
    # 3. Discover Tools
    # We maintain a set of "core" tools that should always be there
    core_tools = {
        "run_shell_command",
        "write_todos",
        "read_file",
        "list_files",
        "delegate_to_agent",
        "web_fetch",
        "google_search",
        "activate_skill"
    }
    
    discovered_tools = set()
    if skills_dir.exists():
        for skill_path in skills_dir.iterdir():
            if not skill_path.is_dir():
                continue
                
            # Check for tools.json
            tools_json_path = skill_path / "tools.json"
            if tools_json_path.exists():
                try:
                    with open(tools_json_path, "r") as f:
                        skill_tools = json.load(f)
                        if isinstance(skill_tools, list):
                            discovered_tools.update(skill_tools)
                except Exception as e:
                    print(f"Error reading {tools_json_path}: {e}")

            # Check for tools/ directory
            tools_dir = skill_path / "tools"
            if tools_dir.exists() and tools_dir.is_dir():
                for tool_file in tools_dir.iterdir():
                    if tool_file.is_file() and tool_file.suffix in [".py", ".sh"]:
                        discovered_tools.add(tool_file.stem.replace("-", "_"))

    # Combine and sort
    all_tools = sorted(list(core_tools.union(discovered_tools)))

    # 4. Update Manifest
    manifest["skills"] = skills
    manifest["allowedTools"] = all_tools

    # 5. Atomic Write
    temp_manifest = manifest_path.with_suffix(".json.tmp")
    with open(temp_manifest, "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    
    os.replace(str(temp_manifest), str(manifest_path))
    print(f"Successfully synced {len(skills)} skills and {len(all_tools)} tools to {manifest_path}")

if __name__ == "__main__":
    sync_registry()
