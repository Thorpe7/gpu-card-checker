"""Continuously check for item availability and add to cart when possible."""

import time
import logging
import argparse

from src.login_headless import setup_driver, cookie_login
from src.navigate_purchase import check_availability, add_to_cart
from src.checkout import proceed_to_checkout

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

CHECK_INTERVAL = 50


def main(product_url, cart_url, product_id, cvv_num, check_interval, headless, dry_run):
    driver = setup_driver(headless=headless)
    driver = cookie_login(driver)
    while True:
        if check_availability(product_url):
            if add_to_cart(driver, product_url, cart_url, product_id, False):
                logging.info("🎉 Success! Item is in your cart. Checkout now.")
                if proceed_to_checkout(driver, cart_url, cvv_num, dry_run=dry_run):
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

    parser = argparse.ArgumentParser()
    parser.add_argument("product_url", type=str, help="URL of the product.")
    parser.add_argument("product_id", type=str, help="The SKU ID for the product.")
    parser.add_argument("cart_url", type=str, help="The URL to your cart.")
    parser.add_argument(
        "--cvv", type=str, help="CVV for your stored payment information"
    )
    parser.add_argument("--dry-run", action="store_true", help="Enable dry-run mode.")

    args = parser.parse_args()
    main(
        product_url=args.product_url,
        product_id=args.product_id,
        cart_url=args.cart_url,
        cvv_num=args.cvv,
        check_interval=10,
        headless=True,
        dry_run=args.dry_run,
    )
