import json
import os
import sys

# 1. Get the absolute path to the folder containing THIS script (jsons/)
# This ensures we find the files even if you run main.py from a different drive/folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Construct absolute paths to the resource files
elements_path = os.path.join(BASE_DIR, "elements.json")
options_path = os.path.join(BASE_DIR, "options.json")

def _load_json_safe(filepath):
    """
    Helper to load JSON with error handling so the app doesn't just hard crash
    if a file is missing during import.
    """
    if not os.path.exists(filepath):
        print(f"[ERROR] Configuration file not found: {filepath}")
        return {}
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"[ERROR] Corrupted JSON in: {filepath}")
        return {}
    except Exception as e:
        print(f"[ERROR] Failed to load {filepath}: {e}")
        return {}

# 3. Load the data
# These variables are now safe to import from anywhere
els = _load_json_safe(elements_path)
options = _load_json_safe(options_path)