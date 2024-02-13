import json
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pyotp
import sys

# Importing credentials and constants
sys.path.append(os.path.dirname(__file__))  # Adjust as necessary to import from the current directory
import login_creds
from constants import Constants  # Ensure this module exists in your project structure

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PaytmMoneyAuth:
    def __init__(self, constants):
        self.constants = constants
        self.token_info_path = os.path.join(os.path.dirname(__file__), 'request_token.json')
        logging.info("Token info will be saved to a secure location.")

    def initiate_user_login(self):
        """Use Selenium to navigate and login, including handling TOTP."""
        # Construct the login URL
        login_url = self.constants._service_config['routes']['login'] + self.constants.API_KEY
        state = 'your_unique_state_value'
        full_url = f"{login_url}{self.constants._service_config['login_param']}{state}"

        # Setup Selenium WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        logging.info("Navigating to the login page...")
        try:
            driver.get(full_url)

            # Fill in the login form
            driver.find_element_by_name("username").send_keys(login_creds.USERNAME)
            driver.find_element_by_name("password").send_keys(login_creds.PASSWORD)
            driver.find_element_by_name("password").send_keys(Keys.RETURN)  # Submit the form

            # Handling TOTP
            totp = pyotp.TOTP(login_creds.TOTP_SECRET).now()
            logging.info(f"Generated TOTP: {totp}")
            # Assuming there's an element to input TOTP, replace 'totp_field_name' with the actual field name or ID
            totp_input = driver.find_element_by_name("totp_field_name")
            totp_input.send_keys(totp)
            totp_input.send_keys(Keys.RETURN)

            logging.info("Login process initiated with TOTP submitted.")
        except Exception as e:
            logging.error(f"An error occurred during the login process: {e}")
        finally:
            # Consider whether you want to close the browser automatically
            # driver.quit()

    def save_request_token(self, request_token):
        try:
            with open(self.token_info_path, 'w') as file:
                json.dump({'request_token': request_token}, file, indent=4)
            logging.info("Request token saved successfully.")
        except Exception as e:
            logging.error("Failed to save request token.")

    def read_request_token(self):
        """Read the request token from a JSON file."""
        try:
            with open(self.token_info_path, 'r') as file:
                token_info = json.load(file)
                request_token = token_info.get('request_token')
                logging.info("Request token read successfully.")
                return request_token
        except Exception as e:
            logging.error("Failed to read request token.")
            return None

    def input_and_save_request_token(self):
        """Prompt the user for the request token and save it."""
        request_token = input("Please enter the request token: ").strip()
        if request_token:
            self.save_request_token(request_token)
        else:
            logging.warning("No request token entered. Please try again.")

constants = Constants()

# Usage
constants = Constants()  # Ensure this correctly initializes your constants
auth = PaytmMoneyAuth(constants)
auth.initiate_user_login()

# New functionality to input and save the request token
auth.input_and_save_request_token()
