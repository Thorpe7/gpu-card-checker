import time
import logging
import requests
import webbrowser
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

log = logging.getLogger(__name__)


def check_availability(product_url):
    """Check if the item is available for purchase."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(product_url, headers=headers)
    if response.status_code != 200:
        log.info("❌ Failed to fetch page.")
        return False

    soup = BeautifulSoup(response.text, "html.parser")
    add_to_cart_btn = soup.find("button", {"data-button-state": "ADD_TO_CART"})

    return add_to_cart_btn is not None  # Returns True if item is available


import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

log = logging.getLogger(__name__)


def add_to_cart(driver, product_url, cart_url, sku_id):
    """Adds a product to the cart and waits for queue processing."""
    log.info(f"🚀 Navigating to product page: {product_url}")
    driver.get(product_url)
    time.sleep(2)  # Allow page to load

    try:
        log.info("🔍 Checking for 'Add to Cart' button...")
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//button[@data-sku-id='{sku_id}' and contains(@data-button-state, 'ADD_TO_CART')]",
                )
            )
        )
        add_to_cart_btn.click()
        log.info("🛒 Clicked 'Add to Cart'!")

        # Wait on the page to check if we enter a queue
        log.info("⏳ Waiting for cart processing...")

        queue_timeout = 120  # Maximum wait time in seconds
        start_time = time.time()

        while time.time() - start_time < queue_timeout:
            time.sleep(5)  # Avoid excessive requests
            if "Your item has been added to cart" in driver.page_source:
                log.info("✅ Item successfully added to cart!")
                break
            elif "You're in line" in driver.page_source:
                log.info("⏳ Still in queue, waiting...")
            else:
                log.info("🔄 Checking cart status...")
                driver.refresh()  # Refresh to check if queue clears

        # Navigate to cart and confirm item is there
        log.info("🛒 Navigating to cart to confirm...")
        driver.get(cart_url)
        time.sleep(3)

        if "Your Cart is Empty" in driver.page_source:
            log.info("❌ Item not in cart. It may have sold out.")
            return False
        else:
            log.info("✅ Item is in cart! Ready for checkout.")
            return True

    except Exception as e:
        log.error(f"❌ Error during add to cart: {e}")
        return False
