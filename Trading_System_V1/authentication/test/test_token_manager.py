import unittest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime, timedelta
from pathlib import Path
from token_manager import TokenManager

class TestTokenManager(unittest.TestCase):

    def setUp(self):
        self.token_manager = TokenManager()

    @patch('token_manager.open', new_callable=unittest.mock.mock_open, read_data=json.dumps({
        'access_token': 'test_access',
        'public_access_token': 'test_public_access',
        'read_access_token': 'test_read_access',
        'expiry': (datetime.now() + timedelta(hours=1)).isoformat()
    }))
    def test_load_tokens_valid(self, mock_file):
        token_info = self.token_manager.load_tokens()
        self.assertIsNotNone(token_info)
        self.assertIn('access_token', token_info)

    @patch('token_manager.open', new_callable=unittest.mock.mock_open, read_data=json.dumps({
        'access_token': 'test_access',
        'public_access_token': 'test_public_access',
        'read_access_token': 'test_read_access',
        'expiry': (datetime.now() - timedelta(hours=1)).isoformat()
    }))
    def test_load_tokens_expired(self, mock_file):
        token_info = self.token_manager.load_tokens()
        self.assertIsNone(token_info['access_token'])

    @patch('token_manager.open', unittest.mock.mock_open())
    @patch('token_manager.json.dump')
    def test_save_tokens(self, mock_json_dump, mock_file_open):
        self.token_manager.save_tokens('new_access', 'new_public_access', 'new_read_access')
        mock_file_open.assert_called_once_with(Path(__file__).resolve().parents[1] / 'token_info.json', 'w')
        mock_json_dump.assert_called_once()

    @patch('token_manager.open', new_callable=unittest.mock.mock_open, read_data='{}')
    def test_load_tokens_no_file(self, mock_file):
        token_info = self.token_manager.load_tokens()
        self.assertIsNone(token_info['access_token'])

    def test_create_default_token_info(self):
        default_token_info = self.token_manager.create_default_token_info()
        self.assertIsNone(default_token_info['access_token'])

if __name__ == '__main__':
    unittest.main()
