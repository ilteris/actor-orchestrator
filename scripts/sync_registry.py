import json
import os

def sync():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(script_dir)
    manifest_path = os.path.join(root, 'gemini-extension.json')
    skills_dir = os.path.join(root, 'skills')
    
    if not os.path.exists(manifest_path):
        print(f'Error: {manifest_path} not found')
        return

    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    if os.path.exists(skills_dir):
        current_skills = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
        current_skills.sort()
    else:
        current_skills = []

    manifest['skills'] = current_skills

    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f'Successfully synced {len(current_skills)} skills to {manifest_path}')

if __name__ == '__main__':
    sync()
