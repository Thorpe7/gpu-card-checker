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


def add_to_cart(driver, product_url, cart_url, sku_id, open_browser):
    """Adds product of interest to your cart."""
    driver.get(product_url)
    time.sleep(1)
    try:
        # sku id for locating 'add to cart'
        add_to_cart_btn = driver.find_element(
            By.XPATH,
            f"//button[@data-sku-id='{sku_id}' and contains(@data-button-state, 'ADD_TO_CART')]",
        )
        add_to_cart_btn.click()
        log.info("🛒 Successfully added item to Cart!")

        time.sleep(1)
        driver.get(cart_url)

        # Check if item is in the cart
        time.sleep(1)
        if "Your Cart is Empty" not in driver.page_source:
            log.info("✅ Item is in cart! Opening browser for checkout...")
            if open_browser:  # Enable if you want bot to open your cart before purchase
                webbrowser.open(cart_url)
            return True
        else:
            log.info("❌ Item not in cart. Retrying...")
            return False

    except Exception as e:
        # Check if "Sold Out" message exists
        if "Sold Out" in driver.page_source:
            log.info("⚠️ Item is out of stock!")
        else:
            log.info("❌ Could not find 'Add to Cart' button!")

        return False
