import requests
import os
import hashlib
import logging
from config import CSV_FILES, CSV_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Directory created: {directory}")
    else:
        logging.info(f"Directory already exists: {directory}")

def md5_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    logging.info(f"Computed MD5 hash for {file_path}")
    return hash_md5.hexdigest()

def download_file(url, local_path):
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=128):
                    f.write(chunk)
            logging.info(f"File downloaded successfully: {local_path}")
        else:
            logging.warning(f"Failed to download file {url}. Status code: {r.status_code}")
    except Exception as e:
        logging.error(f"Error downloading file {url}: {e}")

def update_files():
    ensure_dir(CSV_DIR)
    for name, url in CSV_FILES.items():
        local_path = os.path.join(CSV_DIR, name)
        logging.info(f"Checking file: {name}")
        try:
            if not os.path.exists(local_path) or md5_hash(local_path) != md5_hash(requests.get(url, stream=True).content):
                logging.info(f"Updating file: {name}")
                download_file(url, local_path)
            else:
                logging.info(f"File is up-to-date: {name}")
        except Exception as e:
            logging.error(f"Error updating file {name}: {e}")

if __name__ == "__main__":
    logging.info("Starting file update process.")
    update_files()
    logging.info("File update process completed.")
