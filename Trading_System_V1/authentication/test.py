import json
import logging
import os
import sys
import uuid
import random
import time
from urllib.parse import urlparse, parse_qs
from contextlib import contextmanager

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Adjust the path to include the pmClient directory where constants.py is located
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pmClient'))
from constants import Constants  # Import Constants

sys.path.append(os.path.dirname(__file__))  # Ensure the current directory is in sys.path for config.py
from config import API_KEY  # Import API_KEY from config.py
import login_creds

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@contextmanager
def undetected_chrome(options=None):
    driver = uc.Chrome(options=options)
    try:
        yield driver
    finally:
        driver.quit()

class PaytmMoneyAuth:
    def __init__(self, constants):
        self.constants = constants
        self.token_info_path = os.path.join(os.path.dirname(__file__), 'token_info.json')
        logging.info("Token info will be saved to a secure location.")

    def generate_state_key(self):
        """Generate a unique state key for CSRF protection."""
        return str(uuid.uuid4())

    def initiate_user_login(self):
        state = self.generate_state_key()
        login_url = self.constants._service_config['routes']['login'] + API_KEY
        full_url = f"{login_url}{self.constants._service_config['login_param']}{state}"

        options = uc.ChromeOptions()

        with undetected_chrome(options=options) as driver:
            wait = WebDriverWait(driver, 20000)

            logging.info("Navigating to the login page...")
            driver.get(full_url)
            time.sleep(random.uniform(2, 5))

            username_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="email"], input[type="text"]')))
            username_input.click()
            username_input.clear()
            username_input.send_keys(login_creds.USERNAME)

            password_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
            password_input.send_keys(login_creds.PASSWORD)

            sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[role='presentation'] > button")))
            sign_in_button.click()

            # Wait for the redirection to Google's site to complete
            wait.until(EC.url_contains("google.com"))

            current_url = driver.current_url
            parsed_url = urlparse(current_url)
            query_params = parse_qs(parsed_url.query)
            request_token = query_params.get('request_token', [None])[0]
            if request_token:
                logging.info(f"Request token found: {request_token}")
                self.save_request_token(request_token)
            else:
                logging.error("Request token not found in the URL or redirection did not occur as expected.")

    def save_request_token(self, request_token):
        try:
            with open(self.token_info_path, 'w') as file:
                json.dump({'request_token': request_token}, file, indent=4)
            logging.info("Request token saved successfully.")
        except Exception as e:
            logging.error(f"Failed to save request token: {e}")

    def read_request_token(self):
        try:
            with open(self.token_info_path, 'r') as file:
                token_info = json.load(file)
                request_token = token_info.get('request_token')
                logging.info("Request token read successfully.")
                return request_token
        except Exception as e:
            logging.error(f"Failed to read request token: {e}")
            return None

# Initialize constants
constants = Constants()

# Usage
if __name__ == "__main__":
    auth = PaytmMoneyAuth(constants)
    auth.initiate_user_login()
