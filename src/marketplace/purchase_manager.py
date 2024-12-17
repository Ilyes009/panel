from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.logger import logger
from colorama import Fore
import time

class PurchaseManager:
    def __init__(self):
        self.confirmed_accounts = []
        self.owned_accounts = []
        self.sale_orders_value = None

    def prepare_purchase(self, webpage, sec, sub_purchase, main_purchase):
        try:
            driver = webpage.driver

            if not self._switch_to_iframe(driver, webpage.email):
                return False

            if self.sale_orders_value is None:
                self._get_sale_orders(driver, sec, webpage.email)

            self._set_purchase_value(driver, sec, webpage, sub_purchase, main_purchase)
            return True

        except Exception as e:
            logger.error(f"{webpage.email} preparation process failed: {e}")
            driver.quit()
            return False

    def _switch_to_iframe(self, driver, email):
        count = 5
        while count > 0:
            try:
                iframe = driver.execute_script(
                    'return document.querySelector("#app > div.r6s-marketplace.undefined > div > div > ubisoft-connect").shadowRoot.querySelector("iframe")'
                )
                if iframe:
                    driver.switch_to.frame(iframe)
                    logger.success(f"{email} logged in successfully!")
                    return True
            except Exception:
                count -= 1
                time.sleep(10)
        
        logger.error(f"Failed to switch to iframe for {email}")
        return False

    def _get_sale_orders(self, driver, sec, email):
        try:
            sale_orders_element = WebDriverWait(driver, sec).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div[3]/div[2]/div[2]/span[2]"))
            )
            self.sale_orders_value = int(sale_orders_element.text.replace(',', '').strip())
            logger.info(f"Current Amount Of Sale Orders: {self.sale_orders_value}", Fore.MAGENTA)
        except Exception as e:
            logger.error(f"Failed to retrieve sale orders value for {email}: {e}")

    def _set_purchase_value(self, driver, sec, webpage, sub_purchase, main_purchase):
        try:
            price_input = WebDriverWait(driver, sec).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='marketplace']/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[1]/div/div/div/input"))
            )
            price_input.click()
            purchase_value = main_purchase if webpage.status == "main" else sub_purchase
            price_input.send_keys(str(purchase_value))
            
            if webpage.status == "main":
                logger.info(f"Main account purchase value: {purchase_value}", Fore.BLUE)
            else:
                logger.info(f"Sub account purchase value: {purchase_value}", Fore.YELLOW)
            
            self.confirmed_accounts.append(webpage)
            
        except Exception:
            logger.error(f"The account {webpage.email} may already own this item (input field not accessible).")
            self.owned_accounts.append(webpage)

    def execute_purchase(self, webpage, sec):
        try:
            driver = webpage.driver
            
            # Click purchase button
            purchase_button = WebDriverWait(driver, sec).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='marketplace']/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[3]/button"))
            )
            logger.success(f"Pressing purchase button for {webpage.email}")
            purchase_button.click()

            # Click final confirmation
            final_confirm_button = WebDriverWait(driver, sec).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='shell-modal-id']/div/div[3]/div/div/button[2]"))
            )
            logger.success(f"Pressing final confirmation button for {webpage.email}")
            final_confirm_button.click()
            
            return True

        except Exception as e:
            logger.error(f"{webpage.email} purchase execution failed: {e}")
            return False