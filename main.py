import argparse
import sys
import os
import signal
import time
import threading
import itertools
from datetime import datetime
from utilities.cmd_colors import red, green, yellow, cyan, blue, reset

# --- Imports ---
try:
    from driver.driver import chromeDriver, firefoxDriver
    from driver.search import searchByURL
    from driver.scrape import fullScrape
except ImportError as e:
    print(f"{red}[CRITICAL] Import Error: {e}{reset}")
    sys.exit(1)

# --- UI & Banner ---
BANNER = r"""
       [ IScrapeMDB CLI v1.0.0 ]
       [    Created by MYST    ]
"""

def print_banner():
    # Clear screen for a fresh start (works on Win/Linux/Mac)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\033[96m{BANNER}\033[0m")

def print_status(msg, type="INFO"):
    colors = {
        "INFO": "\033[94m",    # Blue
        "SUCCESS": "\033[92m", # Green
        "WARN": "\033[93m",    # Yellow
        "ERROR": "\033[91m",   # Red
        "INPUT": "\033[95m",   # Magenta
        "SYSTEM": "\033[90m"   # Grey
    }
    col = colors.get(type, "\033[97m")
    # Clean output formatting
    print(f"[{col}{type}{reset}] {msg}")

# --- Loading Animation Class ---
class Spinner:
    """
    A threaded spinner animation to keep things looking alive
    during heavy blocking operations (like driver init).
    """
    def __init__(self, message="Loading..."):
        self.message = message
        self.stop_running = threading.Event()
        self.spin_thread = threading.Thread(target=self._spin)

    def _spin(self):
        # Braille pattern for a smooth spinner
        spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        spinner_cycle = itertools.cycle(spinner_chars)
        
        while not self.stop_running.is_set():
            sys.stdout.write(f"\r{cyan}{next(spinner_cycle)}{reset} {self.message}")
            sys.stdout.flush()
            time.sleep(0.08)
        
        # Clear the line when done
        sys.stdout.write(f"\r{' ' * (len(self.message) + 2)}\r")
        sys.stdout.flush()

    def __enter__(self):
        self.spin_thread.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stop_running.set()
        self.spin_thread.join()

# --- Signal Handling ---
def signal_handler(sig, frame):
    print("\n")
    print_status("Interrupted by user. Exiting...", "WARN")
    # Clean exit
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# --- Helpers ---
def get_targets(args):
    """
    Collects targets from CLI args or File.
    Enforces URL format.
    """
    targets = []
    
    # 1. From Arguments
    if args.targets:
        targets.extend(args.targets)

    # 2. From File
    if args.file:
        if os.path.exists(args.file): 
            print_status(f"Reading targets from: {yellow}{args.file}{reset}", "INFO")
            with open(args.file, 'r') as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
                targets.extend(lines)
        else:
            print_status("Input file not found.", "ERROR")
            sys.exit(1)
            
    # Basic cleanup: Ensure they look like URLs
    cleaned_targets = []
    for t in targets:
        if not t.startswith("http"):
            t = "https://" + t
        cleaned_targets.append(t)
            
    return cleaned_targets

def validate_append_path(path):
    abs_path = os.path.abspath(path)
    
    if "Series" in abs_path or "Movies" in abs_path:
        print_status("Cannot append items to a single Movie/Series folder.", "ERROR")
        print_status("Target must be a List folder (e.g., Scraped/Lists/MyList).", "ERROR")
        sys.exit(1)
    
    data_path = os.path.join(path, "data")
    if not os.path.exists(data_path):
        print_status(f"Invalid List Folder (No 'data' subfolder): {path}", "ERROR")
        sys.exit(1)
        
    return path

