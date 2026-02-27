#!/usr/bin/env python3
import sys
import os
import yaml

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backends import BACKENDS

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_backend(config: dict):
    backend_name = config.get("model", {}).get("backend", "local")
    backend_class = BACKENDS.get(backend_name)
    
    if not backend_class:
        raise ValueError(f"Unknown backend: {backend_name}")
    
    # Get backend-specific config
    backend_config = config.get("model", {}).get(backend_name, {})
    return backend_class(backend_config)

def main():
    if len(sys.argv) < 2:
        print("Error: no input", file=sys.stderr)
        sys.exit(1)
    
    query = sys.argv[1]
    
    try:
        config = load_config()
        backend = get_backend(config)
        response = backend.generate(query, max_tokens=256)
        print(response)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()