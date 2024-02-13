import json
import os
from pyPMClient_master.pmClient.pmClient import PMClient
from pyPMClient_master.pmClient.constants import Constants
from authentication.config import API_KEY, API_SECRET

# Enums for request construction
from pyPMClient_master.pmClient.enums import Source, TransactionType, ProductType

# Get the current directory and construct the path to the access_tokens.json
current_directory = os.path.dirname(os.path.abspath(__file__))
tokens_file_path = os.path.join(current_directory, '..', 'authentication', 'access_tokens.json')

# Read the JWT tokens from access_tokens.json
with open(tokens_file_path, 'r') as token_file:
    tokens = json.load(token_file)

# Initialize the PMClient with the API key and API secret
client = PMClient(api_key=API_KEY, api_secret=API_SECRET)

# Set the JWT tokens directly in the PMClient instance
client.access_token = tokens['access_token']
# Additional tokens set as per requirement

# Construct a margin_list for the scrips_margin calculation
margin_list = [
    {
        "exchange": "NSE",
        "segment": "D",
        "security_id": "44675",
        "txn_type": "B",
        "quantity": "50",
        "strike_price": "21800",
        "trigger_price": "100",
        "instrument": "OPTIDX"
    }
]

# Calculate the margin requirements using the client
# Specify the source as 'Website' or 'OperatorWorkStation', according to the actual source of the API call
margin_requirements = client.scrips_margin(source=Source.OperatorWorkStation.value, margin_list=margin_list)

# Output the margin requirements
print(margin_requirements)
