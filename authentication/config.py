import json
import os

API_KEY = 'e1fb7cbc77ce42b4880357ae7d3458d8'
API_SECRET = '1fd16295d8684313a806825f62d1cb60'
USERNAME = 'khardik888@gmail.com'
PASSWORD = 'cahd8506@'


def load_request_token():
    # Construct the absolute path to the token_info.json file.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    token_file_path = os.path.join(dir_path, 'token_info.json')

    with open(token_file_path, 'r') as f:
        token_info = json.load(f)
    return token_info['request_token']


REQUEST_TOKEN = load_request_token()
