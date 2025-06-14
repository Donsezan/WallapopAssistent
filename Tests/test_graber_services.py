import unittest
from unittest.mock import patch, MagicMock
import requests

# Adjust import path based on your project structure
import sys
import os
# Add the parent directory of 'Services' to the Python path
# This assumes 'Tests' and 'Services' are sibling directories or 'Services' is discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Services.GraberServices import GraberServices
from Services.GraberServices import GraberServices, APIConnectionError
# Constants is not directly used by tests after refactoring, but GraberServices init might use it.
# We assume GraberServices can be initialized without mocking Constants for now.

class TestGraberServices(unittest.TestCase):

    def setUp(self):
        self.graber_service = GraberServices()
        # self.graber_service.searchPath is not relevant for new tests

    def _create_mock_response(self, status_code, json_data, headers=None):
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = status_code
        mock_response.json.return_value = json_data
        mock_response.headers = headers if headers is not None else {}

        if status_code >= 400:
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
                f"{status_code} Error", response=mock_response
            )
        else:
            mock_response.raise_for_status.return_value = None
        return mock_response

    @patch('requests.get')
    def test_get_all_results_successful_pagination(self, mock_requests_get):
        # Expected X-Deviceid from the service instance
        expected_device_id = self.graber_service.device_id
        expected_headers = self.graber_service.headers # This includes the X-Deviceid

        # Setup mock responses for pagination
        mock_response_page1 = self._create_mock_response(
            status_code=200,
            json_data={'search_objects': [{'title': 'Product 1'}, {'title': 'Product 2'}],
                         'meta': {'next_page': 'token123'}},
            headers={'X-Wallapop-Search-Id': 'searchid789'}
        )
        mock_response_page2 = self._create_mock_response(
            status_code=200,
            json_data={'search_objects': [{'title': 'Product 3'}],
                         'meta': {'next_page': 'token456'}},
            headers={} # Search ID not typically in subsequent page headers from API directly
        )
        mock_response_page3 = self._create_mock_response(
            status_code=200,
            json_data={'search_objects': [{'title': 'Product 4'}],
                         'meta': {'next_page': None}},
            headers={}
        )

        mock_requests_get.side_effect = [
            mock_response_page1,
            mock_response_page2,
            mock_response_page3
        ]

        results = self.graber_service.get_all_results_for_keywords(keywords="test")

        self.assertEqual(len(results), 4)
        self.assertEqual(results[0]['title'], 'Product 1')
        self.assertEqual(results[1]['title'], 'Product 2')
        self.assertEqual(results[2]['title'], 'Product 3')
        self.assertEqual(results[3]['title'], 'Product 4')

        self.assertEqual(mock_requests_get.call_count, 3)

        # Call 1 assertions (initial search)
        call1_args, call1_kwargs = mock_requests_get.call_args_list[0]
        self.assertEqual(call1_args[0], "https://api.wallapop.com/api/v3/search")
        self.assertIn('keywords', call1_kwargs['params'])
        self.assertEqual(call1_kwargs['params']['keywords'], 'test')
        self.assertEqual(call1_kwargs['params']['source'], 'search_box')
        # Check important headers, including the dynamic X-Deviceid
        for key, value in expected_headers.items():
            self.assertEqual(call1_kwargs['headers'][key], value)


        # Call 2 assertions (next page 1)
        call2_args, call2_kwargs = mock_requests_get.call_args_list[1]
        expected_url_page2 = f"https://api.wallapop.com/api/v3/search?next_page=token123&source=deep_link&search_id=searchid789"
        self.assertEqual(call2_args[0], expected_url_page2)
        # Subsequent calls might not pass all params, only URL matters mostly
        self.assertEqual(call2_kwargs['headers']['X-Deviceid'], expected_device_id)


        # Call 3 assertions (next page 2)
        call3_args, call3_kwargs = mock_requests_get.call_args_list[2]
        expected_url_page3 = f"https://api.wallapop.com/api/v3/search?next_page=token456&source=deep_link&search_id=searchid789"
        self.assertEqual(call3_args[0], expected_url_page3)
        self.assertEqual(call3_kwargs['headers']['X-Deviceid'], expected_device_id)

    @patch('requests.get')
    def test_get_all_results_with_target_list_filtering(self, mock_requests_get):
        mock_response_page1 = self._create_mock_response(
            status_code=200,
            json_data={'search_objects': [{'title': 'Include This Product 1'}, {'title': 'Exclude This'}],
                         'meta': {'next_page': 'token123'}},
            headers={'X-Wallapop-Search-Id': 'searchid789'}
        )
        mock_response_page2 = self._create_mock_response(
            status_code=200,
            json_data={'search_objects': [{'title': 'Include This Product 3'}],
                         'meta': {'next_page': None}}, # No more pages
            headers={}
        )
        mock_requests_get.side_effect = [mock_response_page1, mock_response_page2]

        target_list = ['Include This'] # Note: ParseResults does case-insensitive partial match
        results = self.graber_service.get_all_results_for_keywords(
            keywords="test",
            target_list=target_list
        )

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['title'], 'Include This Product 1')
        self.assertEqual(results[1]['title'], 'Include This Product 3')
        # Ensure ParseResults was called with the target_list
        # This requires inspecting calls to ParseResults if it were mocked,
        # or relying on the output like above.

    @patch('requests.get')
    def test_get_all_results_no_results_found(self, mock_requests_get):
        mock_response_empty = self._create_mock_response(
            status_code=200,
            json_data={'search_objects': [], 'meta': {'next_page': None}},
            headers={'X-Wallapop-Search-Id': 'searchid789'}
        )
        mock_requests_get.return_value = mock_response_empty # Only one call expected

        results = self.graber_service.get_all_results_for_keywords(keywords="test_no_results")

        self.assertEqual(len(results), 0)
        self.assertEqual(mock_requests_get.call_count, 1)
        call_args, call_kwargs = mock_requests_get.call_args_list[0]
        self.assertEqual(call_kwargs['params']['keywords'], 'test_no_results')

    @patch('requests.get')
    def test_get_all_results_with_max_results(self, mock_requests_get):
        mock_response_page1 = self._create_mock_response(
            status_code=200,
            json_data={'search_objects': [{'title': 'Product 1'}, {'title': 'Product 2'}],
                         'meta': {'next_page': 'token123'}},
            headers={'X-Wallapop-Search-Id': 'searchid789'}
        )
        # This response should not be fetched if max_results is working
        mock_response_page2 = self._create_mock_response(
            status_code=200,
            json_data={'search_objects': [{'title': 'Product 3'}],
                         'meta': {'next_page': None}},
            headers={}
        )
        mock_requests_get.side_effect = [mock_response_page1, mock_response_page2]

        results = self.graber_service.get_all_results_for_keywords(keywords="test_max", max_results=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Product 1')
        # Assert that requests.get was only called once, for the first page
        self.assertEqual(mock_requests_get.call_count, 1)

        # Test max_results that spans across current page but not to next
        mock_requests_get.reset_mock() # Reset call count for next scenario
        mock_requests_get.side_effect = [mock_response_page1, mock_response_page2] # Re-assign side_effect
        results_max2 = self.graber_service.get_all_results_for_keywords(keywords="test_max_2", max_results=2)
        self.assertEqual(len(results_max2), 2)
        self.assertEqual(results_max2[0]['title'], 'Product 1')
        self.assertEqual(results_max2[1]['title'], 'Product 2')
        self.assertEqual(mock_requests_get.call_count, 1) # Still only one call needed

    @patch('requests.get')
    def test_api_error_on_initial_search(self, mock_requests_get):
        # Test ConnectionError
        mock_requests_get.side_effect = requests.exceptions.ConnectionError("Initial connection error")

        # The method should catch APIConnectionError and print a message.
        # For now, we expect an empty list as per current error handling in get_all_results_for_keywords
        # (It prints and returns what it has, which is nothing if initial search fails)
        with patch('builtins.print') as mock_print: # Mock print to check error messages
            results = self.graber_service.get_all_results_for_keywords(keywords="test_fail")
            self.assertEqual(results, [])
            mock_print.assert_any_call("An API connection error occurred: API connection error: Initial connection error")

        # Test HTTPError (e.g., 500)
        mock_requests_get.reset_mock()
        mock_requests_get.side_effect = None # Clear previous side_effect
        mock_requests_get.return_value = self._create_mock_response(status_code=500, json_data={}, headers={})

        with patch('builtins.print') as mock_print:
            results = self.graber_service.get_all_results_for_keywords(keywords="test_http_fail")
            self.assertEqual(results, [])
            mock_print.assert_any_call("An API connection error occurred: API request failed with status 500: 500 Error")

    @patch('requests.get')
    def test_api_error_during_pagination(self, mock_requests_get):
        mock_response_page1 = self._create_mock_response(
            status_code=200,
            json_data={'search_objects': [{'title': 'Product 1'}],
                         'meta': {'next_page': 'token123'}},
            headers={'X-Wallapop-Search-Id': 'searchid789'}
        )
        # Second call will raise an error
        mock_requests_get.side_effect = [
            mock_response_page1,
            requests.exceptions.ConnectionError("Paginated connection error")
        ]

        with patch('builtins.print') as mock_print:
            results = self.graber_service.get_all_results_for_keywords(keywords="test_pagination_fail")
            # Should return results obtained before the error
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]['title'], 'Product 1')
            mock_print.assert_any_call("Fetching next page with token: token123")
            mock_print.assert_any_call("An API connection error occurred: API connection error: Paginated connection error")

        # Test HTTP Error during pagination
        mock_requests_get.reset_mock()
        mock_response_page1_http = self._create_mock_response( # New instance for clarity
            status_code=200,
            json_data={'search_objects': [{'title': 'Product A'}],
                         'meta': {'next_page': 'tokenABC'}},
            headers={'X-Wallapop-Search-Id': 'searchXYZ'}
        )
        mock_response_page2_error = self._create_mock_response(status_code=503, json_data={}, headers={})

        mock_requests_get.side_effect = [mock_response_page1_http, mock_response_page2_error]

        with patch('builtins.print') as mock_print:
            results = self.graber_service.get_all_results_for_keywords(keywords="test_pagination_http_fail")
            self.assertEqual(len(results), 1) # Results from first page
            self.assertEqual(results[0]['title'], 'Product A')
            self.assertEqual(self.graber_service.search_id, "searchXYZ") # Check search_id was set
            mock_print.assert_any_call("Fetching next page with token: tokenABC")
            mock_print.assert_any_call("An API connection error occurred: API request failed with status 503: 503 Error")


if __name__ == '__main__':
    unittest.main(verbosity=2)
