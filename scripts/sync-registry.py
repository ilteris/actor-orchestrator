#!/usr/bin/env python3
import json
import os
import sys

def sync_registry(project_root):
    skills_dir = os.path.join(project_root, "skills")
    manifest_path = os.path.join(project_root, "gemini-extension.json")
    
    if not os.path.exists(skills_dir):
        print(f"Error: {skills_dir} not found.")
        return
    
    if not os.path.exists(manifest_path):
        print(f"Error: {manifest_path} not found.")
        return

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    # 1. Sync Skills
    skills = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
    skills.sort()
    
    old_skills = manifest.get("skills", [])
    manifest["skills"] = skills
    
    if set(old_skills) != set(skills):
        print(f"Updated skills: {old_skills} -> {skills}")
    else:
        print("Skills are already in sync.")

    # 2. Save manifest
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    
    print(f"Manifest {manifest_path} updated successfully.")

if __name__ == "__main__":
    # Default to the parent directory of this script
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sync_registry(root)
