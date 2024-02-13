import json
import os
from pyPMClient_master.pmClient.pmClient import PMClient
from pyPMClient_master.pmClient.constants import Constants
from authentication.config import API_KEY, API_SECRET

# Get the current directory and construct the path to the access_tokens.json
current_directory = os.path.dirname(os.path.abspath(__file__))
tokens_file_path = os.path.join(current_directory, '..', 'authentication', 'access_tokens.json')

# Read the JWT tokens from access_tokens.json
with open(tokens_file_path, 'r') as token_file:
    tokens = json.load(token_file)

# Initialize the constants and PMClient with the API key and API secret
constants = Constants()
client = PMClient(api_key=API_KEY, api_secret=API_SECRET)

# Set the JWT tokens directly in the PMClient instance
client.access_token = tokens['access_token']  # The PMClient class should have a property to set this
client.public_access_token = tokens.get('public_access_token')  # if used
client.read_access_token = tokens.get('read_access_token')  # if used

# Fetch the positions data using the client
positions_data = client.position()

# Output the positions data
print(positions_data)
