import aiohttp
import asyncio
import os
import json
import logging
from log_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def load_urls(file_path='urls.json'):
    """Load URLs from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Failed to load URLs from {file_path}: {e}")
        return {}

async def download_file(session, url, destination):
    """Download a file from a URL to a destination."""
    async with session.get(url) as response:
        if response.status == 200:
            temp_file = destination + '.tmp'
            with open(temp_file, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            return temp_file
        else:
            logger.error(f"Failed to download {url}: {response.status}")
            return None

async def download_csv_files(urls, destination_folder):
    """Download multiple CSV files from given URLs to a destination folder."""
    os.makedirs(destination_folder, exist_ok=True)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for name, url in urls.items():
            current_path = os.path.join(destination_folder, name)
            task = asyncio.ensure_future(download_file(session, url, current_path))
            tasks.append(task)
        await asyncio.gather(*tasks)

async def main():
    urls = load_urls('urls.json')  # Load URLs from urls.json
    destination_folder = "security_master/current_master"
    await download_csv_files(urls, destination_folder)

if __name__ == "__main__":
    asyncio.run(main())
