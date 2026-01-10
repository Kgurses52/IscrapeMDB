import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utilities.cmd_colors import blue, yellow, red, reset

# Mute noisy selenium logs
logging.getLogger('selenium').setLevel(logging.ERROR)

# Mapping string selectors to Selenium 'By' objects
# This replaces the long 'if/else' chain
LOCATORS = {
    "CLASS_NAME": By.CLASS_NAME,
    "ID": By.ID,
    "XPATH": By.XPATH,
    "NAME": By.NAME,
    "CSS_SELECTOR": By.CSS_SELECTOR,
    "TAG_NAME": By.TAG_NAME,
    "LINK_TEXT": By.LINK_TEXT,
    "PARTIAL_LINK_TEXT": By.PARTIAL_LINK_TEXT
}

# ---------------------------------------------------------
# DRIVER INITIALIZATION
# ---------------------------------------------------------

def chromeDriver(headless: bool = True):
    options = ChromeOptions()
    _set_common_options(options, headless)
    
    # Chrome-specific options can go here if needed
    
    # --- 2. The Anti-Media Wall ---
    # Standard prefs to block content
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2, # Block CSS (Risky! formatting might break, but it's fast)
        "profile.managed_default_content_settings.fonts": 2, # Block Fonts
        "profile.managed_default_content_settings.cookies": 2, # Block Cookies (Speed boost, enable if site breaks)
        "profile.managed_default_content_settings.javascript": 1, # Keep JS (needed for 99% of sites)
        "profile.managed_default_content_settings.plugins": 2,
        "profile.managed_default_content_settings.popups": 2,
        "profile.managed_default_content_settings.geolocation": 2,
        "profile.managed_default_content_settings.media_stream": 2,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-features=PreloadMediaEngagementData,MediaEngagementBypassAutoplayPolicies")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.page_load_strategy = 'eager'  # Load DOM only, don't wait for all network requests
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    driver.set_window_size(960, 1080)
    return driver


def firefoxDriver(headless: bool = True):
    options = FirefoxOptions()
    _set_common_options(options, headless)
    
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install()),
        options=options
    )
    return driver


def _set_common_options(options, headless: bool):
    """
    Applies aggressive scraping options to the driver to kill media and speed up loading.
    """
    if headless:
        options.add_argument("--headless=new")

    # --- 1. Speed & Network Optimization ---
    options.add_argument("--dns-prefetch-disable")
    
    # Kill background networking/reporting tasks that slow things down
    options.add_argument("--disable-features=NetworkService,NetworkServiceInProcess")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-breakpad")  # Disables crash reporting
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-component-extensions-with-background-pages")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-hang-monitor")
    options.add_argument("--disable-ipc-flooding-protection")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-prompt-on-repost")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-sync")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--no-first-run")
    options.add_argument("--password-store=basic")
    options.add_argument("--use-mock-keychain")
    options.add_argument("--force-color-profile=srgb")


    # Flags to force-kill audio/video subsystems
    options.add_argument("--autoplay-policy=user-gesture-required")
    options.add_argument("--mute-audio")
    
    # Aggressive: Stop Chrome from reading/drawing canvas (often used for video players)
    options.add_argument("--disable-reading-from-canvas") 
    options.add_argument("--disable-remote-fonts") # Don't download fancy fonts
    options.add_argument("--disable-software-rasterizer")
    
    # --- 3. Stealth ---
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    options.add_argument('--log-level=3')
    
    def checkBrowser() -> str:
        """
        Checks if Chrome is available, falls back to Firefox.
        Properly closes the test instance to prevent memory leaks.
        """
        # Try Chrome
        try:
            driver = chromeDriver(headless=True)
            driver.get("https://www.google.com/")
            driver.quit() # Close it immediately!
            print(f"[{blue}Options{reset}] Default set to {yellow}Chrome{reset}")
            return "chrome"
        except Exception:
            pass # Silently fail and try Firefox

        # Try Firefox
        try:
            driver = firefoxDriver(headless=True)
            driver.get("https://www.google.com/")
            driver.quit() # Close it immediately!
            print(f"[{blue}Options{reset}] Default set to {yellow}FireFox{reset}")
            return "firefox"
        except Exception:
            print(f"[{red}Error{reset}] Make sure Chrome or Firefox is installed.")
            # We might want to raise an error here or let the main script handle None
            raise SystemExit("No valid browser driver found.")


# ---------------------------------------------------------
# ELEMENT INTERACTION
# ---------------------------------------------------------

def getEl(driver, by_string: str, value: str, timeout: int = 0):
    """
    Finds a single element. 
    """
    wait = WebDriverWait(driver, timeout)
    locator = LOCATORS.get(by_string)
    
    if not locator:
        raise ValueError(f"Invalid locator type: {by_string}")
        
    return wait.until(EC.presence_of_element_located((locator, str(value))))


def getEls(driver, by_string: str, value: str, timeout: int = 0):
    """
    Finds all matching elements.
    """
    wait = WebDriverWait(driver, timeout)
    locator = LOCATORS.get(by_string)
    
    if not locator:
        raise ValueError(f"Invalid locator type: {by_string}")

    return wait.until(EC.presence_of_all_elements_located((locator, str(value))))


def scrollDown(driver, pixels: int):
    driver.execute_script(f"window.scrollBy(0, {pixels});")


def scrollUp(driver, pixels: int):
    driver.execute_script(f"window.scrollBy(0, {-pixels});")


def text(web_element, remove_str=None, replace_with=None):
    """
    Safe extraction of text from an element.
    """
    try:
        val = web_element.get_attribute("textContent")
        if not val:
            return ""
        
        val = val.strip()
        
        if remove_str:
            # Handle replacement safely
            replacement = str(replace_with) if replace_with is not None else ""
            return val.replace(remove_str, replacement)
            
        return val
    except Exception:
        return "ERR"