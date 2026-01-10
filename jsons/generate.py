import json
import os
from datetime import datetime
from typing import Any, Optional

# Local imports
from utilities.files import create_folder, createIndexLists

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def get_variable_name(file_path: str) -> str:
    """
    Returns the JS variable name based on the file content/type.
    Prioritizes 'REVIEW_DATA' and 'MAIN_DATA' for frontend compatibility.
    """
    filename = os.path.basename(file_path).lower()
    
    # Check specifically for review files
    if "review" in filename:
        return "REVIEW_DATA"
    
    # Check for main data files (including those in Lists)
    if "main" in filename:
        # You can add specific logic here if LIST_DATA needs to be distinct
        # logic: if "Lists" in file_path: return "LIST_DATA"
        return "MAIN_DATA"

    # Fallback: converts 'cast.js' -> 'CAST_DATA'
    name_no_ext = os.path.splitext(filename)[0]
    return f"{name_no_ext.replace(' ', '_').upper()}_DATA"


# ---------------------------------------------------------
# CORE FUNCTIONS
# ---------------------------------------------------------

def create_js(file_path: str):
    """
    Creates a .js file initialized with an empty object: const NAME_DATA = {}
    Does nothing if the file already exists.
    """
    if os.path.exists(file_path):
        return

    try:
        var_name = get_variable_name(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"const {var_name} = {{}}")
    except Exception as e:
        print(f"Error creating JS file: {e}")


def write_js(file_path: str, header: str, data: Any, main_header: Optional[str] = None):
    """
    Reads a JS file (acting as JSON storage), updates it, and writes it back.
    Format: const VAR_NAME = { ...json... }
    """
    current_data = {}
    var_name = get_variable_name(file_path)

    try:
        # --- 1. READ AND PARSE ---
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Locate the start of the JSON object
                start_index = content.find('{')
                if start_index != -1:
                    json_payload = content[start_index:]
                    try:
                        current_data = json.loads(json_payload)
                    except json.JSONDecodeError:
                        print(f"Warning: JSON structure broken in {file_path}, resetting data.")
                        current_data = {}
        
        # --- 2. UPDATE DATA ---
        if main_header:
            # Ensure the main_header key exists and is a dictionary
            if main_header not in current_data or not isinstance(current_data[main_header], dict):
                current_data[main_header] = {}
            
            current_data[main_header][header] = data
        else:
            current_data[header] = data

        # --- 3. WRITE BACK ---
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"const {var_name} = ")
            json.dump(current_data, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Error writing to JS file {file_path}: {e}")


def createList(list_name: str) -> str:
    """
    Sets up the directory structure and initial files for a curated List.
    """
    folder_path = f"Scraped/Lists/{list_name}"
    json_path = f"{folder_path}/data/"
    js_file = f"{json_path}main.js"

    print(f"Creating list: {list_name}...")

    # Create directories
    create_folder(json_path)
    
    # Create HTML index if utility is available
    createIndexLists(folder_path)
    
    # Initialize the data file
    create_js(js_file)

    # Add metadata
    creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_js(js_file, "ListName", list_name, main_header="list_info")
    write_js(js_file, "DateCreated", creation_date, main_header="list_info")

    return folder_path