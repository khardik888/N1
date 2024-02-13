import csv
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

# Organize option chain data into a list of dictionaries
formatted_data = []
for option_contract in option_chain_data['data']['results']:
    formatted_contract = {
        'pml_id': option_contract['pml_id'],
        'exchange': option_contract['exchange'],
        'underlying_scrip_code': option_contract['underlaying_scrip_code'],
        'segment': option_contract['segment'],
        'security_id': option_contract['security_id'],
        'pml_symbol': option_contract['pml_symbol'],
        'vega': option_contract['vega'],
        'fresh_pos': option_contract['fresh_pos'],
        'iv': option_contract['iv'],
        'square_off_pos': option_contract['square_off_pos'],
        'desc': option_contract['desc'],
        'theta': option_contract['theta'],
        'gamma': option_contract['gamma'],
        'spot_price': option_contract['spot_price'],
        'delta': option_contract['delta'],
        'price': option_contract['price'],
        'stk_price': option_contract['stk_price'],
        'net_chg': option_contract['net_chg'],
        'oi': option_contract['oi'],
        'oi_per_chg': option_contract['oi_per_chg'],
        'oi_net_chg': option_contract['oi_net_chg'],
        'per_chg': option_contract['per_chg'],
        'traded_vol': option_contract['traded_vol'],
        'symbol': option_contract['symbol'],
        'expiry_date': option_contract['expiry_date'],
        'option_type': option_contract['option_type'],
        'instrument': option_contract['instrument'],
        'name': option_contract['name'],
        'tick_size': option_contract['tick_size'],
        'lot_size': option_contract['lot_size'],
        'exch_feed_time': option_contract['exch_feed_time']
    }
    formatted_data.append(formatted_contract)

# Save the formatted data to a CSV file
output_file_path = os.path.join(current_directory, 'formatted_option_chain_data.csv')
with open(output_file_path, 'w', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=formatted_data[0].keys())
    writer.writeheader()
    writer.writerows(formatted_data)

print("Option chain data saved successfully to:", output_file_path)
