import logging
import requests
from authentication.token_manager import TokenManager
from execution.pmClient.constants import Constants

class UserDetailsService:
    def __init__(self, token_manager: TokenManager):
        self.logger = logging.getLogger(__name__)
        self.token_manager = token_manager
        self.constants = Constants()

    def fetch_user_details(self, access_token):
        if not access_token:
            self.logger.error("Access token is not available.")
            return None

        user_details_endpoint = self.constants._service_config['routes']['user_details'][0]
        host = self.constants._service_config['host']
        url = f"{host}{user_details_endpoint}"

        headers = {
            "x-jwt-token": access_token,
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            self.logger.error(f"An unexpected error occurred: {err}")

        return None
