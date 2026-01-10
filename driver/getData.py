from typing import List, Dict, Tuple, Optional, Any
import time

# Local imports
from driver.driver import getEl, getEls, scrollDown, scrollUp, text
from driver.search import searchByURL
from jsons.load import els
from utilities.cmd_colors import errorElement

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

# Elements in this list will NOT show an error message if missing.
# This keeps the console clean for optional data.
SILENT_ELEMENTS = [
    "targetType", 
    "reviewAllbtn", 
    "parentsGuide", 
    "parentsGuideRating",
    "parentsGuideType"
] 

def _log_missing_element(element_name: str):
    """
    Wrapper for errorElement to allow silencing specific errors.
    """
    if element_name not in SILENT_ELEMENTS:
        errorElement(element_name)

# ---------------------------------------------------------
# TARGET INFORMATION
# ---------------------------------------------------------

def getTargetInfo(driver) -> Tuple[str, str, str, str]:
    """
    Retrieves the main title, date, rating, and description of the target.
    Returns "None" and logs an error if an element is missing.
    """
    data = {}
    fields = ["targetTitle", "targetDate", "targetRate", "targetDescription"]

    for field in fields:
        try:
            info = els[field]
            element = getEl(driver, info["by"], info["value"])
            data[field] = element
        except Exception:
            data[field] = "None"
            _log_missing_element(field)

    # Formatting specific return values as requested
    return (
        text(data["targetTitle"]),
        text(data["targetDate"], "–", " - "),
        text(data["targetRate"]),
        text(data["targetDescription"], "–", "-")
    )


def getTargetPG(driver, retry: bool = False) -> Optional[List[Dict[str, str]]]:
    """
    Scrapes the Parental Guide.
    Uses a 'retry' flag instead of recursion to prevent infinite loops.
    """
    cache = []
    target_url = driver.current_url
    # Clean URL extraction
    base_url = target_url[:target_url.rfind('/') + 1]
    
    # Navigate to parental guide
    searchByURL(driver, f"{base_url}parentalguide/")

    try:
        pg_info = els["parentsGuide"]
        parents_guide = getEls(driver, pg_info["by"], pg_info["value"])
        
        for item in parents_guide:
            rate_info = els["parentsGuideRating"]
            type_info = els["parentsGuideType"]
            
            pg_rating = getEl(item, rate_info["by"], rate_info["value"])
            pg_type = getEl(item, type_info["by"], type_info["value"])
            
            cache.append({
                "type": text(pg_type),
                "rate": text(pg_rating)
            })

    except Exception:
        # If it fails and we haven't retried yet, try once more
        if not retry:
            searchByURL(driver, target_url)
            return getTargetPG(driver, retry=True)
        else:
            # If it fails twice, return None to avoid crash
            searchByURL(driver, target_url)
            # Log it silently if configured
            _log_missing_element("parentsGuide")
            return None

    # Return to original page before returning data
    searchByURL(driver, target_url)
    return cache


def getTargetRev(driver, enhanced: bool = True) -> Any:
    """
    Scrapes user reviews. 
    Enhanced mode attempts to click 'All' and scroll down to load more.
    """
    cache = []
    target_url = driver.current_url
    base_url = target_url[:target_url.rfind('/') + 1]
    
    searchByURL(driver, f"{base_url}reviews/?ref_=tt_ururv_sm&spoilers=EXCLUDE")

    if enhanced:
        try:
            clicked = clickReviewAll(driver)
            if clicked:
                # Loop replaces the repetitive copy-paste scrolling
                for _ in range(8):
                    scrollDown(driver, 500000)
                    time.sleep(1)
        except Exception as e:
            scrollUp(driver, 10000)
            return e

    try:
        title_info = els["reviewTitle"]
        content_info = els["reviewContent"]

        review_titles = getEls(driver, title_info["by"], title_info["value"])
        review_contents = getEls(driver, content_info["by"], content_info["value"])

        # Ensure we don't index out of bounds if lists are different sizes
        size = min(len(review_titles), len(review_contents))
        
        for i in range(size):
            cache.append({
                "title": text(review_titles[i]),
                "content": text(review_contents[i])
            })

    except Exception:
        searchByURL(driver, target_url)
        return None, None
    
    searchByURL(driver, target_url)
    return cache


