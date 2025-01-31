"""Continuously check for item availability and add to cart when possible."""

import os
import time
import logging

from src.login_headless import setup_driver, cookie_login
from src.navigate_purchase import check_availability, add_to_cart
from src.checkout import proceed_to_checkout

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main(product_url, cart_url, product_id, cvv_num, check_interval, headless):
    driver = setup_driver(headless=headless)
    driver = cookie_login(driver)
    while True:
        if check_availability(product_url):
            if add_to_cart(driver, product_url, cart_url, product_id, False):
                logging.info("🎉 Success! Item is in your cart. Checkout now.")
                if proceed_to_checkout(driver, cart_url, cvv_num, dry_run=True):
                    break  # Stop checking if item is successfully added
                else:
                    logging.info("❌ Purchase failed.")
        else:
            logging.info(
                "❌ Item still sold out. Retrying in %s seconds...", check_interval
            )
        time.sleep(check_interval)

    driver.quit()


if __name__ == "__main__":

    TEST_URL = "https://www.bestbuy.com/site/msi-nvidia-geforce-rtx-4060-8gb-ventus-2x-oc-8gb-gddr6-pci-express-4-0-graphics-card-black/6548653.p?skuId=6548653"
    TEST_ID = "6548653"

    product_id = "6614151"
    product_url = "https://www.bestbuy.com/site/nvidia-geforce-rtx-5090-32gb-gddr7-graphics-card-dark-gun-metal/6614151.p?skuId=6614151"
    cart_url = "https://www.bestbuy.com/cart"
    check_interval = 50
    main(product_url, cart_url, product_id, "123", check_interval, headless=True)
