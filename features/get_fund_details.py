import json
import os
from pyPMClient_master.pmClient.pmClient import PMClient
from pyPMClient_master.pmClient.constants import Constants
from authentication.config import API_KEY, API_SECRET

current_directory = os.path.dirname(os.path.abspath(__file__))
tokens_file_path = os.path.join(current_directory, '..', 'authentication', 'access_tokens.json')

with open(tokens_file_path, 'r') as token_file:
    tokens = json.load(token_file)

constants = Constants()

client = PMClient(api_key=API_KEY, api_secret=API_SECRET)
client.access_token = tokens['access_token']
client.public_access_token = tokens.get('public_access_token')
client.read_access_token = tokens.get('read_access_token')

fund_summary_data = client.funds_summary(config=True)
print(fund_summary_data)
