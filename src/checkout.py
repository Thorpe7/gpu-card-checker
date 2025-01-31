import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

log = logging.getLogger(__name__)


def proceed_to_checkout(driver, cart_url, cvv_num, dry_run=True):
    """Handles the checkout process but avoids final purchase if dry_run=True."""
    log.info("🚀 Navigating to cart...")
    driver.get(cart_url)
    time.sleep(2)

    if "Your Cart is Empty" in driver.page_source:
        log.info("❌ Error: Cart is empty. Cannot proceed to checkout.")
        return False

    try:
        log.info("🛒 Clicking 'Checkout'...")
        checkout_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Checkout')]")
            )
        )
        checkout_btn.click()
        time.sleep(2)

        log.info("📦 Selecting 'Delivery' option if available...")
        try:
            delivery_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[@type='radio'][contains(@value, 'DELIVERY')]")
                )
            )
            delivery_option.click()
            log.info("✅ Selected 'Delivery' option.")
            time.sleep(2)
        except:
            log.info("⚠️ Delivery option not found. Proceeding with default.")

        log.info("🔎 Checking for iframe before CVV entry...")
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        cvv_entered = False

        for index, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)

                cvv_input = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.ID, "cvv"))
                )

                log.info("✅ CVV field found! Entering CVV...")
                cvv_input.clear()
                cvv_input.send_keys(cvv_num)
                cvv_input.send_keys(Keys.TAB)
                cvv_entered = True

                driver.switch_to.default_content()
                break

            except Exception:
                driver.switch_to.default_content()

        if not cvv_entered:
            try:
                log.info("💳 Attempting to enter CVV directly (outside iframe)...")
                cvv_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "cvv"))
                )
                cvv_input.clear()
                cvv_input.send_keys(cvv_num)
                log.info("✅ CVV entered successfully!")

            except Exception as e:
                log.error(f"❌ CVV input field not found! Error: {e}")
                return False

        if dry_run:
            log.info("🚧 Dry-run mode enabled: Skipping 'Place Order' button!")
            return True

        log.info("✅ Placing order...")
        place_order_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Place Order')]")
            )
        )
        place_order_btn.click()

        time.sleep(5)
        if "Thank you for your order" in driver.page_source:
            log.info("🎉 Order placed successfully!")
            return True
        else:
            log.info("❌ Order placement failed. Check logs.")
            return False

    except Exception as e:
        log.error(f"❌ Error during checkout: {e}")
        return False
