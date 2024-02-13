import requests
import hashlib
import os
import logging

# Configure logging with a custom log format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# URLs of the CSV files
csv_files = {
    "security_master.csv": "https://developer.paytmmoney.com/data/v1/scrips/security_master.csv",
    "nse_security_master.csv": "https://developer.paytmmoney.com/data/v1/scrips/nse_security_master.csv",
    "bse_security_master.csv": "https://developer.paytmmoney.com/data/v1/scrips/bse_security_master.csv",
    "option_security_master.csv": "https://developer.paytmmoney.com/data/v1/scrips/option_security_master.csv",
    "future_security_master.csv": "https://developer.paytmmoney.com/data/v1/scrips/future_security_master.csv",
    "index_security_master.csv": "https://developer.paytmmoney.com/data/v1/scrips/index_security_master.csv",
    "equity_security_master.csv": "https://developer.paytmmoney.com/data/v1/scrips/equity_security_master.csv",
    "etf_security_master.csv": "https://developer.paytmmoney.com/data/v1/scrips/etf_security_master.csv"
}

# Define the folder name
folder_name = "security_master"

# Create the folder if it doesn't exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Function to calculate a file's MD5 hash
def md5_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function to download a file
def download_file(url, local_path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(local_path, 'wb') as f:
            f.write(r.content)
        logging.info(f"Downloaded new file: {local_path}")
    else:
        logging.error(f"HTTP error occurred: {r.status_code} Client Error: Not Found for url: {url}")

# Check each file
for file_name, url in csv_files.items():
    local_folder_path = os.path.join(folder_name, file_name)
    local_file_path = os.path.join('D:/Trading_System/data_handler/', local_folder_path)

    # If the file exists locally, compare the hashes
    if os.path.exists(local_file_path):
        response = requests.get(url)
        if response.status_code == 200:
            remote_hash = hashlib.md5(response.content).hexdigest()
            local_hash = md5_hash(local_file_path)

            if remote_hash != local_hash:
                logging.info(f"Hash changed for {file_name}, downloading new version...")
                download_file(url, local_file_path)
            else:
                logging.info(f"No changes detected for {file_name}, skipping download.")
        else:
            logging.error(f"Failed to retrieve remote file for hash comparison: {file_name}")
    else:
        # If the file doesn't exist locally, download it
        logging.info(f"{file_name} does not exist locally, downloading...")
        download_file(url, local_file_path)
