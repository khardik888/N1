import unittest
from unittest.mock import patch, MagicMock
from authentication import Auth

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.auth = Auth()

    def test_generate_auth_url(self):
        auth_url = self.auth.generate_auth_url()
        self.assertIn('https://login.paytmmoney.com/merchant-login', auth_url)

    @patch('authentication.PMClient')
    def test_exchange_request_token_success(self, mock_pm_client):
        mock_pm_client.generate_session.return_value = {'access_token': 'test_token'}
        success = self.auth.exchange_request_token('dummy_request_token')
        self.assertTrue(success)
        self.assertEqual(self.auth.access_token, 'test_token')

    @patch('authentication.PMClient')
    def test_exchange_request_token_failure(self, mock_pm_client):
        mock_pm_client.generate_session.return_value = {}
        success = self.auth.exchange_request_token('dummy_request_token')
        self.assertFalse(success)
        self.assertIsNone(self.auth.access_token)

    @patch('authentication.requests.get')
    def test_validate_access_token_success(self, mock_get):
        mock_get.return_value.status_code = 200
        result = self.auth.validate_access_token()
        self.assertTrue(result)

    @patch('authentication.requests.get')
    def test_validate_access_token_failure(self, mock_get):
        mock_get.return_value.status_code = 401
        result = self.auth.validate_access_token()
        self.assertFalse(result)

    @patch('builtins.input', return_value='dummy_request_token')
    @patch('authentication.Auth.exchange_request_token', return_value=True)
    def test_reauthenticate_success(self, mock_exchange_request_token, mock_input):
        success = self.auth.reauthenticate()
        self.assertTrue(success)

    @patch('builtins.input', return_value='dummy_request_token')
    @patch('authentication.Auth.exchange_request_token', return_value=False)
    def test_reauthenticate_failure(self, mock_exchange_request_token, mock_input):
        success = self.auth.reauthenticate()
        self.assertFalse(success)

if __name__ == '__main__':
    unittest.main()
