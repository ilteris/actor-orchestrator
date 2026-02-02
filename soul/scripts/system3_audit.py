#!/Users/ilteris/soul_venv/bin/python3
import os
import re
import glob
from datetime import datetime, timedelta

def get_last_24h_files(directory):
    files = []
    now = datetime.now()
    threshold = now - timedelta(hours=24)
    pattern = os.path.join(directory, "????-??-??.md")
    for f in glob.glob(pattern):
        mtime = datetime.fromtimestamp(os.path.getmtime(f))
        if mtime > threshold:
            files.append(f)
    return sorted(files)

def analyze_traces(files):
    analysis = {
        "verbosity_warnings": [],
        "protocol_drift": [],
        "efficiency_notes": [],
        "proposed_patches": []
    }
    
    for file_path in files:
        with open(file_path, 'r') as f:
            content = f.read()
            
            # Check for Interleaved Reflection
            if "### Interleaved Reflection" not in content and "Interleaved Reflection" not in content:
                analysis["protocol_drift"].append(f"Missing Reflection block in {os.path.basename(file_path)}")
            
            # Check for excessive conversational filler
            fillers = ["I hope this helps", "Let me know if", "I have finished", "I am now"]
            for filler in fillers:
                if filler.lower() in content.lower():
                    analysis["verbosity_warnings"].append(f"Detected filler '{filler}' in {os.path.basename(file_path)}")
            
            # Check for Thinking block vs Content ratio
            thinking_blocks = re.findall(r"### Thinking:(.*?)(?=###|$)", content, re.DOTALL)
            for block in thinking_blocks:
                if len(block) > 1000:
                    analysis["efficiency_notes"].append(f"Oversized Thinking block in {os.path.basename(file_path)} (>1000 chars)")

    # Heuristic Patch Generation (GLOBAL)
    if analysis["protocol_drift"]:
        analysis["proposed_patches"].append("Strengthen Protocol enforcement: Add 'STRICT: Every response MUST contain a reflection block' to SOUL.md.")
    
    if analysis["verbosity_warnings"]:
        analysis["proposed_patches"].append("Refine Persona: Update SYSTEM.md to explicitly ban phrases like 'I hope this helps' or 'I am now'.")
        
    if not analysis["protocol_drift"] and not analysis["verbosity_warnings"]:
        analysis["proposed_patches"].append("System Health Nominal: No immediate patches required.")

    return analysis

def generate_report(analysis):
    date_str = datetime.now().strftime("%Y-%m-%d")
    md = f"# Global System 3 Trace Analysis - {date_str}\n\n"
    md += "> NOTE: This audit analyzes the synthesized memory of all machines.\n\n"
    
    md += "## Protocol Drift\n"
    if not analysis["protocol_drift"]:
        md += "- Protocol adherence is 100%.\n"
    else:
        for p in analysis["protocol_drift"]:
            md += f"- {p}\n"
            
    md += "\n## Verbosity & Tone Audit\n"
    if not analysis["verbosity_warnings"]:
        md += "- Tone is stoic and direct.\n"
    else:
        for v in analysis["verbosity_warnings"]:
            md += f"- {v}\n"
            
    md += "\n## Proposed SYSTEM.md Patches (Fleet-wide)\n"
    for patch in analysis["proposed_patches"]:
        if ':' in patch:
            title, desc = patch.split(':', 1)
            md += f"### Patch candidate: {title.strip()}\n"
            md += f"{desc.strip()}\n\n"
        else:
            md += f"### Patch candidate: {patch}\n"
            md += f"{patch}\n\n"
        
    return md

if __name__ == "__main__":
    memory_dir = "soul/memory"
    files = get_last_24h_files(memory_dir)
    analysis = analyze_traces(files)
    report = generate_report(analysis)
    
    # Global output - overwrite/update the single current intelligence report
    output_path = f"soul/memory/system3_audit.md"
    with open(output_path, 'w') as f:
        f.write(report)
    print(f"Global System 3 Audit complete: {output_path}")