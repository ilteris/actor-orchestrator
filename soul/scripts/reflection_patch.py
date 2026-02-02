#!/Users/ilteris/soul_venv/bin/python3
import sys
import os

def reflect(thought_block):
    """
    Simulates a reflection block to increase reflection density.
    In a real agent, this would be an interleaved reasoning turn.
    """
    print("### [ INTERLEAVED REFLECTION ]")
    print(thought_block)
    print("---")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        reflect(sys.argv[1])
    else:
        print("Usage: reflection_patch.py <thought_block>")
