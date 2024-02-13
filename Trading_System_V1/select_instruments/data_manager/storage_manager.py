# storage_manager.py
import os
import shutil
import logging
from log_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def replace_file_with_backup(current_file, new_file, backup_directory):
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory, exist_ok=True)
    if os.path.exists(current_file):
        basename = os.path.basename(current_file)
        backup_file = os.path.join(backup_directory, f"{basename}.{int(time.time())}.bak")
        shutil.move(current_file, backup_file)
        logger.info(f"Backed up old file: {backup_file}")
    shutil.move(new_file, current_file)
    logger.info(f"Updated file: {current_file}")
