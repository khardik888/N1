import os
import json
import logging
import sys

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from authentication.config import API_KEY, API_SECRET, REQUEST_TOKEN
    from pyPMClient_master.pmClient import PMClient
except ImportError as e:
    logging.error(f"Import error: {e}")
    sys.exit(1)

def load_access_tokens():
    try:
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'authentication', 'access_tokens.json')
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Failed to load access tokens: {e}")
        sys.exit(1)

try:
    pm = PMClient(api_key=API_KEY, api_secret=API_SECRET)
    access_tokens = load_access_tokens()
    pm.set_access_token(access_tokens['access_token'])
    pm.set_public_access_token(access_tokens.get('public_access_token'))
    pm.set_read_access_token(access_tokens.get('read_access_token'))
    user_details = pm.get_user_details()
    print("User Details:", user_details)
except Exception as e:
    logging.error(f"Error occurred: {e}")