def getTargetCast(driver) -> Optional[List[Dict[str, str]]]:
    """
    Scrapes the cast list and their roles.
    """
    cast_data = []

    try:
        # Fetch Names
        try:
            name_info = els["castName"]
            cast_names = getEls(driver, name_info["by"], name_info["value"])
        except Exception:
            _log_missing_element("castName")
            cast_names = []

        # Fetch Roles
        try:
            role_info = els["castRole"]
            cast_roles = getEls(driver, role_info["by"], role_info["value"])
        except Exception:
            _log_missing_element("castRole")
            cast_roles = []

        # Pair them up
        limit = min(len(cast_names), len(cast_roles))
        for i in range(limit):
            role_text = cast_roles[i].get_attribute("innerText") or ""
            cast_data.append({
                "name": text(cast_names[i]),
                "role": role_text.replace("\n", " ")
            })
            
        return cast_data

    except Exception:
        return None


def getTargetRuntime(driver) -> Optional[str]:
    """
    Scrolls down to find runtime, scrapes it, then scrolls back up.
    """
    scrollDown(driver, 8000)
    try:
        rt_info = els["runtime"]
        runtime = getEl(driver, rt_info["by"], rt_info["value"])
        scrollUp(driver, 8000)
        return text(runtime)
    except Exception:
        scrollUp(driver, 3000)
        _log_missing_element("runtime")
        return None


def getTargetDirs(driver) -> Optional[List[str]]:
    """
    Scrapes directors. Returns a list of unique director names.
    """
    cache_dirs = []
    try:
        dirs_info = els["targetDirs"]
        target_dirs = getEls(driver, dirs_info["by"], dirs_info["value"])
    except Exception:
        _log_missing_element("targetDirs")
        return None

    for item in target_dirs:
        dir_name = text(item)
        if dir_name not in cache_dirs:
            cache_dirs.append(dir_name)
            
    return cache_dirs


# ---------------------------------------------------------
# SERIES FIELDS
# ---------------------------------------------------------

def getEpsCount(driver) -> int:
    """
    Returns the total episode count as an integer.
    """
    info = els["epsCount"]
    # Handle case where element might not exist or text is not an int
    try:
        eps_count_els = getEls(driver, info["by"], info["value"])
        return int(eps_count_els[0].text)
    except (IndexError, ValueError, Exception):
        return 0

def getEpsAddress(driver) -> str:
    """
    Returns the text address/title of the episode list.
    """
    info = els["epsAddress"]
    eps_address = getEl(driver, info["by"], info["value"])
    return eps_address.text if eps_address else ""


# ---------------------------------------------------------
# UTILITIES
# ---------------------------------------------------------

def clickReviewAll(driver) -> bool:
    """
    Attempts to click the 'All Reviews' button using JS to bypass overlays.
    """
    try:
        btn_info = els["reviewAllbtn"]
        btn = getEl(driver, btn_info["by"], btn_info["value"])

        if btn:
            # JS execution is more reliable for hidden/overlayed buttons
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            driver.execute_script("arguments[0].click();", btn)
            return True
    except Exception:
        # Silenced via wrapper
        _log_missing_element("reviewAllbtn")
    
    return False


def getType(driver) -> str:
    """
    Retrieves the media type (e.g., TV Series, Movie).
    """
    try:
        info = els["targetType"]
        target_type = getEl(driver, info["by"], info["value"])
        return text(target_type)
    except Exception:
        _log_missing_element("targetType")
        return "Unknown"