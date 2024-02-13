# hash_checker.py
import hashlib
import logging
from log_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def file_hash(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def is_file_changed(old_file, new_file):
    old_hash = file_hash(old_file)
    new_hash = file_hash(new_file)
    return old_hash != new_hash
