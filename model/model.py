#!/usr/bin/env python3
import sys
import os

# Path to your existing tier1.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from model.tier1 import Tier1Engine

_model = None

def get_model():
    global _model
    if _model is None:
        _model = Tier1Engine(
            model_path="models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
            n_threads=4
        )
    return _model

def main():
    if len(sys.argv) < 2:
        print("Error: no input", file=sys.stderr)
        sys.exit(1)
    
    query = sys.argv[1]
    
    try:
        model = get_model()
        response = model.generate(query, max_tokens=256)
        print(response)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()