import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

COOKIES_PATH = "src/utils/cookies.pkl"


def save_cookies():
    """Open a browser, let the user log in, then save session cookies."""
    options = Options()
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    driver.get("https://www.bestbuy.com/")
    input("🔵 Log in manually, then press ENTER to save cookies...")

    with open(COOKIES_PATH, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

    print("✅ Saved session cookies!")
    driver.quit()


if __name__ == "__main__":
    save_cookies()
