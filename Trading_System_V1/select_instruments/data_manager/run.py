import asyncio
import os
import json
from downloader import download_csv_files, setup_logging as downloader_setup_logging
from hash_checker import is_file_changed, setup_logging as hash_checker_setup_logging
from storage_manager import replace_file_with_backup, setup_logging as storage_manager_setup_logging

# Define paths
CURRENT_MASTER_DIR = "security_master/current_master"
ARCHIVE_MASTER_DIR = "security_master/archive_master"
URLS_JSON = "urls.json"

# Setup logging
downloader_setup_logging()
hash_checker_setup_logging()
storage_manager_setup_logging()

def load_urls(file_path=URLS_JSON):
    with open(file_path, 'r') as file:
        return json.load(file)

async def update_files(urls, current_dir, archive_dir):
    # Ensure directory structure
    if not os.path.exists(current_dir):
        os.makedirs(current_dir, exist_ok=True)
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir, exist_ok=True)

    # Download and process files
    for name, url in urls.items():
        current_path = os.path.join(current_dir, name)
        temp_path = current_path + '.tmp'

        # Download to a temporary file
        await download_csv_files({name: url}, os.path.dirname(temp_path))

        # If the file is new or changed, replace and backup
        if not os.path.exists(current_path) or is_file_changed(current_path, temp_path):
            replace_file_with_backup(current_path, temp_path, archive_dir)
        else:
            os.remove(temp_path)

async def main():
    urls = load_urls()
    await update_files(urls, CURRENT_MASTER_DIR, ARCHIVE_MASTER_DIR)

if __name__ == "__main__":
    asyncio.run(main())
