import requests
import logging
from execution.pmClient.constants import Constants
from authentication.token_manager import TokenManager

class FundDetailsService:
    def __init__(self, token_manager: TokenManager):
        self.logger = logging.getLogger(__name__)
        self.token_manager = token_manager
        self.constants = Constants()

    def fetch_fund_details(self, access_token):  # Updated to accept access_token
        if not access_token:
            self.logger.error("Access token is not available.")
            return None

        fund_details_route_template = self.constants._service_config['routes']['funds_summary'][0]
        fund_details_route = fund_details_route_template.replace("{config}", "true")

        host = self.constants._service_config['host']
        url = f"{host}{fund_details_route}"

        headers = {
            "x-jwt-token": access_token,
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            self.logger.info("Fund details retrieved successfully.")
            return response.json()
        except requests.HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err} - {response.text}")
        except Exception as err:
            self.logger.error(f"An unexpected error occurred: {err}")

        return None
