import logging
import os
import sys

# Assuming your pmClient.py is one directory up from your current script.
sys.path.append('../')
from pmClient import PMClient

# Use environment variables for sensitive data
API_KEY = os.getenv('PM_API_KEY')
API_SECRET = os.getenv('PM_API_SECRET')
REQUEST_TOKEN = os.getenv('PM_REQUEST_TOKEN')
ACCESS_TOKEN = os.getenv('PM_ACCESS_TOKEN')
PUBLIC_ACCESS_TOKEN = os.getenv('PM_PUBLIC_ACCESS_TOKEN')
READ_ACCESS_TOKEN = os.getenv('PM_READ_ACCESS_TOKEN')

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize PMClient with API key and secret
pm = PMClient(api_key=API_KEY, api_secret=API_SECRET)

try:
    # Generate session
    pm.generate_session(REQUEST_TOKEN)

    # Set access tokens
    pm.set_access_token(ACCESS_TOKEN)
    pm.set_public_access_token(PUBLIC_ACCESS_TOKEN)
    pm.set_read_access_token(READ_ACCESS_TOKEN)

    # Attempt to get user details
    user_details = pm.get_user_details()
    logging.info("User details retrieved successfully: %s", user_details)
except Exception as e:
    # Log with more context
    logging.error("Failed to retrieve user details: %s", e, exc_info=True)
