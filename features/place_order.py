import json
import os
from pyPMClient_master.pmClient.pmClient import PMClient
from authentication.config import API_KEY, API_SECRET
from pyPMClient_master.pmClient.enums import Source, TransactionType, OrderType, ProductType

current_directory = os.path.dirname(os.path.abspath(__file__))
tokens_file_path = os.path.join(current_directory, '..', 'authentication', 'access_tokens.json')

with open(tokens_file_path, 'r') as token_file:
    tokens = json.load(token_file)

client = PMClient(api_key=API_KEY, api_secret=API_SECRET)
client.access_token = tokens['access_token']

order_response = client.place_order(
    txn_type=TransactionType.Buy.value,
    exchange="NSE",
    segment="D",
    product=ProductType.Intraday.value,
    security_id="43986",
    quantity=50,
    validity="DAY",
    order_type=OrderType.Limit.value,
    price=20,
    source=Source.OperatorWorkStation.value,
    off_mkt_flag=False
)

print(order_response)
