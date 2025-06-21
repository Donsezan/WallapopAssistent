import unittest
from unittest.mock import patch, MagicMock, call # Added call for checking multiple calls
import sys
import os
import json # Added for the new test

# Adjust the path to import from the root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timezone # Added as per requirement
from main_logic import Main_logic
from Services.GraberServices import GraberServices, APIConnectionError # GraberServices might be mocked directly
from constants import Constants
from helper import Helper
from Context.paramtersContext import ParamtersContext # Assuming this is the type of self.ctx.MainParameters
from Context.context import Context # Assuming this is the type of self.ctx

class TestMainLogic(unittest.TestCase):
    def setUp(self):
        # Mock context and its nested MainParameters
        self.mock_ctx = MagicMock(spec=Context)
        self.mock_main_parameters = MagicMock(spec=ParamtersContext)
        self.mock_ctx.MainParameters = self.mock_main_parameters

        # Common default return values for mocked context methods
        self.mock_main_parameters.get_search_text.return_value = "default_keyword"
        self.mock_main_parameters.get_search_type.return_value = Constants.SearchType.Direct_search # Default to Direct_search
        self.mock_main_parameters.get_history_digging_days.return_value = 30 # Default
        self.mock_main_parameters.get_content_filter_checkBox.return_value = Constants.CheackBox_enabled_status
        self.mock_main_parameters.get_content_filter_text.return_value = ""
        self.mock_main_parameters.get_price_filter_checkbox.return_value = "disabled" # Important: provide default
        self.mock_main_parameters.get_price_limit_from.return_value = "0"
        self.mock_main_parameters.get_price_limit_to.return_value = "1000"
        self.mock_main_parameters.get_dict.return_value = {} # For rehydrate_contnet calls if any
        self.mock_ctx.get_context_rehydrate_state.return_value = True # Prevent rehydrate_contnet actual logic
        self.mock_ctx.get_updated_paramter_status.return_value = False # Prevent Download_content actual logic initially

        self.main_logic_instance = Main_logic(self.mock_ctx)

        # It might be useful to also mock FileServices and FiltersServices if their real implementations interfere
        # For now, assuming their impact on load_content is minimal or handled by context mocks.

    def test_initialization(self):
        # A simple test to ensure the test file is runnable and setUp works
        self.assertIsNotNone(self.main_logic_instance)
        print("TestMainLogic initialized successfully.")

    @patch('main_logic.datetime') # Mock datetime for this test
    @patch('main_logic.GraberServices') # Patch GraberServices in the module where it's used by Main_logic
    def test_load_content_direct_search_success(self, MockGraberServices, MockCustomDatetime):
        # Renamed from test_load_content_direct_search_success_with_date_mock
        mock_graber_instance = MockGraberServices.return_value

        # Setup mock for datetime.now()
        mock_now_for_test = datetime(2023, 1, 5, 0, 0, 0, tzinfo=timezone.utc) # A date close to item dates
        MockCustomDatetime.now.return_value = mock_now_for_test
        real_datetime_fromisoformat = datetime.fromisoformat
        MockCustomDatetime.fromisoformat.side_effect = lambda d_str: real_datetime_fromisoformat(d_str.replace('Z', '+00:00'))

        # Define mock product data
        product1_k1 = {'id': '1', 'title': 'Product 1 k1', 'modified_at': '2023-01-01T10:00:00Z', 'creation_date': '2023-01-01T10:00:00Z'}
        product2_k1 = {'id': '2', 'title': 'Product 2 k1', 'modified_at': '2023-01-03T10:00:00Z', 'creation_date': '2023-01-03T10:00:00Z'}
        product1_k2 = {'id': '3', 'title': 'Product 1 k2', 'modified_at': '2023-01-02T10:00:00Z', 'creation_date': '2023-01-02T10:00:00Z'}
        duplicate_product_k2 = {'id': '1', 'title': 'Duplicate Product k2', 'modified_at': '2023-01-04T10:00:00Z', 'creation_date': '2023-01-04T10:00:00Z'}

        def graber_side_effect(keywords, target_list, max_results, **kwargs):
            mock_graber_instance.search_id = "dummy_search_id" 
            if keywords == "keyword1":
                return [product1_k1, product2_k1]
            elif keywords == "keyword2":
                return [product1_k2, duplicate_product_k2]
            return []
        mock_graber_instance.get_all_results_for_keywords.side_effect = graber_side_effect

        self.mock_main_parameters.get_search_type.return_value = Constants.SearchType.Direct_search
        self.mock_main_parameters.get_search_text.return_value = "keyword1" + Constants.SearchString_Siparator + "keyword2"
        self.mock_main_parameters.get_history_digging_days.return_value = 365 
        self.mock_main_parameters.get_dip_limit.return_value = 0 

        results = self.main_logic_instance.load_content(sorted_objects=[], key='test_direct_search_key')

        expected_calls_corrected = [
            call(keywords="keyword1", target_list=None, max_results=None),
            call(keywords="keyword2", target_list=None, max_results=None)
        ]
        mock_graber_instance.get_all_results_for_keywords.assert_has_calls(expected_calls_corrected, any_order=False)
        self.assertEqual(mock_graber_instance.get_all_results_for_keywords.call_count, 2)
        
        self.assertEqual(len(results), 3, f"Results were: {results}") 
        self.assertEqual(results[0]['id'], '2') 
        self.assertEqual(results[1]['id'], '3') 
        self.assertEqual(results[2]['id'], '1') 


    @patch('main_logic.datetime') # Mock datetime for this test
    @patch.object(Constants, 'Items_per_rotation', 2)
    @patch('main_logic.GraberServices')
    def test_load_content_history_search_success(self, MockGraberServices, MockCustomDatetime): # Signature updated
        mock_graber_instance = MockGraberServices.return_value

        # Setup mock for datetime.now()
        mock_now_for_test = datetime(2023, 2, 5, 0, 0, 0, tzinfo=timezone.utc) # A date close to item dates
        MockCustomDatetime.now.return_value = mock_now_for_test
        real_datetime_fromisoformat = datetime.fromisoformat
        MockCustomDatetime.fromisoformat.side_effect = lambda d_str: real_datetime_fromisoformat(d_str.replace('Z', '+00:00'))

        # Define mock product data (more than max_results to test slicing by the service mock)
        product1 = {'id': '10', 'title': 'History Product 10', 'modified_at': '2023-02-01T10:00:00Z', 'creation_date': '2023-02-01T10:00:00Z'}
        product2 = {'id': '11', 'title': 'Unique History Product 11', 'modified_at': '2023-02-03T10:00:00Z', 'creation_date': '2023-02-03T10:00:00Z'}
        product3 = {'id': '12', 'title': 'Test History Product 12', 'modified_at': '2023-02-02T10:00:00Z', 'creation_date': '2023-02-02T10:00:00Z'}
        product4 = {'id': '13', 'title': 'Another History Product 13', 'modified_at': '2023-02-04T10:00:00Z', 'creation_date': '2023-02-04T10:00:00Z'}

        mock_api_return_data_for_side_effect = [product1, product2, product3, product4]

        def graber_side_effect(keywords, target_list, max_results, **kwargs):
            mock_graber_instance.search_id = "dummy_search_id_history"
            # Simulate the GraberService's behavior: it gets all items, then sorts, then applies max_results
            # For simplicity in the mock, we can just slice, as load_content will re-sort anyway.
            # The key is that the *number* of items returned by the mock respects max_results.
            data_to_return = list(mock_api_return_data_for_side_effect) # Use a copy
            if max_results is not None:
                # Sorting before slicing is what GraberServices.get_all_results_for_keywords does.
                # Let's simulate that for accuracy of what load_content receives.
                # Note: GraberServices.get_all_results_for_keywords sorts, then ParseResults is called, then it's sorted again in main_logic.
                # The mock here simulates the *final* output of get_all_results_for_keywords *before* it's returned to main_logic.
                # That method internally calls ParseResults, and the list *from ParseResults* is what might be sliced by max_results.
                # However, the current GraberServices.get_all_results_for_keywords applies max_results *after* ParseResults.
                # So, the data passed to ParseResults is complete, then ParseResults filters, then max_results is applied.
                # For this mock, we assume target_list in ParseResults doesn't filter these items for simplicity of testing max_results.

                # Correct simulation: get_all_results_for_keywords fetches all, then calls ParseResults, then applies max_results.
                # Let's assume ParseResults (with the given target_list) returns all items from data_to_return here.
                # Then max_results is applied.
                # The sorting for max_results should happen *before* slicing.

                # Sort by modified_at descending (newest first) to mimic ParseResults output if it were sorted,
                # or just to ensure the slice for max_results is deterministic.
                # The actual ParseResults in GraberServices doesn't sort. Sorting is done in main_logic.
                # The get_all_results_for_keywords in GraberServices applies max_results to the list *from* ParseResults.
                # So, if ParseResults returns an unsorted list, max_results slices that.
                # For this test, let's make the side_effect simple: return a list sliced by max_results.
                # The sorting aspect will be handled by main_logic.
                if max_results is not None:
                    data_to_return = data_to_return[:max_results] # Simple slice for the mock
            return data_to_return

        mock_graber_instance.get_all_results_for_keywords.side_effect = graber_side_effect

        # Configure context for History Search
        search_type_history = getattr(Constants.SearchType, 'History_search', 1)
        self.mock_main_parameters.get_search_type.return_value = search_type_history

        search_text_history = "history keyword" # This will be split by SearchString_Siparator for target_list
        self.mock_main_parameters.get_search_text.return_value = search_text_history
        self.mock_main_parameters.get_history_digging_days.return_value = 365

        self.mock_main_parameters.get_dip_limit.return_value = 1 # dip_limit = 1
        # Items_per_rotation is patched to 2 by decorator, so max_items_to_fetch in load_content will be 1 * 2 = 2

        results = self.main_logic_instance.load_content(sorted_objects=[], key='test_history_search_key')

        # Assertions
        expected_target_list_param = search_text_history.split(Constants.SearchString_Siparator)
        mock_graber_instance.get_all_results_for_keywords.assert_called_once_with(
            keywords=search_text_history,      # Full search text used as 'keywords' for API
            target_list=expected_target_list_param, # Split text used as 'target_list' for ParseResults inside service
            max_results=2
        )

        # The mocked service (via side_effect) returns a list of 2 items (due to max_results=2).
        # In this mock, it's [product1, product2] because of the simple slice.
        # main_logic.load_content then sorts these:
        # product2 (P_id=11, date=03)
        # product1 (P_id=10, date=01)

        self.assertEqual(len(results), 2)
        # Based on the simple slice [product1, product2] and then main_logic sorting them:
        self.assertEqual(results[0]['id'], '11') # product2 (2023-02-03)
        self.assertEqual(results[1]['id'], '10') # product1 (2023-02-01)

    @patch('main_logic.GraberServices')
    @patch.object(Main_logic, 'rehydrate_contnet') # Patching the method on the class instance via the class
    def test_load_content_api_error_exception_raised(self, mock_rehydrate_contnet_method, MockGraberServices):
        mock_graber_instance = MockGraberServices.return_value

        # Configure GraberServices mock to raise APIConnectionError
        mock_graber_instance.get_all_results_for_keywords.side_effect = APIConnectionError("Test API Failure")

        # Configure context (search type doesn't strictly matter for this error path)
        self.mock_main_parameters.get_search_type.return_value = Constants.SearchType.Direct_search
        self.mock_main_parameters.get_search_text.return_value = "any_keyword"
        self.mock_main_parameters.get_dip_limit.return_value = 0 # No limit

        # Call the method under test
        results = self.main_logic_instance.load_content(sorted_objects=[], key='test_api_error_key')

        # Assertions
        self.assertEqual(results, []) # Expect an empty list on API error

        # Verify that rehydrate_contnet was called with offline_error=True
        mock_rehydrate_contnet_method.assert_called_once_with(offline_error=True)

    @patch('main_logic.GraberServices')
    @patch.object(Main_logic, 'rehydrate_contnet') # Patching the method on the class instance via the class
    def test_load_content_api_returns_empty_and_no_search_id(self, mock_rehydrate_contnet_method, MockGraberServices):
        mock_graber_instance = MockGraberServices.return_value

        # Configure GraberServices mock to return empty list and no search_id
        def graber_side_effect(keywords, target_list, max_results, **kwargs):
            # Simulate that the call to GraberServices did not successfully establish a search.
            mock_graber_instance.search_id = None
            return []
        mock_graber_instance.get_all_results_for_keywords.side_effect = graber_side_effect

        # Configure context
        self.mock_main_parameters.get_search_type.return_value = Constants.SearchType.Direct_search
        self.mock_main_parameters.get_search_text.return_value = "keyword_for_empty_return"
        self.mock_main_parameters.get_dip_limit.return_value = 0

        results = self.main_logic_instance.load_content(sorted_objects=[], key='test_empty_return_key')

        self.assertEqual(results, [])
        mock_rehydrate_contnet_method.assert_called_once_with(offline_error=True)

    @patch('main_logic.GraberServices')
    @patch('main_logic.datetime') # Mock datetime for this specific test
    def test_load_content_deduplication_and_sorting(self, MockCustomDatetime, MockGraberServices):
        # Renamed from test_load_content_deduplication_and_sorting_with_date_mock
        mock_graber_instance = MockGraberServices.return_value

        # Setup mock for datetime.now() within main_logic's scope for this test
        mock_now_for_test = datetime(2023, 3, 5, 0, 0, 0, tzinfo=timezone.utc) # A date close to item dates
        MockCustomDatetime.now.return_value = mock_now_for_test
        real_datetime_fromisoformat = datetime.fromisoformat
        MockCustomDatetime.fromisoformat.side_effect = lambda d_str: real_datetime_fromisoformat(d_str.replace('Z', '+00:00'))


        # Define mock product data with duplicates and unsorted order (same as original test)
        p1_v1 = {'id': 'A', 'title': 'Product A v1', 'modified_at': '2023-03-01T10:00:00Z', 'creation_date': '2023-03-01T10:00:00Z'}
        p2    = {'id': 'B', 'title': 'Product B',    'modified_at': '2023-03-03T10:00:00Z', 'creation_date': '2023-03-03T10:00:00Z'}
        p1_v2 = {'id': 'A', 'title': 'Product A v2', 'modified_at': '2023-03-02T10:00:00Z', 'creation_date': '2023-03-02T10:00:00Z'} 
        p3    = {'id': 'C', 'title': 'Product C',    'modified_at': '2023-03-01T12:00:00Z', 'creation_date': '2023-03-01T12:00:00Z'}
        mock_service_results = [p1_v1, p2, p1_v2, p3]

        def graber_side_effect(keywords, target_list, max_results, **kwargs):
            mock_graber_instance.search_id = "dummy_search_id_dedup_sort_mocked_date"
            # This mock does not slice by max_results, returns all 4 items.
            return mock_service_results
        mock_graber_instance.get_all_results_for_keywords.side_effect = graber_side_effect

        # Configure context (same as original test)
        self.mock_main_parameters.get_search_type.return_value = Constants.SearchType.History_search 
        self.mock_main_parameters.get_search_text.return_value = "dedup_sort_keywords_mocked_date"
        self.mock_main_parameters.get_history_digging_days.return_value = 365 
        self.mock_main_parameters.get_dip_limit.return_value = 0 # Results in max_items_to_fetch = 10

        results = self.main_logic_instance.load_content(sorted_objects=[], key='test_dedup_sort_mocked_date_key')
        
        # Assertions (same as original test)
        mock_graber_instance.get_all_results_for_keywords.assert_called_once()
        self.assertEqual(len(results), 3, f"Results were: {results}") # Added message for easier debugging
        self.assertEqual(results[0]['id'], 'B') 
        self.assertEqual(results[1]['id'], 'C') 
        self.assertEqual(results[2]['id'], 'A') 


    @patch('main_logic.GraberServices')
    @patch('main_logic.datetime') # Mock datetime used by main_logic
    def test_load_content_date_filtering(self, MockMainLogicDatetime, MockGraberServices):
        mock_graber_instance = MockGraberServices.return_value

        # Setup mock for datetime.now() within main_logic's scope
        mock_now = datetime(2023, 3, 15, 12, 0, 0, tzinfo=timezone.utc)
        MockMainLogicDatetime.now.return_value = mock_now

        # Ensure datetime.fromisoformat and strptime called by main_logic uses the real one for parsing strings to dates
        # The mock should only control what 'now' is.
        real_datetime_fromisoformat = datetime.fromisoformat
        real_datetime_strptime = datetime.strptime
        MockMainLogicDatetime.fromisoformat.side_effect = lambda d_str: real_datetime_fromisoformat(d_str)
        MockMainLogicDatetime.strptime.side_effect = lambda d_str, fmt: real_datetime_strptime(d_str, fmt)
        # Pass through the class itself for direct calls like datetime.strptime if any part of main_logic uses that form.
        # Also handles direct instantiation like datetime(Y,M,D, tzinfo=...) if used
        MockMainLogicDatetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs) if args else MockMainLogicDatetime # Return the mock for class-level access


        # Define mock product data from GraberServices
        p_very_new    = {'id': 'D1', 'title': 'Product Very New',    'modified_at': '2023-03-14T00:00:00Z', 'creation_date': '2023-03-14T00:00:00Z'}
        p_newish      = {'id': 'D2', 'title': 'Product Newish',      'modified_at': '2023-03-10T00:00:00Z', 'creation_date': '2023-03-10T00:00:00Z'}
        p_boundary    = {'id': 'D3', 'title': 'Product Boundary',    'modified_at': '2023-03-08T11:00:00Z', 'creation_date': '2023-03-08T11:00:00Z'}
        p_too_old     = {'id': 'D4', 'title': 'Product Too Old',     'modified_at': '2023-03-01T00:00:00Z', 'creation_date': '2023-03-01T00:00:00Z'}
        p_older_than_sorted = {'id': 'D5', 'title': 'Older than sorted', 'modified_at': '2023-03-09T00:00:00Z', 'creation_date': '2023-03-09T00:00:00Z'}

        mock_service_results = [p_very_new, p_newish, p_boundary, p_too_old, p_older_than_sorted]

        def graber_side_effect(keywords, target_list, max_results, **kwargs):
            mock_graber_instance.search_id = "dummy_search_id_date_filter"
            return mock_service_results
        mock_graber_instance.get_all_results_for_keywords.side_effect = graber_side_effect

        # Configure context
        self.mock_main_parameters.get_search_type.return_value = Constants.SearchType.History_search
        self.mock_main_parameters.get_search_text.return_value = "date_filter_keywords"
        self.mock_main_parameters.get_history_digging_days.return_value = 7
        self.mock_main_parameters.get_dip_limit.return_value = 0

        prepared_sorted_objects = [{'id': 'S1', 'title': 'Sorted Object Newest', 'modified_at': '2023-03-09T05:00:00Z', 'creation_date': '2023-03-09T05:00:00Z'}]

        results = self.main_logic_instance.load_content(sorted_objects=prepared_sorted_objects, key='test_date_filter_key')

        # Expected filtering based on trace: [p_very_new, p_newish]
        # Sorted order by main_logic: p_very_new (Mar 14), p_newish (Mar 10)
        # p_older_than_sorted (Mar 9, 0am) is <= prepared_sorted_objects[0] (Mar 9, 5am) -> loop breaks
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], 'D1') # p_very_new
        self.assertEqual(results[1]['id'], 'D2') # p_newish

    @patch('main_logic.datetime')
    @patch('main_logic.GraberServices') # Patch GraberServices as it's called by load_content
    def test_load_content_with_history_files(self, MockGraberServices, MockCustomDatetime):
        mock_graber_instance = MockGraberServices.return_value
        # Simulate a successful API call by setting a search_id attribute for most cases
        mock_graber_instance.search_id = "dummy_search_id_history_files_test"

        # --- Test Case 3: Date filtering behavior ---
        # (Implementing this one first as it's most aligned with the "history files" theme)
        with self.subTest("Date filtering with history and new items"):
            # Mock datetime.now()
            mock_now_dt = datetime(2024, 1, 25, 0, 0, 0, tzinfo=timezone.utc)
            MockCustomDatetime.now.return_value = mock_now_dt
            real_datetime_fromisoformat = datetime.fromisoformat
            MockCustomDatetime.fromisoformat.side_effect = lambda d_str: real_datetime_fromisoformat(d_str.replace('Z', '+00:00'))
            
            # Load one of the history files
            history_file_path = os.path.join("temp", "History_8bccf737-622c-4443-b58c-93ebc65a3a40.json")
            with open(history_file_path, 'r') as f:
                sorted_history_data = json.load(f) # Laptop (2024-01-15), Phone (2024-01-01)
            
            # Configure MainParameters for this subtest
            self.mock_main_parameters.get_history_digging_days.return_value = 12 # Items older than 2024-01-13 are too old
            self.mock_main_parameters.get_search_text.return_value = "any_search" # Not relevant for this filter part
            self.mock_main_parameters.get_dip_limit.return_value = 0 # max_results = None
            self.mock_main_parameters.get_search_type.return_value = Constants.SearchType.History_search

            # New items to be returned by GraberServices
            new_item1 = {"id": "101", "title": "Very New Gadget", "modified_at": "2024-01-20T00:00:00Z"} # Keep (recent)
            new_item2 = {"id": "102", "title": "Newish Gadget", "modified_at": "2024-01-14T00:00:00Z"} # Keep (within 12 days, newer than history item 1)
            new_item3 = {"id": "103", "title": "Old Gadget", "modified_at": "2024-01-10T00:00:00Z"}    # Filtered out (older than 12 days)
            new_item4 = {"id": "104", "title": "Gadget Older Than History", "modified_at": "2024-01-12T00:00:00Z"} # Filtered out (older than newest history item which is 2024-01-15)
                                                                                                                        # and also older than 12 days from mock_now_dt
            new_item5 = {"id": "105", "title": "Gadget Same Day as History Newest", "modified_at": "2024-01-15T11:00:00Z"} # Keep (newer than history item 1)

            mock_graber_instance.get_all_results_for_keywords.return_value = [new_item1, new_item2, new_item3, new_item4, new_item5]

            results = self.main_logic_instance.load_content(sorted_objects=sorted_history_data, key='date_filter_test_key')
            
            # Assertions for date filtering
            # Expected: new_item1 (2024-01-20), new_item5 (2024-01-15T11), new_item2 (2024-01-14)
            # new_item3 (2024-01-10) is older than 12 days from 2024-01-25.
            # new_item4 (2024-01-12) is older than 12 days from 2024-01-25.
            # newest item in sorted_history_data is 2024-01-15T10:00:00Z.
            # new_item1 (Jan 20) is newer.
            # new_item5 (Jan 15 T11) is newer.
            # new_item2 (Jan 14) is older than latest_existing_item_date (Jan 15 T10) -> loop breaks.
            # All subsequent items (new_item4, new_item3) are also older.
            # Expected items: new_item1, new_item5.
            
            self.assertEqual(len(results), 2, f"Expected 2 items, got {len(results)}. Results: {results}")
            result_ids = {item['id'] for item in results}
            self.assertEqual(result_ids, {"101", "105"})

        # --- Test Case 1: Varying search_text ---
        with self.subTest("Varying search_text parameter"):
            self.mock_main_parameters.get_search_text.return_value = "Specific Search Term"
            self.mock_main_parameters.get_dip_limit.return_value = 0 # max_results = None
            self.mock_main_parameters.get_search_type.return_value = Constants.SearchType.History_search
            # Ensure datetime doesn't interfere if not explicitly set for this subtest
            MockCustomDatetime.now.return_value = datetime(2024,1,25,0,0,0, tzinfo=timezone.utc)


            mock_graber_instance.get_all_results_for_keywords.return_value = [{"id": "S1", "title": "Search Result", "modified_at": "2024-01-24T00:00:00Z"}]
            
            # Using an empty history for simplicity of checking Graber call
            self.main_logic_instance.load_content(sorted_objects=[], key='search_text_test_key')
            
            expected_target_list = "Specific Search Term".split(Constants.SearchString_Siparator)
            mock_graber_instance.get_all_results_for_keywords.assert_called_with(
                keywords="Specific Search Term", 
                target_list=expected_target_list, 
                max_results=None
            )

        # --- Test Case 2: Varying dip_limit ---
        with self.subTest("Varying dip_limit parameter"):
            self.mock_main_parameters.get_search_text.return_value = "any"
            self.mock_main_parameters.get_search_type.return_value = Constants.SearchType.History_search
            MockCustomDatetime.now.return_value = datetime(2024,1,25,0,0,0, tzinfo=timezone.utc)


            # Scenario A: dip_limit = 1 (max_results = 1 * Constants.Items_per_rotation (default 40))
            self.mock_main_parameters.get_dip_limit.return_value = 1 
            # Patch Items_per_rotation for this specific call if needed, or use default. Default is 40.
            # To make it testable without changing global Constants, we can assume Graber mock will just receive it.
            expected_max_A = 1 * Constants.Items_per_rotation # Default 40
            
            mock_graber_instance.get_all_results_for_keywords.return_value = [{"id": "D1", "title": "DipLimit Result A", "modified_at": "2024-01-24T00:00:00Z"}]
            self.main_logic_instance.load_content(sorted_objects=[], key='dip_limit_test_key_A')
            args_A, kwargs_A = mock_graber_instance.get_all_results_for_keywords.call_args
            self.assertEqual(kwargs_A['max_results'], expected_max_A)

            # Scenario B: dip_limit = 0 (max_results = None)
            self.mock_main_parameters.get_dip_limit.return_value = 0
            mock_graber_instance.get_all_results_for_keywords.return_value = [{"id": "D2", "title": "DipLimit Result B", "modified_at": "2024-01-24T00:00:00Z"}]
            self.main_logic_instance.load_content(sorted_objects=[], key='dip_limit_test_key_B')
            args_B, kwargs_B = mock_graber_instance.get_all_results_for_keywords.call_args
            self.assertIsNone(kwargs_B['max_results'])
            
            # Scenario C: dip_limit = None (max_results = 10)
            self.mock_main_parameters.get_dip_limit.return_value = None
            mock_graber_instance.get_all_results_for_keywords.return_value = [{"id": "D3", "title": "DipLimit Result C", "modified_at": "2024-01-24T00:00:00Z"}]
            self.main_logic_instance.load_content(sorted_objects=[], key='dip_limit_test_key_C')
            args_C, kwargs_C = mock_graber_instance.get_all_results_for_keywords.call_args
            self.assertEqual(kwargs_C['max_results'], 10)


if __name__ == '__main__':
    unittest.main()
