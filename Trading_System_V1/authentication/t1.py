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
from pyzbar.pyzbar import decode
from PIL import Image
import pyotp

# Ensure the 'pmClient' directory is in sys.path for importing Constants
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pmClient'))
from constants import Constants
sys.path.append(os.path.dirname(__file__))  # For importing config and login credentials
from config import API_KEY
import login_creds

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@contextmanager
def undetected_chrome(options=None):
    if options is None:
        options = uc.ChromeOptions()
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

    def get_login_url(self):
        """Construct the login URL with the API key and state parameter."""
        state = self.generate_state_key()
        login_url = self.constants._service_config['routes']['login'] + API_KEY
        full_url = f"{login_url}{self.constants._service_config['login_param']}{state}"
        return full_url

    def generate_totp(self):
        """Generate TOTP using the secret key stored in a QR code."""
        qr_image = Image.open('qr.png')  # Ensure the QR code image is available at this path
        decoded_data = decode(qr_image)
        uri = decoded_data[0].data.decode()
        secret_key = uri.split('secret=')[1].split('&')[0]
        totp = pyotp.TOTP(secret_key)
        return totp.now()

    def initiate_user_login(self):
        with undetected_chrome() as driver:
            wait = WebDriverWait(driver, 20)
            logging.info("Navigating to the login page...")
            driver.get(self.get_login_url())

            time.sleep(random.uniform(2, 5))  # Random delay to mimic human behavior

            username_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="email"], input[type="text"]')))
            username_input.click()
            username_input.clear()
            username_input.send_keys(login_creds.USERNAME)

            password_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
            password_input.send_keys(login_creds.PASSWORD)

            sign_in_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span[role='presentation'] > button")))
            sign_in_button.click()

            logging.info("Please enter the OTP manually and click Submit.")
            initial_login_url = driver.current_url

            # Wait for the user to manually enter the OTP and detect URL change to proceed
            WebDriverWait(driver, 300).until_not(lambda driver: driver.current_url == initial_login_url)
            logging.info("Detected URL change, proceeding to TOTP input...")

            # After detecting the URL change, wait for 5 seconds to ensure the TOTP page is fully loaded
            time.sleep(5)

            # Now proceed with the TOTP input automatically
            totp_fields = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="password"]'))
            )

            totp_code = self.generate_totp()
            if len(totp_code) == len(totp_fields):
                for digit, field in zip(totp_code, totp_fields):
                    field.send_keys(digit)
                    time.sleep(1)  # Wait for 1 second between each digit entry
            else:
                logging.error("The length of the TOTP code does not match the number of input fields.")

            # After entering the TOTP, locate the submit button and click it
            totp_submit_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit')]"))
            )
            totp_submit_button.click()

            # Wait for any redirection to occur after the TOTP submission
            WebDriverWait(driver, 30).until(lambda d: d.current_url != initial_login_url)
            current_url = driver.current_url
            logging.info(f"Redirected to URL: {current_url}")  # Log the redirected URL for verification
            parsed_url = urlparse(current_url)
            query_params = parse_qs(parsed_url.query)
            request_token = query_params.get('request_token', [None])[
                0]  # Adjust 'request_token' as per actual query param name

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

if __name__ == "__main__":
    constants = Constants()
    auth = PaytmMoneyAuth(constants)
    auth.initiate_user_login()
