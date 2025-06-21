import unittest
from unittest.mock import patch, MagicMock, ANY
import requests # For requests.exceptions
from Services.GraberServices import GraberServices, APIConnectionError
from constants import Constants # For Direct_search_path
import re # For regex matching of device ID

class TestGraberServices(unittest.TestCase):

    def setUp(self):
        self.graber_services = GraberServices()
        # Clear default parameters that might interfere with specific test setups
        self.graber_services.parameters = {}


    # Test for generate_application_device_id (static method)
    def test_generate_application_device_id_format(self):
        # Arrange
        # Act
        device_id = GraberServices.generate_application_device_id()
        # Assert
        self.assertIsNotNone(device_id)
        self.assertIsInstance(device_id, str)
        pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
        self.assertRegex(device_id, pattern)

    # Test for __init__
    def test_init_device_id_and_headers(self):
        # Arrange & Act
        graber_service_instance = GraberServices() # Create a new instance for this test
        # Assert
        self.assertIsNotNone(graber_service_instance.device_id)
        self.assertIn("X-Deviceid", graber_service_instance.headers)
        self.assertEqual(graber_service_instance.headers["X-Deviceid"], graber_service_instance.device_id)
        self.assertIsNone(graber_service_instance.search_id)

    # Tests for _make_api_request
    @patch('requests.get')
    def test_make_api_request_success(self, mock_requests_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "success"}
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        url = "http://fakeapi.com/test"
        params = {"key": "value"}

        # Act
        response = self.graber_services._make_api_request(url, params=params)

        # Assert
        mock_requests_get.assert_called_once_with(url, headers=self.graber_services.headers, params=params)
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(response, mock_response)

    @patch('requests.get')
    def test_make_api_request_http_error(self, mock_requests_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 404
        # Configure the response object for the HTTPError
        http_error = requests.exceptions.HTTPError("404 Client Error")
        http_error.response = mock_response # Attach the response to the error
        mock_response.raise_for_status.side_effect = http_error
        mock_requests_get.return_value = mock_response

        url = "http://fakeapi.com/notfound"

        # Act & Assert
        with self.assertRaises(APIConnectionError) as context:
            self.graber_services._make_api_request(url)
        self.assertIn("API request failed with status 404", str(context.exception))

    @patch('requests.get')
    def test_make_api_request_connection_error(self, mock_requests_get):
        # Arrange
        mock_requests_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        url = "http://fakeapi.com/connect_error"

        # Act & Assert
        with self.assertRaises(APIConnectionError) as context:
            self.graber_services._make_api_request(url)
        self.assertIn("API connection error: Connection failed", str(context.exception))

    # Tests for search_initial
    @patch.object(GraberServices, '_make_api_request')
    def test_search_initial_success(self, mock_make_api_request):
        # Arrange
        mock_api_response = MagicMock()
        mock_api_response.headers = {'X-Wallapop-Search-Id': 'test-search-id'}
        mock_api_response.json.return_value = {
            "data": "some_data",
            "meta": {"next_page": "next_token_123"}
        }
        mock_make_api_request.return_value = mock_api_response

        keywords = "test keyword"
        # Explicitly pass all expected default params if they are not None in the original parameters
        # or ensure they are part of kwargs if they should override
        extra_params = {
            "category_ids": "100",
            "latitude":"10.0",
            "longitude":"20.0",
            "country_code": "ES", # Example of a default from original params
            "order_by": "newest"   # Example of a default
        }

        expected_call_params = {
            'source': 'search_box',
            'keywords': keywords,
            **extra_params
        }
        # Remove keys from expected_call_params if their value is None, as per method logic
        expected_call_params = {k: v for k, v in expected_call_params.items() if v is not None}


        # Act
        json_response, next_page_token = self.graber_services.search_initial(keywords, **extra_params)

        # Assert
        mock_make_api_request.assert_called_once_with(Constants.Direct_search_path, params=ANY)

        called_args, called_kwargs = mock_make_api_request.call_args
        actual_params_in_call = called_kwargs.get('params', {})

        # Check that all expected params are in the actual call params
        for key, value in expected_call_params.items():
            self.assertEqual(actual_params_in_call.get(key), value, f"Mismatch for param key: {key}")

        # Check that no unexpected params (from this test's perspective) were added if they were None
        # This depends on the default self.graber_services.parameters which we cleared in setUp for predictability

        self.assertEqual(self.graber_services.search_id, 'test-search-id')
        self.assertEqual(json_response, {"data": "some_data", "meta": {"next_page": "next_token_123"}})
        self.assertEqual(next_page_token, "next_token_123")


    # Tests for fetch_next_page
    @patch.object(GraberServices, '_make_api_request')
    def test_fetch_next_page_success(self, mock_make_api_request):
        # Arrange
        self.graber_services.search_id = "current-search-id"
        next_page_token_input = "token_abc"

        mock_api_response = MagicMock()
        mock_api_response.json.return_value = {
            "data": "page 2 data",
            "meta": {"next_page": "new_token_xyz"}
        }
        mock_make_api_request.return_value = mock_api_response

        expected_url = f"{Constants.Direct_search_path}?next_page={next_page_token_input}&source=deep_link&search_id={self.graber_services.search_id}"

        # Act
        json_response, new_next_page_token = self.graber_services.fetch_next_page(next_page_token_input)

        # Assert
        mock_make_api_request.assert_called_once_with(expected_url)
        self.assertEqual(json_response, {"data": "page 2 data", "meta": {"next_page": "new_token_xyz"}})
        self.assertEqual(new_next_page_token, "new_token_xyz")

    def test_fetch_next_page_no_search_id(self):
        # Arrange
        self.graber_services.search_id = None
        # Act & Assert
        with self.assertRaisesRegex(ValueError, "search_id is not set. Call search_initial first."):
            self.graber_services.fetch_next_page("some_token")

    def test_fetch_next_page_no_token(self):
        # Arrange
        self.graber_services.search_id = "some-search-id"
        # Act & Assert
        with self.assertRaisesRegex(ValueError, "next_page_token is not set. Call search_initial first."):
            self.graber_services.fetch_next_page(None)


    # Tests for ParseResults
    def test_parse_results_with_data_and_target_list(self):
        # Arrange
        json_response = {
            "data": {
                "section": {
                    "payload": {
                        "items": [
                            {"title": "Old Laptop", "id": 1},
                            {"title": "New Amazing Laptop", "id": 2},
                            {"title": "Desktop PC", "id": 3}
                        ]
                    }
                }
            }
        }
        target_list = ["laptop"]
        # Act
        with patch('builtins.print') as mock_print:
            results = self.graber_services.ParseResults(json_response, target_list)
        # Assert
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], 1)
        self.assertEqual(results[1]["id"], 2)

    def test_parse_results_with_data_no_target_list(self):
        # Arrange
        items_payload = [
            {"title": "Old Laptop", "id": 1},
            {"title": "New Amazing Laptop", "id": 2}
        ]
        json_response = {"data": {"section": {"payload": {"items": items_payload}}}}
        # Act
        with patch('builtins.print') as mock_print:
            results = self.graber_services.ParseResults(json_response, None)
        # Assert
        self.assertEqual(len(results), 2)
        self.assertEqual(results, items_payload)

    def test_parse_results_no_data_key(self):
        # Arrange
        json_response = {"other_key": "value"}
        # Act
        with patch('builtins.print') as mock_print:
            results = self.graber_services.ParseResults(json_response, ["laptop"])
            mock_print.assert_any_call("No search objects found in the response.")
        # Assert
        self.assertEqual(results, [])

    def test_parse_results_no_items_key_robust(self):
        # To test robustness for missing 'items', we'd ideally want the code to use .get()
        # Since it uses direct access `json_response['data']['section']['payload']['items']`,
        # a KeyError is expected if any part of that path is missing.
        # This test verifies the behavior with a missing 'items' key.
        json_response_missing_items = {
            "data": {
                "section": {
                    "payload": {
                        # "items" key is missing here
                        "some_other_info": "details"
                    }
                }
            }
        }
        with patch('builtins.print') as mock_print: # To catch any prints
            with self.assertRaises(KeyError) as context:
                self.graber_services.ParseResults(json_response_missing_items, ["laptop"])
            self.assertTrue('items' in str(context.exception).lower())


    # Tests for get_all_results_for_keywords
    @patch.object(GraberServices, 'search_initial')
    @patch.object(GraberServices, 'fetch_next_page')
    @patch.object(GraberServices, 'ParseResults')
    @patch('helper.Helper.unix_data_is_older_than', return_value=False)
    def test_get_all_results_pagination(self, mock_unix_older, mock_parse_results, mock_fetch_next_page, mock_search_initial):
        # Arrange
        keywords = "test"

        mock_search_initial.return_value = ({"data_initial": "page1"}, "token_page2")
        mock_fetch_next_page.side_effect = [
            ({"data_next": "page2"}, "token_page3"),
            ({"data_final": "page3"}, None)
        ]
        mock_parse_results.side_effect = [
            [{"id": 1, "title": "item1", "modified_at": 100}],
            [{"id": 2, "title": "item2", "modified_at": 200}],
            [{"id": 3, "title": "item3", "modified_at": 300}]
        ]

        # Act
        with patch('builtins.print') as mock_print:
            all_products = self.graber_services.get_all_results_for_keywords(keywords, target_list=["item"], max_results=None)

        # Assert
        # target_list is used by ParseResults, not passed to search_initial via get_all_results_for_keywords's **kwargs
        # max_results=None ensures the date check and final slicing are bypassed for this pagination test.
        mock_search_initial.assert_called_once_with(keywords)
        self.assertEqual(mock_fetch_next_page.call_count, 2)

        self.assertEqual(mock_parse_results.call_count, 3)
        mock_parse_results.assert_any_call({"data_initial": "page1"}, ["item"])
        mock_parse_results.assert_any_call({"data_next": "page2"}, ["item"])
        mock_parse_results.assert_any_call({"data_final": "page3"}, ["item"])

        self.assertEqual(len(all_products), 3)

    @patch.object(GraberServices, 'search_initial')
    @patch.object(GraberServices, 'fetch_next_page')
    @patch.object(GraberServices, 'ParseResults')
    @patch('helper.Helper.unix_data_is_older_than')
    def test_get_all_results_stops_by_unix_data_older(self, mock_unix_older, mock_parse_results, mock_fetch_next_page, mock_search_initial):
        # Arrange
        keywords = "test_days"
        # This 'max_results' is interpreted as 'days_limit' for unix_data_is_older_than
        days_limit_for_older_check = 5

        mock_search_initial.return_value = ({"initial": "data"}, "token1")

        mock_parse_results.side_effect = [
            [{"id": 1, "modified_at": 100}, {"id": 2, "modified_at": 200}],
            # Subsequent calls to ParseResults won't happen if loop breaks
        ]
        # First call to unix_data_is_older_than (after initial parse) returns False
        # Second call (after first fetch_next_page and parse) returns True, stopping pagination
        mock_unix_older.side_effect = [False, True]

        # fetch_next_page will be called once, then unix_data_is_older_than will stop it.
        mock_fetch_next_page.return_value = ({"next_page_data": "data"}, "token2")
                                            # This data won't be fully processed by ParseResults if the test is set up for immediate stop
                                            # Let's adjust ParseResults to reflect this
        mock_parse_results.side_effect = [
             [{"id": 1, "modified_at": 100}, {"id": 2, "modified_at": 200}], # from initial
             [{"id": 3, "modified_at": 300}] # from first next_page (this will be the batch that triggers stop)
        ]


        # Act
        with patch('builtins.print') as mock_print:
            # The function's max_results param is used for final slicing AND for the days_limit.
            all_products = self.graber_services.get_all_results_for_keywords(keywords, max_results=days_limit_for_older_check)

        # Assert
        # The max_results param of get_all_results_for_keywords is NOT passed to search_initial.
        mock_search_initial.assert_called_once_with(keywords)

        # ParseResults for initial data, then unix_data_is_older_than(min_mod_at_batch1, days_limit) -> False
        # fetch_next_page called once
        # ParseResults for next page data, then unix_data_is_older_than(min_mod_at_total, days_limit) -> True. Loop breaks.

        self.assertEqual(mock_unix_older.call_count, 2) # One after initial, one after first fetch
        mock_unix_older.assert_any_call(100, days_limit_for_older_check) # min of first batch
        mock_unix_older.assert_any_call(100, days_limit_for_older_check) # min of combined batch [1,2,3]

        mock_fetch_next_page.assert_called_once()

        self.assertEqual(mock_parse_results.call_count, 2) # Initial + one next page

        # All items accumulated before stopping are [item1, item2, item3]
        # The final slicing is then applied with max_results=days_limit_for_older_check (which is 5)
        # So, all 3 items should be returned.
        self.assertEqual(len(all_products), 3)


    @patch.object(GraberServices, 'search_initial', side_effect=APIConnectionError("Initial search failed"))
    def test_get_all_results_api_connection_error_initial(self, mock_search_initial):
        # Arrange
        keywords = "test"
        # Act
        with patch('builtins.print') as mock_print:
            all_products = self.graber_services.get_all_results_for_keywords(keywords)
            mock_print.assert_any_call("An API connection error occurred: Initial search failed")
        # Assert
        self.assertEqual(all_products, [])

    @patch.object(GraberServices, 'search_initial')
    @patch.object(GraberServices, 'fetch_next_page', side_effect=APIConnectionError("Next page failed"))
    @patch.object(GraberServices, 'ParseResults', return_value=[{"id":1, "modified_at":100}])
    @patch('helper.Helper.unix_data_is_older_than', return_value=False)
    def test_get_all_results_api_connection_error_next_page(self, mock_unix_older, mock_parse, mock_fetch_next_page, mock_search_initial):
        # Arrange
        keywords = "test"
        mock_search_initial.return_value = ({"initial": "data"}, "token1")

        # Act
        with patch('builtins.print') as mock_print:
            all_products = self.graber_services.get_all_results_for_keywords(keywords)
            mock_print.assert_any_call("An API connection error occurred: Next page failed")

        # Assert
        self.assertEqual(len(all_products), 1)
        self.assertEqual(all_products[0]["id"], 1)


    @patch.object(GraberServices, 'search_initial')
    @patch.object(GraberServices, 'fetch_next_page')
    @patch.object(GraberServices, 'ParseResults')
    @patch('helper.Helper.unix_data_is_older_than', return_value=False) # Ensure it doesn't stop early due to date
    def test_get_all_results_final_slicing_by_max_results_param(self, mock_unix_older, mock_parse_results, mock_fetch_next_page, mock_search_initial):
        # Arrange
        keywords = "test_slice"
        max_items_to_return = 2

        mock_search_initial.return_value = ({"data_initial": "page1"}, "token_page2")
        mock_fetch_next_page.return_value = ({"data_next": "page2"}, None)

        mock_parse_results.side_effect = [
            [{"id": 1, "title": "item1", "modified_at": 100}],
            [{"id": 2, "title": "item2", "modified_at": 200}, {"id": 3, "title": "item3", "modified_at": 300}]
        ]
        # Total items accumulated before slicing: 3

        # Act
        with patch('builtins.print') as mock_print:
            all_products = self.graber_services.get_all_results_for_keywords(keywords, max_results=max_items_to_return)

        # Assert
        # unix_data_is_older_than is called with (ANY, max_items_to_return) where max_items_to_return is used as days_limit
        # This test assumes it returns False, so pagination continues until no more pages or error.
        # Then, the final list of 3 items is sliced to max_items_to_return (2).
        self.assertEqual(len(all_products), max_items_to_return)
        self.assertEqual(all_products[0]['id'], 1)
        self.assertEqual(all_products[1]['id'], 2)
        # Check that unix_data_is_older_than was called with max_items_to_return as the day limit
        mock_unix_older.assert_any_call(ANY, max_items_to_return)


if __name__ == '__main__':
    unittest.main()
