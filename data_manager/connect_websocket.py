import json
import logging
import os
import csv
from datetime import datetime
from pyPMClient_master.pmClient.WebSocketClient import WebSocketClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the path to the script directory and customer preferences JSON file
current_script_dir = os.path.dirname(__file__)  # Gets the directory where the script is located
preferences_path = os.path.join(current_script_dir, 'customer_preferences.json')

# Define the path to the access_tokens.json file dynamically
parent_dir = os.path.dirname(current_script_dir)  # Navigate up to the parent directory
access_tokens_path = os.path.join(parent_dir, 'authentication', 'access_tokens.json')  # Path to access_tokens.json

# Load access tokens from a JSON file
try:
    with open(access_tokens_path, 'r') as file:
        tokens = json.load(file)
    public_access_token = tokens['public_access_token']
except Exception as e:
    logging.error(f"Failed to load access tokens: {e}")
    raise

# Initialize WebSocketClient with the public access token
webSocketClient = WebSocketClient(public_access_token)

# Load customer preferences from a JSON file
def load_customer_preferences(file_path):
    """Load customer preferences from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Failed to load customer preferences: {e}")
        raise

customerPreferences = load_customer_preferences(preferences_path)

def ensure_directory_exists(directory):
    """Ensures the specified directory exists, creates it if it does not."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_to_csv(data_for_csv, filename, headers=None):
    """General function to save data to CSV, ensuring headers are written for new files."""
    with open(filename, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers if headers else data_for_csv.keys())
        if file.tell() == 0:  # If file is empty, write the header
            writer.writeheader()
        writer.writerow(data_for_csv)

def save_data_to_csv(data, base_directory, security_id, received_timestamp):
    """Saves data into specific CSV files within instrument-specific folders."""
    instrument_dir = os.path.join(base_directory, security_id)
    ensure_directory_exists(instrument_dir)

    date_str = datetime.now().strftime('%Y-%m-%d')
    market_data_filename = os.path.join(instrument_dir, f"market_data_{security_id}_{date_str}.csv")
    market_depth_filename = os.path.join(instrument_dir, f"market_depth_{security_id}_{date_str}.csv")

    # Modify here for market data excluding depth_packet with timestamp as first column
    if 'depth_packet' in data:
        market_data = {'received_timestamp': received_timestamp, **{key: value for key, value in data.items() if key != 'depth_packet'}}
    else:
        market_data = {'received_timestamp': received_timestamp, **data}
    save_to_csv(market_data, market_data_filename, headers=['received_timestamp'] + [key if key != 'scrip_id' else 'security_id' for key in data.keys() if key != 'depth_packet'])

    # For market depth, process each depth_packet entry individually
    if 'depth_packet' in data:
        for depth_key, depth_info in data['depth_packet'].items():
            depth_data = {'received_timestamp': received_timestamp, 'security_id': security_id, **depth_info}
            save_to_csv(depth_data, market_depth_filename, headers=['received_timestamp', 'security_id'] + list(depth_info.keys()))

def process_message_item(data):
    received_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    security_id = str(data.get('security_id', ''))

    # Define the base directory to save CSV files (same directory as the code)
    base_directory = os.path.join(current_script_dir, 'instrument_data')

    save_data_to_csv(data, base_directory, security_id, received_timestamp)

def on_message(arr):
    logging.info(f"Message received: {arr}")
    if isinstance(arr, str):
        data = json.loads(arr)
    else:
        data = arr  # Assuming arr is already a dict or list

    if isinstance(data, list):
        for item in data:
            process_message_item(item)
    elif isinstance(data, dict):
        process_message_item(data)
    else:
        logging.error("Received message is neither a list nor a dict.")

def on_open():
    logging.info("WebSocket connection opened.")
    webSocketClient.subscribe(customerPreferences)

def on_close(code, reason):
    logging.info(f"WebSocket connection closed. Code: {code}, Reason: {reason}")

def on_error(error_message):
    logging.error(f"WebSocket error: {error_message}")

# Setting event listeners
webSocketClient.set_on_open_listener(on_open)
webSocketClient.set_on_close_listener(on_close)
webSocketClient.set_on_error_listener(on_error)
webSocketClient.set_on_message_listener(on_message)

# Reconnect configuration
webSocketClient.set_reconnect_config(True, 5)

# Connect to the WebSocket server
webSocketClient.connect()
