import secrets
import logging
import requests
from urllib.parse import urlencode
from execution.pmClient.pmClient import PMClient
from .token_manager import TokenManager
from authentication.config import API_KEY, API_SECRET

class Auth:
    AUTH_BASE_URL = 'https://login.paytmmoney.com/merchant-login'

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.token_manager = TokenManager()
        self.pm_client = PMClient(api_key=self.api_key, api_secret=self.api_secret)
        self.token_info = self.token_manager.get_tokens()
        self.access_token = self.token_info.get('access_token')
        self.logger.info("API credentials loaded and PMClient initialized successfully.")

    def generate_auth_url(self):
        state = secrets.token_urlsafe()
        params = {'apiKey': self.api_key, 'state': state}
        auth_url = f"{self.AUTH_BASE_URL}?{urlencode(params)}"
        self.logger.info(f"Authentication URL generated: {auth_url}")
        return auth_url

    def exchange_request_token(self, request_token):
        session_output = self.pm_client.generate_session(request_token)
        self.logger.info(f"Session output: {session_output}")

        if 'access_token' in session_output:
            self.token_manager.save_tokens(
                access_token=session_output['access_token'],
                public_access_token=session_output.get('public_access_token'),
                read_access_token=session_output.get('read_access_token'))
            self.access_token = session_output['access_token']
            self.logger.info("Access token retrieved and saved successfully.")
            return True
        else:
            self.logger.error("Required token not found in the session data. Session Output: " + str(session_output))
            return False

    def validate_access_token(self):
        if not self.access_token:
            self.logger.error("Access token is not available.")
            return False

        url = "https://developer.paytmmoney.com/accounts/v1/user/details"
        headers = {"x-jwt-token": self.access_token}
        try:
            response = requests.get(url, headers=headers)
            self.logger.debug(f"Validation Request: URL={url}, Headers={headers}")
            self.logger.debug(f"Validation Response: Status={response.status_code}, Body={response.text}")

            if response.status_code == 200:
                self.logger.info("Access token validation successful.")
                return True
            else:
                self.logger.error(f"Access token validation failed. HTTP status: {response.status_code}, Response: {response.json()}")
                return False
        except Exception as e:
            self.logger.error(f"Exception in token validation: {e}")
            return False

    def reauthenticate(self):
        self.logger.info("Reauthentication required. Please authenticate again.")
        auth_url = self.generate_auth_url()
        self.logger.info(f"Authentication URL: {auth_url}")
        request_token = input("After authentication, please enter the request token here: ")

        if self.exchange_request_token(request_token):
            self.logger.info("Reauthentication successful.")
            return True
        else:
            self.logger.error("Reauthentication failed.")
            return False

    def get_client(self):
        return self.pm_client if self.access_token else None
