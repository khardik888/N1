import json
import logging
import os
import uuid
from urllib.parse import urlparse, parse_qs
import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyzbar.pyzbar import decode
from PIL import Image
import pyotp
from pyPMClient_master.pmClient.pmClient import PMClient
from pyPMClient_master.pmClient.constants import Constants
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def enter_otp(driver):
    logging.info("Prompting for OTP input.")
    # Directly prompt for OTP in the console without checking for the OTP input box presence.
    otp = input("Please enter the OTP sent to your mobile number: ")

    # Attempt to find the OTP input boxes. If found, fill them in.
    try:
        otp_inputs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="password"][maxlength="1"]')))
        for digit, otp_input in zip(otp, otp_inputs):
            otp_input.send_keys(digit)
        logging.info("OTP entered into the found input boxes.")
    except TimeoutException:
        logging.warning("Could not locate OTP input boxes. Please ensure you manually complete the OTP verification in the browser.")

    # Attempt to find and click the next/submit button.
    try:
        next_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[role='presentation'] > button")))
        next_button.click()
    except TimeoutException:
        logging.error("Next button not found. Please manually click the next button in the browser.")58


class PaytmMoneyAuth:
    def __init__(self):
        self.constants = Constants()
        self.token_info_path = os.path.join(os.path.dirname(__file__), 'token_info.json')
        logging.info("Token info will be saved to a secure location.")
        self.pm_client = PMClient(api_secret=config.API_SECRET, api_key=config.API_KEY)

    def generate_state_key(self):
        return str(uuid.uuid4())

    def get_login_url(self):
        state = self.generate_state_key()
        return f"{self.constants._service_config['routes']['login']}{config.API_KEY}{self.constants._service_config['login_param']}{state}"

    def generate_totp(self):
        decoded_data = decode(Image.open('qr.png'))
        secret_key = decoded_data[0].data.decode().split('secret=')[1].split('&')[0]
        return pyotp.TOTP(secret_key).now()

    def initiate_user_login(self):
        try:
            with self.setup_driver() as driver:
                self.navigate_and_authenticate(driver)
        except WebDriverException as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise

    def setup_driver(self):
        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options)
        driver.__enter__ = lambda *args: driver
        driver.__exit__ = lambda *args: driver.quit()
        return driver

    def navigate_and_authenticate(self, driver):
        driver.get(self.get_login_url())
        self.enter_credentials_and_authenticate(driver)

    def enter_credentials_and_authenticate(self, driver):
        wait = WebDriverWait(driver, 20)
        username_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="email"], input[type="text"]')))
        password_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
        sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[role='presentation'] > button")))

        username_input.send_keys(config.USERNAME)
        password_input.send_keys(config.PASSWORD)
        sign_in_button.click()

        # Wait until not on the login URL anymore to ensure navigation has occurred
        WebDriverWait(driver, 20).until_not(EC.url_to_be(self.get_login_url()))

    def enter_totp(self, driver):
        totp_code = self.generate_totp()
        totp_fields = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="password"]')))

        for digit, field in zip(totp_code, totp_fields):
            field.send_keys(digit)

        submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit')]")))
        submit_button.click()

        WebDriverWait(driver, 30).until_not(EC.url_to_be(driver.current_url))
        self.save_access_tokens(driver.current_url)

    def save_access_tokens(self, url):
        request_token = self.extract_token(url)
        access_tokens = self.pm_client.generate_session(request_token=request_token) if request_token else None
        if access_tokens:
            with open('access_tokens.json', 'w') as file:
                json.dump(access_tokens, file, indent=4)
            logging.info("Access tokens saved successfully.")
        else:
            logging.error("Failed to obtain access tokens.")

    def extract_token(self, url):
        query_params = parse_qs(urlparse(url).query)
        return query_params.get('requestToken', [None])[0]

# Creating and using the PaytmMoneyAuth instance
paytm_money_auth = PaytmMoneyAuth()
paytm_money_auth.initiate_user_login()
