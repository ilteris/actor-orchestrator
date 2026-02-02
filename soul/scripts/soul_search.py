#!/Users/ilteris/soul_venv/bin/python3
import os
import sys
import json
import subprocess
import argparse
from datetime import datetime

# Path Configuration
SOUL_MEMORY = "soul/memory"
SOUL_REGISTRY = "soul/registry"
SOUL_VENV_PYTHON = "/Users/ilteris/soul_venv/bin/python3"

# System Prompt for Semantic Search
SYSTEM_PROMPT = """
You are Teddy's Semantic Search Engine.
Your goal is to analyze the provided search results (from ripgrep) and identify the most relevant technical traces, architectural decisions, or status updates.

Rules:
1. Be extremely concise.
2. Group results by machine or date if possible.
3. If no direct match is found semantically, explain why.
4. Highlight 'Technical Traces' and 'Architectural Narratives'.
"""

def search_local(query, target_dir):
    """
    Uses ripgrep to find raw text matches in the specified directory.
    """
    print(f"### [ ripgrep: searching '{query}' in {target_dir} ]")
    try:
        # ripgrep command: search for query, return filename and matching line
        result = subprocess.run(
            ["rg", "-i", "--heading", "--line-number", query, target_dir],
            capture_output=True,
            text=True
        )
        return result.stdout
    except FileNotFoundError:
        print("Error: ripgrep (rg) not found. Please install it.")
        return ""

def semantic_reasoning(query, raw_results):
    """
    Uses Gemini to perform semantic reasoning over the raw ripgrep results.
    """
    if not raw_results.strip():
        return "No local matches found to reason about."

    print("### [ Gemini: Semantic Analysis ]")
    
    # Construct the prompt for Gemini
    prompt = f"{SYSTEM_PROMPT}\n\nUser Query: {query}\n\nRaw Search Results:\n{raw_results}"
    
    try:
        # Use gemini CLI for one-shot reasoning
        result = subprocess.run(
            ["gemini", prompt],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"Error during semantic reasoning: {e}"

def main():
    parser = argparse.ArgumentParser(description="Agentic Soul Search: ripgrep + Gemini")
    parser.add_argument("query", help="The search query")
    parser.add_argument("--dir", default=SOUL_MEMORY, help=f"Directory to search (default: {SOUL_MEMORY})")
    parser.add_argument("--raw", action="store_true", help="Return raw ripgrep results only")
    
    args = parser.parse_args()

    # Step 1: High-speed local search
    raw_results = search_local(args.query, args.dir)
    
    if args.raw:
        print(raw_results)
        return

    # Step 2: Semantic enrichment
    enriched_results = semantic_reasoning(args.query, raw_results)
    
    # Output the final intelligence
    print("\n--- [ Agentic Search Results ] ---\n")
    print(enriched_results)

if __name__ == "__main__":
    main()
