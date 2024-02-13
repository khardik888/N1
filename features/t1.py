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

# Parameters for the order_margin calculation
# Replace these values with the actual ones you wish to use
exchange = "NSE"
segment = "D"
security_id = "44675"  # Example security ID
txn_type = "B"
quantity = 1
price = 21800
product = "C"
trigger_price = 0

# Calculate the order margin using the client
# Specify the source as 'OperatorWorkStation', according to the actual source of the API call
order_margin_requirements = client.order_margin(
    source=Source.OperatorWorkStation.value,
    exchange=exchange,
    segment=segment,
    security_id=security_id,
    txn_type=txn_type,
    quantity=quantity,
    price=price,
    product=product,
    trigger_price=trigger_price
)

# Output the order margin requirements
print(order_margin_requirements)
