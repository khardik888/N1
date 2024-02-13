import json
import os
from pyPMClient_master.pmClient.pmClient import PMClient
from pyPMClient_master.pmClient.constants import Constants
from authentication.config import API_KEY, API_SECRET

# Path setup for access tokens
current_directory = os.path.dirname(os.path.abspath(__file__))
tokens_file_path = os.path.join(current_directory, '..', 'authentication', 'access_tokens.json')

# Read the JWT tokens from access_tokens.json
with open(tokens_file_path, 'r') as token_file:
    tokens = json.load(token_file)

# Initialize constants and PMClient
constants = Constants()
client = PMClient(api_key=API_KEY, api_secret=API_SECRET)

# Set the JWT tokens in the PMClient instance
client.access_token = tokens['access_token']
client.public_access_token = tokens.get('public_access_token')
client.read_access_token = tokens.get('read_access_token')

# Define the parameters for the option chain request
option_type = 'CALL'  # Example: 'CE' for Call European, change as per your requirement
symbol = 'NIFTY'  # Example: 'XYZ', change to your desired symbol
expiry = '15-02-2024'  # Example: '31-12-2024', change to the desired expiry date in DD-MM-YYYY format

# Fetch the option chain data using the client
option_chain_data = client.get_option_chain(option_type, symbol, expiry)

# Output the option chain data
print(option_chain_data)
