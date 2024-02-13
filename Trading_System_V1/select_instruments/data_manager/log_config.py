# log_config.py
import logging.config
import json
import os

def setup_logging(default_path='logging_config.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration"""
    path = os.getenv(env_key, default_path)
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