def make_portable(target_folder):
    """
    Combines HTML + JS into a single file for offline sharing.
    """
    index_path = os.path.join(target_folder, "index.html")
    data_path = os.path.join(target_folder, "data")
    
    if not os.path.exists(index_path):
        print_status(f"No index.html found in {target_folder}", "ERROR")
        return
   
    print_status(f"converting to portable: {target_folder}", "INFO")

    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Inject Main Data
        main_js_path = os.path.join(data_path, "main.js")
        if os.path.exists(main_js_path):
            with open(main_js_path, 'r', encoding='utf-8') as f:
                main_js = f.read()
            html = html.replace('<script src="data/main.js"></script>', f'<script>\n{main_js}\n</script>')
        
        # Inject Review Data
        review_js = ""
        review_path = os.path.join(data_path, "review.js")
        if os.path.exists(review_path):
            with open(review_path, 'r', encoding='utf-8') as f:
                review_js = f.read()
            html = html.replace('<script src="data/review.js"></script>', f'<script>\n{review_js}\n</script>')

        # Save Output
        output_path = os.path.join(target_folder, "portable.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
            
        print_status(f"Portable file created: {green}{output_path}{reset}", "SUCCESS")

    except Exception as e:
        print_status(f"Error creating portable file: {e}", "ERROR")

# --- Main Logic ---
def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    # Inputs
    parser.add_argument("targets", nargs="*", help="Target IMDb URL(s)")
    parser.add_argument("-f", "--file", metavar="PATH", help="Text file with links (one per line)")
    
    # Utilities
    parser.add_argument("-portable", metavar="PATH", help="Convert an existing scrape folder to a single HTML file")

    # Modes
    parser.add_argument("-l", "--list", metavar="NAME", help="Create a NEW Curated List")
    parser.add_argument("-a", "--append", metavar="PATH", help="Append to an EXISTING List (Folder Path)")
    
    # Config
    parser.add_argument("-t", "--type", choices=["movie", "series"], help="Force specific media type (optional)")
    # Added Brave here
    parser.add_argument("--browser", choices=["chrome", "firefox"], default="chrome", help="Browser backend")
    parser.add_argument("--head", action="store_true", help="Run with browser visible (Headed mode)")
    parser.add_argument("--fast", action="store_true", help="Skip Reviews & Parental Guide for speed")
    parser.add_argument("-r", action="store_true", help="Deep scrape All Reviews (Slower)") 
    parser.add_argument("--no-html", action="store_true", help="Skip generating index.html")
    
    args = parser.parse_args()
    print_banner()

    # --- Exclusive Function Check ---
    if args.portable:
        make_portable(args.portable)
        sys.exit(0)

    # 1. Input Collection
    target_list = get_targets(args)
    
    # 2. Mode Validation
    if not target_list and not args.list: 
        print_status("No targets provided. Use --help for usage.", "WARN")
        sys.exit(0)

    # 3. List Logic
    append_path = ""
    
    if args.list:
        from jsons.generate import createList
        print_status(f"Setting up New List: {cyan}{args.list}{reset}", "INFO")
        append_path = createList(args.list) 
        print_status(f"List Environment Ready at: {append_path}", "SUCCESS")

    elif args.append:
        append_path = validate_append_path(args.append)
        print_status(f"Targeting List: {cyan}{append_path}{reset}", "INFO")

    elif len(target_list) > 1:
        # If user provides multiple links but no list, create a batch list automatically
        from jsons.generate import createList
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        auto_name = f"Batch_{timestamp}"
        print_status(f"Multiple targets detected. Auto-creating List: {yellow}'{auto_name}'{reset}", "WARN")
        append_path = createList(auto_name)

    # 4. Driver Init (With Animation)
    if target_list:
        headless_mode = not args.head
        driver = None
        
        try:
            # The spinner runs while this block executes
            with Spinner(message=f"Firing up {args.browser.capitalize()} driver..."):
                if args.browser == "chrome":
                    driver = chromeDriver(headless=headless_mode)
                else:
                    driver = firefoxDriver(headless=headless_mode)
            
            print_status(f"Driver Online ({args.browser})", "SUCCESS")

        except Exception as e:
            print("\n")
            print_status(f"Driver Initialization Failed: {e}", "ERROR")
            sys.exit(1)

        # 5. Processing Loop
        total = len(target_list)
        for idx, current_target in enumerate(target_list):
            print(f"\n{blue}--- [{idx+1}/{total}] Processing: {current_target} ---{reset}")
            
            # Type Logic
            current_type = args.type
            if append_path and current_type == "series":
                print_status("Skipping: Cannot add Series to a List (Movie lists only supported currently).", "ERROR")
                continue
            
            # Navigate
            if current_target != driver.current_url:
                searchByURL(driver, current_target)

            # Scrape
            try:
                fullScrape(
                    driver, 
                    media_type=current_type,
                    pg=not args.fast,
                    ur=not args.fast,
                    enhanced_ur=args.r,
                    create_html=not args.no_html,
                    append_to_filepath=append_path,
                    folder_name=None 
                )
            except KeyboardInterrupt:
                print_status("Skipping current item...", "WARN")
                continue
            except Exception as e:
                print_status(f"Scrape Error: {e}", "ERROR")
                pass

        driver.quit()
        print("\n")
        print_status("Operations Complete.", "SUCCESS")

if __name__ == "__main__":
    main()