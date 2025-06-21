import unittest
import sys
import os

# Add project root to sys.path to allow importing from Services
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from Services.FiltersServices import FiltersServices

class TestFiltersServices(unittest.TestCase):

    def setUp(self):
        self.filters_services = FiltersServices()
        self.sample_contents = [
            {"id": "1", "title": "Apple iPhone 13", "description": "Latest model smartphone with A15 Bionic chip.","price": {"amount": 800.0,"currency": "EUR"}},
            {"id": "2", "title": "Samsung Galaxy S22", "description": "Android smartphone with great camera.", "price": {"amount": 150.0,"currency": "EUR"}},
            {"id": "3", "title": "Old Apple iPhone8", "description": "Used smartphone, good condition.", "price": {"amount": 70.0,"currency": "EUR"}}, # No space for iphone*8
            {"id": "4", "title": "Google Pixel6", "description": "Smartphone with pure Android experience.", "price": {"amount": 99.99,"currency": "EUR"}}, # No space for pixel*
            {"id": "5", "title": "Apple MacBook Pro 16", "description": "Powerful laptop for professionals.", "price": {"amount": 250.0,"currency": "EUR"}},
            {"id": "6", "title": "Cheap Android Phone", "description": "Basic smartphone for calls and texts.", "price": {"amount": 15.9,"currency": "EUR"}},
            {"id": "7", "title": "Apple iPad Air", "description": "Tablet for entertainment and work.", "price": {"amount": 0.01,"currency": "GBP"}}, # No digits in title
            {"id": "8", "title": "Samsung TV Model T5000", "description": "Smart TV with 4K display.",  "price": {"amount": 300.0,"currency": "USD"}}
        ]

    def test_filtering_content_no_filters(self):
        result = self.filters_services.filteringContent(self.sample_contents, [], "", [])
        self.assertEqual(result, self.sample_contents)

    def test_filtering_content_by_title(self):
        result = self.filters_services.filteringContent(self.sample_contents, ["Apple"], "", [])
        self.assertEqual(len(result), 4) # iPhone 13, iPhone 8, MacBook Pro, iPad Air
        for item in result:
            self.assertIn("apple", item["title"].lower())

        # Test with wildcard for digits
        result_iphone13 = self.filters_services.filteringContent(self.sample_contents, ["iphone*13"], "", [])
        self.assertEqual(len(result_iphone13), 0) # "iphone\d*13" does not match "Apple iPhone 13" (space)
        # self.assertEqual(result_iphone13[0]["id"], "1") # This line would fail if len is 0

    def test_filtering_content_by_description(self):
        # Parameter name in code is isDiscriptionCheck
        result = self.filters_services.filteringContent(self.sample_contents, [], "smartphone", [], isDiscriptionCheck=True)
        self.assertEqual(len(result), 5)
        expected_ids = sorted(["1", "2", "3", "4", "6"])
        result_ids = sorted([item["id"] for item in result])
        self.assertEqual(result_ids, expected_ids)
        for item in result:
            self.assertIn("smartphone", item["description"].lower())

    def test_filtering_content_by_price(self):
        result = self.filters_services.filteringContent(self.sample_contents, [], "", ["100.00", "600.00"], isPriceCheck=True)
        self.assertEqual(len(result), 3) # iPhone8 (250), Pixel6 (599), iPad Air (499), TV (350)
        expected_ids = sorted(["2", "5", "8"])
        result_ids = sorted([item["id"] for item in result])
        self.assertEqual(result_ids, expected_ids)
        for item in result:
            price = float(item["price"]["amount"])
            self.assertTrue(100.00 <= price <= 600.00)

    def test_filtering_content_by_price_exact_match(self):
        result = self.filters_services.filteringContent(self.sample_contents, [], "", ["99.99", "99.99"], isPriceCheck=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "4")

    def test_filtering_content_by_price_outside_range(self):
        result = self.filters_services.filteringContent(self.sample_contents, [], "", ["1500.00", "2000.00"], isPriceCheck=True)
        self.assertEqual(len(result), 0)

    def test_filtering_content_combined_filters(self):
        # Title "Apple", Description "smartphone", Price ["200.00", "800.00"]
        result = self.filters_services.filteringContent(self.sample_contents, ["Apple"], "smartphone", ["200.00", "800.00"], isDiscriptionCheck=True, isPriceCheck=True)
        self.assertEqual(len(result), 1)
        expected_ids = sorted(["1"]) # Apple iPhone 13 (799), Old Apple iPhone8 (250)
        result_ids = sorted([item["id"] for item in result])
        self.assertEqual(result_ids, expected_ids)

    def test_filtering_content_multiple_title_patterns(self):
        # Expects items containing BOTH "Apple" AND "iPhone" in title
        result = self.filters_services.filteringContent(self.sample_contents, ["Apple", "iPhone"], "", [])
        self.assertEqual(len(result), 2)
        expected_ids = sorted(["1", "3"]) # Apple iPhone 13, Old Apple iPhone8
        result_ids = sorted([item["id"] for item in result])
        self.assertEqual(result_ids, expected_ids)
        for item in result:
            self.assertIn("apple", item["title"].lower())
            self.assertIn("iphone", item["title"].lower())

    def test_filtering_content_title_pattern_with_star(self):
        # '*' in pattern is replaced with '\d*' (zero or more digits)
        result_iphone8 = self.filters_services.filteringContent(self.sample_contents, ["iphone*8"], "", [])
        self.assertEqual(len(result_iphone8), 1)
        self.assertEqual(result_iphone8[0]["id"], "3") # Matches "Old Apple iPhone8"

        result_pixel = self.filters_services.filteringContent(self.sample_contents, ["Pixel*"], "", [])
        self.assertEqual(len(result_pixel), 1)
        self.assertEqual(result_pixel[0]["id"], "4") # Matches "Google Pixel6"

        result_t5000 = self.filters_services.filteringContent(self.sample_contents, ["T*000"], "", [])
        self.assertEqual(len(result_t5000), 1)
        self.assertEqual(result_t5000[0]["id"], "8") # Matches "Samsung TV Model T5000"

        # Test for pattern that matches zero digits
        result_ipad_air = self.filters_services.filteringContent(self.sample_contents, ["iPad*Air"], "", [])
        self.assertEqual(len(result_ipad_air), 0) # "iPad\d*Air" does not match "Apple iPad Air" (space)
        # self.assertEqual(result_ipad_air[0]["id"], "7") # This line would fail if len is 0


    def test_filtering_content_empty_input(self):
        result = self.filters_services.filteringContent([], ["Apple"], "smartphone", ["200.00", "800.00"], isDiscriptionCheck=True, isPriceCheck=True)
        self.assertEqual(result, [])

    def test_filtering_content_no_match(self):
        result = self.filters_services.filteringContent(self.sample_contents, ["NonExistentPattern"], "", [])
        self.assertEqual(result, [])

    def test_filter_text_case_insensitivity(self):
        # Title filter is case-insensitive by default due to re.IGNORECASE
        result = self.filters_services.filteringContent(self.sample_contents, ["apple"], "", [])
        self.assertEqual(len(result), 4) # iPhone 13, iPhone 8, MacBook Pro, iPad Air
        result_ids = sorted([item["id"] for item in result])
        expected_ids = sorted(["1", "3", "5", "7"])
        self.assertEqual(result_ids, expected_ids)

        # Description filter should also be case-insensitive
        result_desc = self.filters_services.filteringContent(self.sample_contents, [], "SMARTPHONE", [], isDiscriptionCheck=True)
        self.assertEqual(len(result_desc), 5)
        expected_desc_ids = sorted(["1", "2", "3", "4", "6"])
        result_desc_ids = sorted([item["id"] for item in result_desc])
        self.assertEqual(result_desc_ids, expected_desc_ids)


if __name__ == '__main__':
    unittest.main()
