import time
import logging
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# === CONFIGURATION ===
COOKIES_PATH = "src/utils/cookies.pkl"  # File to store session cookies
HOME_URL = "https://www.bestbuy.com/"

# Enable logging for debugging
log = logging.getLogger(__name__)


def setup_driver(headless=True):
    """Initialize the WebDriver with improved headless stability."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Use a real User-Agent to prevent detection
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36"
    )

    driver = webdriver.Chrome(service=Service(), options=options)
    return driver


def load_cookies(driver):
    """Load saved cookies to authenticate the session."""
    try:
        driver.get("https://www.bestbuy.com/")
        time.sleep(1)

        with open(COOKIES_PATH, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)

        driver.refresh()
        time.sleep(5)

        print("✅ Loaded session cookies. User should be logged in.")
    except Exception as e:
        print("❌ Failed to load cookies:", e)


def cookie_login(driver):
    """Loads cookies and verifies login without re-entering credentials."""
    load_cookies(driver)

    # Verify login by checking if "Account" is visible
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(@class, 'c-button-unstyled')]")
            )
        )
        print("✅ Verified: User is logged in.")
    except:
        print("⚠️ Warning: Login may not have persisted.")

    return driver


if __name__ == "__main__":
    driver = setup_driver(headless=True)
    driver = cookie_login(driver)
