import unittest
from unittest.mock import patch, MagicMock
import requests

# Adjust import path based on your project structure
import sys
import os
# Add the parent directory of 'Services' to the Python path
# This assumes 'Tests' and 'Services' are sibling directories or 'Services' is discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Services.GraberServices import GraberServices, APIConnectionError # Import APIConnectionError
from constants import Constants # GraberServices uses Constants in __init__

class TestGraberServices(unittest.TestCase):

    def setUp(self):
        # Mock Constants if its values are crucial and not easily available in test environment
        # For now, assume Constants.Direct_search_path is a simple string
        self.graber_service = GraberServices()
        # Replace actual searchPath with a dummy one for tests if it's used by requests.get
        self.graber_service.searchPath = "mock_search_path"


    @patch('requests.get')
    def test_get_response_success(self, mock_requests_get):
        # Configure the mock for a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        expected_json = {"data": "success"}
        mock_response.json.return_value = expected_json
        mock_requests_get.return_value = mock_response

        # Call the method
        result = self.graber_service.GetReposne(request_param={})

        # Assertions
        self.assertEqual(result, expected_json)
        mock_requests_get.assert_called_once_with(
            self.graber_service.searchPath,
            headers=self.graber_service.headers,
            params={}
        )
        mock_response.raise_for_status.assert_called_once()

    @patch('requests.get')
    def test_get_response_connection_error(self, mock_requests_get):
        # Configure the mock to raise ConnectionError
        mock_requests_get.side_effect = requests.exceptions.ConnectionError("Test connection error")

        # Assert that APIConnectionError is raised (as GraberServices wraps ConnectionError)
        with self.assertRaises(APIConnectionError) as context:
            self.graber_service.GetReposne(request_param={})

        self.assertTrue("API connection error: Test connection error" in str(context.exception))
        mock_requests_get.assert_called_once_with(
            self.graber_service.searchPath,
            headers=self.graber_service.headers,
            params={}
        )

    @patch('requests.get')
    def test_get_response_http_error(self, mock_requests_get):
        # Configure the mock for an HTTP error
        mock_response = MagicMock()
        mock_response.status_code = 500
        # Configure raise_for_status to raise an HTTPError
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Server Error", response=mock_response
        )
        mock_requests_get.return_value = mock_response

        # Assert that APIConnectionError is raised
        with self.assertRaises(APIConnectionError) as context:
            self.graber_service.GetReposne(request_param={})

        self.assertTrue("Server Error" in str(context.exception)) # Check original error message
        self.assertTrue("API request failed with status 500" in str(context.exception))
        mock_requests_get.assert_called_once_with(
            self.graber_service.searchPath,
            headers=self.graber_service.headers,
            params={}
        )
        mock_response.raise_for_status.assert_called_once()

if __name__ == '__main__':
    unittest.main()
