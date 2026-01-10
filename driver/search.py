from typing import List, Tuple
from selenium.webdriver.common.keys import Keys
from driver.driver import getEl, getEls, scrollDown
from jsons.load import els

# ---------------------------------------------------------
# SEARCH FUNCTIONS
# ---------------------------------------------------------

def searchByName(driver, target_name: str) -> Tuple[List[str], List[str]]:
    """
    Searches for a title on IMDb and returns lists of Hrefs and Titles.
    Returns empty lists if nothing found or critical error occurs.
    """
    
    # 1. Go to Home
    driver.get("https://www.imdb.com/")

    # 2. Perform Search
    try:
        search_info = els["searchBar"]
        search_bar = getEl(driver, search_info["by"], search_info["value"])
        search_bar.send_keys(target_name + Keys.ENTER)
    except Exception:
        # If we can't even search, return empty immediately
        return [], []

    # 3. Filter for "Exact Match" / "Titles"
    # We use a short timeout and try/except because this button isn't always there
    try:
        exact_info = els["extactBtn"] # Keeping your JSON key name despite the typo
        exact_btn = getEl(driver, exact_info["by"], exact_info["value"], timeout=2)
        exact_btn.click()
    except Exception:
        pass # It's fine if this fails, we might already be on the results page

    # 4. Parse Results
    try:
        results_div = els["resultsDiv"]
        results = getEls(driver, results_div["by"], results_div["value"])
    except Exception:
        return [], []

    title_hrefs = []
    title_texts = []

    for result in results:
        try:
            # We look *inside* the result element
            t_info = els["resultTitle"]
            d_info = els["resultDate"]

            # fast timeout (1s) because elements should be loaded if parent is loaded
            result_title = getEl(result, t_info["by"], t_info["value"], timeout=1)
            result_date = getEl(result, d_info["by"], d_info["value"], timeout=1)

            title_hrefs.append(result_title.get_attribute("href"))
            title_texts.append(f"{result_title.text} ({result_date.text})")
            
            # Small scroll to keep interaction "human" and trigger lazy loads
            scrollDown(driver, 200)

        except Exception:
            # CRITICAL FIX: If one result is bad, SKIP IT. Do not return the error.
            continue

    return title_hrefs, title_texts


def searchByURL(driver, url: str):
    """
    Navigates the driver to a specific URL, ensuring protocol presence.
    """
    url = url.strip()
    
    if not url.lower().startswith("http"):
        url = "https://" + url

    driver.get(url)