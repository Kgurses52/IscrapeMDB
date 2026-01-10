import time
from typing import Optional

# Local imports
from driver.driver import getEl, getEls, text
from driver.search import searchByURL
from jsons.load import els
from utilities.files import create_folder, createIndexMovie, createIndexSeries, make_safe_folder_name
from utilities.cmd_colors import green, yellow, blue, cyan, reset

# Import specific functions from getData to avoid namespace pollution
from driver.getData import (
    getTargetInfo, getTargetCast, getTargetRuntime, getTargetDirs,
    getTargetPG, getTargetRev, getEpsCount, getEpsAddress, getType
)

# ---------------------------------------------------------
# MAIN SCRAPER
# ---------------------------------------------------------

def fullScrape(
    driver,
    media_type: Optional[str] = None,
    pg: bool = True,
    ur: bool = True,
    enhanced_ur: bool = False,
    main_id: str = "main",
    just_main: bool = False,
    folder_name: Optional[str] = None,
    create_html: bool = True,
    append_to_filepath: str = ""
):
    """
    Main orchestration function to scrape data and save it.
    """
    
    # --- 1. Basic Info ---
    target_title, target_date, target_rate, target_description = getTargetInfo(driver)
    
    # Sanitize title for folder usage
    safe_title = make_safe_folder_name(target_title)

    # Determine Folder Name
    if not folder_name:
        # aggressive safety check on date split in case date is "None"
        date_year = target_date.split(" ")[0] if target_date and target_date != "None" else "Unknown"
        folder_name = f"{safe_title} ({date_year})"

    # Determine Type (Series vs Movie)
    if media_type is None:
        media_type = checkType(driver)

    # --- 2. Path Setup ---
    json_path = ""
    
    # Logic for base path selection
    if append_to_filepath:
        main_id = target_title # Override ID if appending (e.g. for episodes)
        json_path = f"{append_to_filepath}/data/"
    elif media_type == "series":
        base_path = f"Scraped/Series/{folder_name}"
        create_folder(f"{base_path}/data/")
        json_path = f"{base_path}/data/"
        if create_html:
            createIndexSeries(f"{base_path}/")
    else: # Default to movie
        main_id = target_title
        base_path = f"Scraped/Movies/{folder_name}"
        create_folder(f"{base_path}/data/")
        json_path = f"{base_path}/data/"
        if create_html:
            createIndexMovie(f"{base_path}/")

    # --- 3. Recording Base Data ---
    # Using 'create_js' only once per file usually, or appending.
    # Assuming create_js initializes/clears the file.
    if not append_to_filepath: # Only create main.js if we are at the root level
        from jsons.generate import create_js 
        create_js(f"{json_path}main.js")

    from jsons.generate import write_js
    
    # Batch write basic info
    write_js(f"{json_path}main.js", "Title", target_title, main_id)
    write_js(f"{json_path}main.js", "Date", target_date, main_id)
    write_js(f"{json_path}main.js", "Rate", target_rate, main_id)
    write_js(f"{json_path}main.js", "Description", target_description, main_id)

    # --- 4. Additional Data ---
    target_cast = getTargetCast(driver)
    target_runtime = getTargetRuntime(driver)
    target_dirs = getTargetDirs(driver)

    write_js(f"{json_path}main.js", "Cast", target_cast, main_id)
    write_js(f"{json_path}main.js", "Runtime", target_runtime, main_id)
    write_js(f"{json_path}main.js", "Directors", target_dirs, main_id)

    # --- 5. Optional Data (Parents Guide & Reviews) ---
    
    # Parents Guide
    if pg:
        parents_guide = getTargetPG(driver)
        
        if parents_guide is None:
            log_subject = main_id if main_id != "main" else target_title
            print(f"[{cyan}UNFOUND{reset}] Can't find {blue}Parents Guide{reset} data for {log_subject}")
        
        write_js(f"{json_path}main.js", "ParentsGuide", parents_guide, main_id)

    # Reviews
    if ur:
        # Only create review file if it's the main scrape, otherwise append?
        # Assuming we want a separate review.js
        if not append_to_filepath:
             from jsons.generate import create_js
             create_js(f"{json_path}review.js")
             
        reviews = getTargetRev(driver, enhanced_ur)
        
        if reviews is None:
            log_subject = main_id if main_id != "main" else target_title
            print(f"[{cyan}UNFOUND{reset}] Can't find {blue}Reviews{reset} data for {log_subject}")
            write_js(f"{json_path}review.js", "Reviews", None, main_id)
        else:
            # FIXED: Removed the loop that wrote the same list multiple times.
            # Just write the list once.
            write_js(f"{json_path}review.js", "Reviews", reviews, main_id)

    # --- 6. Series Handling ---
    if not just_main and media_type == "series":
        eps_count = getEpsCount(driver)
        # Determine review count for series logic if needed, otherwise pass 0
        review_count = len(reviews) if reviews else 0
        fullScrapeSeries(driver, eps_count, folder_name, pg=pg, ur=ur, urs=review_count)


# ---------------------------------------------------------
# SERIES SPECIFIC
# ---------------------------------------------------------

def fullScrapeSeries(driver, eps_count, folder_name, pg=True, ur=True, urs=0):
    """
    Iterates through episodes of a series.
    """
    url = driver.current_url
    clean_url = url[:url.rfind('/') + 1]
    
    # Go to episodes list
    searchByURL(driver, clean_url + "episodes/")

    # Enter the first episode
    try:
        first_eps_info = els["firstEps"]
        first_eps_els = getEls(driver, first_eps_info["by"], first_eps_info["value"])
        if not first_eps_els:
            print(f"[{yellow}WARN{reset}] No episodes found.")
            return
        driver.get(first_eps_els[0].get_attribute("href"))
    except Exception as e:
        print(f"[{yellow}ERROR{reset}] Could not enter first episode: {e}")
        return

    # Loop through episodes
    # Starting from 1 implies we scrape the first one inside the loop
    for i in range(1, eps_count + 1): # Added +1 to cover the last episode if count is exact
        start_time = time.perf_counter()
        
        eps_address = getEpsAddress(driver)
        # Sanitize episode address for file system
        eps_address = eps_address.replace(".", "").strip()
        
        # Recursive call for the episode
        # Note: We pass just_main=True to stop infinite recursion
        fullScrape(
            driver, 
            media_type="series", 
            pg=pg, 
            ur=ur, 
            enhanced_ur=False, 
            main_id=eps_address, 
            just_main=True, 
            folder_name=folder_name, 
            create_html=False,
            append_to_filepath=f"Scraped/Series/{folder_name}"
        )

        # Navigation to next episode
        # Only click next if we aren't at the last episode
        if i < eps_count:
            try:
                next_btn_info = els["nextEpsBtn"]
                next_btn = getEl(driver, next_btn_info["by"], next_btn_info["value"])
                next_btn.click()
            except Exception:
                print(f"[{yellow}WARN{reset}] Could not click next episode button at E{i}.")
                break

        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"[{green}DONE{reset}] E{i}/{eps_count} {yellow}--{reset} elapsed: {yellow}{duration:.2f}{reset}sec ")



def checkType(driver) -> str:
    """
    Determines if the target is a Series or a Movie.
    """
    type_text = getType(driver)
    
    # If the text contains typical Series keywords
    if "Series" in type_text or "TV" in type_text or "Episode" in type_text:
        print(f"[{blue}INFO{reset}] Auto checked type : Series")
        return "series"
    
    # Default to movie if Unknown or explicit Movie
    print(f"[{blue}INFO{reset}] Auto checked type : Movie")
    return "movie"