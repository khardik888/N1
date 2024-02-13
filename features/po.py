import json
import os
from pyPMClient_master.pmClient.pmClient import PMClient
from pyPMClient_master.pmClient.constants import Constants
from authentication.config import API_KEY, API_SECRET

# Assuming the corrected enum names based on your enums.py and documentation provided
from pyPMClient_master.pmClient.enums import Source, TransactionType, ProductType

# Corrected enum usage according to documentation and your error message
# Please adjust the following line if the SDK provides a direct Exchange enum or similar
# For demonstration, using string literals as per the documentation provided
EXCHANGE_NSE = 'NSE'
EXCHANGE_BSE = 'BSE'

# Read the JWT tokens
current_directory = os.path.dirname(os.path.abspath(__file__))
tokens_file_path = os.path.join(current_directory, '..', 'authentication', 'access_tokens.json')

with open(tokens_file_path, 'r') as token_file:
    tokens = json.load(token_file)

# Initialize the PMClient
client = PMClient(api_key=API_KEY, api_secret=API_SECRET)

# Set the JWT tokens
client.access_token = tokens['access_token']
# Additional tokens can be set here if needed

# Place an order example
order_response = client.place_order(
    txn_type="B",  # Assuming 'Buy' is represented in the TransactionType enum
    exchange="NSE",  # Use the correct way to specify the exchange based on your SDK and documentation
    segment="D",  # Specify the correct segment as per your requirement and SDK documentation
    product="I",  # Adjust based on actual enum names/values
    security_id="43986",  # Example security ID, adjust as necessary
    quantity=50,  # Number of shares to buy
    validity="DAY",  # Order validity
    order_type='LMT',  # Assuming 'Limit' order type, adjust as necessary
    price=20,  # Assuming a limit price of 2500, adjust as necessary
    source="O",  # Source of the order, adjust based on enums.py contents
    off_mkt_flag=False  # Assuming it's a regular market order
)

print(order_response)
