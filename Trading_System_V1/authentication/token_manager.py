import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

class TokenManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.token_file = Path(__file__).resolve().parents[1] / 'token_info.json'
        self.token_info = self.load_tokens()

    def load_tokens(self):
        if self.token_file.exists():
            with open(self.token_file, 'r') as file:
                token_info = json.load(file)
                expiry_time = datetime.fromisoformat(token_info['expiry'])
                if datetime.now() < expiry_time:
                    self.logger.info("Using saved tokens.")
                    return token_info
                else:
                    self.logger.warning("Tokens expired.")
                    return self.create_default_token_info()
        else:
            self.logger.warning("Token file does not exist. Creating default tokens.")
            return self.create_default_token_info()

    def save_tokens(self, access_token, public_access_token, read_access_token):
        expiry_time = datetime.now() + timedelta(hours=24)  # Token expires in 24 hours
        token_info = {
            'access_token': access_token,
            'public_access_token': public_access_token,
            'read_access_token': read_access_token,
            'expiry': expiry_time.isoformat()
        }
        with open(self.token_file, 'w') as file:
            json.dump(token_info, file)
            self.logger.info("Tokens saved successfully.")
            self.token_info = token_info  # Update token_info

    def get_tokens(self):
        return self.token_info

    def create_default_token_info(self):
        """Create default token info structure."""
        return {
            'access_token': None,
            'public_access_token': None,
            'read_access_token': None,
            'expiry': None
        }
