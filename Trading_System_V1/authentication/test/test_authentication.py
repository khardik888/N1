import unittest
from unittest.mock import patch
from authentication.authentication import Auth


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.auth = Auth()

    def test_generate_auth_url(self):
        # Test if the auth URL is correctly generated
        auth_url = self.auth.generate_auth_url()
        self.assertIn('https://login.paytmmoney.com/merchant-login', auth_url)

    @patch('authentication.requests.get')
    def test_validate_access_token_success(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Test validate_access_token method
        result = self.auth.validate_access_token()
        self.assertTrue(result)

    # Add more tests for other methods and scenarios

if __name__ == '__main__':
    unittest.main()
