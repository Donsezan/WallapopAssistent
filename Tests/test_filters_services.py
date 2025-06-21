import unittest
from Services.FiltersServices import FiltersServices

class TestFiltersServices(unittest.TestCase):

    def setUp(self):
        self.filter_services = FiltersServices()
        self.sample_contents = [
            {"id": 1, "title": "Amazing New Laptop", "description": "Latest model with great specs", "price": {"amount": "1200.00"}},
            {"id": 2, "title": "Old Desktop Computer", "description": "Still works, good for parts", "price": {"amount": "150.00"}},
            {"id": 3, "title": "Wireless Mouse", "description": "Ergonomic and responsive", "price": {"amount": "25.00"}},
            {"id": 4, "title": "Mechanical Keyboard", "description": "Clicky keys, RGB lighting", "price": {"amount": "75.00"}},
            {"id": 5, "title": "Laptop Pro X2000", "description": "Business laptop, very secure", "price": {"amount": "950.00"}},
            {"id": 6, "title": "Gaming Laptop G-Force", "description": "High-end GPU, 144Hz screen", "price": {"amount": "2500.00"}},
            {"id": 7, "title": "Monitor 27 inch", "description": "IPS panel, great colors", "price": {"amount": "300.00"}},
            {"id": 8, "title": "Tablet Android 10 inch", "description": "Good for media consumption", "price": {"amount": "220.00"}},
            {"id": 9, "title": "Smartphone X", "description": "Latest flagship phone", "price": {"amount": "1000.00"}},
            {"id": 10, "title": "Used Laptop", "description": "Decent condition, good for students", "price": {"amount": "450.00"}},
            {"id": 11, "title": "Product Model G123Force", "description": "Special G model", "price": {"amount": "350.00"}}, # For title wildcard test
            {"id": 12, "title": "Big Screen TV", "description": "Size 14400 screen, ultra HD", "price": {"amount": "1800.00"}}, # For desc wildcard test
        ]

    # Tests for filteringContent
    def test_filtering_content_by_title(self):
        # Arrange
        patterns = ["laptop"]
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, patterns, [], priceRange=None, isDiscriptionCheck=False, isPriceCheck=False)
        # Assert
        self.assertEqual(len(filtered), 4) # IDs: 1, 5, 6, 10
        self.assertTrue(all("laptop" in item["title"].lower() for item in filtered))
        ids = {item["id"] for item in filtered}
        self.assertEqual(ids, {1, 5, 6, 10})


    def test_filtering_content_by_title_with_star_wildcard_for_digits(self):
        # Arrange
        patterns = ["laptop pro x*"] # This expects digits after x, e.g. x2000
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, patterns, [], priceRange=None, isDiscriptionCheck=False, isPriceCheck=False)
        # Assert
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], 5) # Laptop Pro X2000

    def test_filtering_content_by_description(self):
        # Arrange
        patterns = ["great specs"]
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, [], patterns, priceRange=None, isDiscriptionCheck=True, isPriceCheck=False)
        # Assert
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], 1) # Amazing New Laptop

    def test_filtering_content_by_price_range(self):
        # Arrange
        price_range = ("100.00", "500.00")
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, [], [], priceRange=price_range, isDiscriptionCheck=False, isPriceCheck=True)
        # Assert
        # Items in range (inclusive): 150 (ID 2), 300 (ID 7), 220 (ID 8), 450 (ID 10), 350 (ID 11)
        self.assertEqual(len(filtered), 5)
        ids = {item["id"] for item in filtered}
        self.assertEqual(ids, {2, 7, 8, 10, 11})


    def test_filtering_content_combined_title_and_price(self):
        # Arrange
        title_patterns = ["laptop"]
        price_range = ("900.00", "1500.00")
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, title_patterns, [], priceRange=price_range, isDiscriptionCheck=False, isPriceCheck=True)
        # Assert
        # Laptops: 1 (1200), 5 (950), 6 (2500), 10 (450)
        # Price range (900-1500): 1 (1200), 5 (950), 9 (1000)
        # Combined: Laptop AND Price (900-1500) => ID 1 (1200), ID 5 (950)
        self.assertEqual(len(filtered), 2)
        ids = {item["id"] for item in filtered}
        self.assertEqual(ids, {1, 5})

    def test_filtering_content_combined_all_filters(self):
        # Arrange
        title_patterns = ["laptop"]
        desc_patterns = ["latest model"]
        price_range = ("1000.00", "1500.00")
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, title_patterns, desc_patterns, priceRange=price_range, isDiscriptionCheck=True, isPriceCheck=True)
        # Assert
        # Title "laptop": 1, 5, 6, 10
        # Desc "latest model": 1
        # Price (1000-1500): 1 (1200), 9 (1000)
        # All combined: ID 1
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], 1)

    def test_filtering_content_no_match_title(self):
        # Arrange
        patterns = ["nonexistent"]
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, patterns, [], priceRange=None, isDiscriptionCheck=False, isPriceCheck=False)
        # Assert
        self.assertEqual(len(filtered), 0)

    def test_filtering_content_no_match_price(self):
        # Arrange
        price_range = ("5000.00", "6000.00")
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, [], [], priceRange=price_range, isDiscriptionCheck=False, isPriceCheck=True)
        # Assert
        self.assertEqual(len(filtered), 0)

    def test_filtering_content_empty_input_contents(self):
        # Arrange
        patterns = ["laptop"]
        # Act
        filtered = self.filter_services.filteringContent([], patterns, [], priceRange=None, isDiscriptionCheck=False, isPriceCheck=False)
        # Assert
        self.assertEqual(len(filtered), 0)

    def test_filtering_content_none_input_contents(self):
        # Arrange
        patterns = ["laptop"]
        # Act
        filtered = self.filter_services.filteringContent(None, patterns, [], priceRange=None, isDiscriptionCheck=False, isPriceCheck=False)
        # Assert
        self.assertIsNone(filtered)

    def test_filtering_content_no_filters_applied(self):
        # Arrange
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, [], [], priceRange=None, isDiscriptionCheck=False, isPriceCheck=False)
        # Assert
        # If title patterns are empty, _filter_text returns all items because all([]) is True.
        self.assertEqual(len(filtered), len(self.sample_contents))


    def test_filter_text_multiple_patterns_all_must_match_title(self):
        # Arrange
        patterns = ["laptop", "pro"]
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, patterns, [], priceRange=None, isDiscriptionCheck=False, isPriceCheck=False)
        # Assert
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], 5) # Laptop Pro X2000

    def test_filter_text_multiple_patterns_all_must_match_description(self):
        # Arrange
        patterns = ["ergonomic", "responsive"]
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, [], patterns, priceRange=None, isDiscriptionCheck=True, isPriceCheck=False)
        # Assert
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], 3) # Wireless Mouse

    def test_filter_text_wildcard_in_pattern_title_matches_digits(self):
        # Arrange
        patterns = ["G*Force"] # Should match G123Force (ID 11) because * becomes \d*
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, patterns, [], priceRange=None, isDiscriptionCheck=False, isPriceCheck=False)
        # Assert
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], 11)

    def test_filter_text_wildcard_in_pattern_description_matches_digits(self):
        # Arrange
        patterns = ["144* screen"] # Should match "Size 14400 screen" (ID 12)
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, [], patterns, priceRange=None, isDiscriptionCheck=True, isPriceCheck=False)
        # Assert
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], 12)


    def test_filter_text_case_insensitivity_title(self):
        # Arrange
        patterns = ["amazing new laptop"]
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, patterns, [], priceRange=None, isDiscriptionCheck=False, isPriceCheck=False)
        # Assert
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], 1)

    def test_filter_text_case_insensitivity_description(self):
        # Arrange
        patterns = ["LATEST MODEL WITH GREAT SPECS"]
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, [], patterns, priceRange=None, isDiscriptionCheck=True, isPriceCheck=False)
        # Assert
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], 1)


    def test_price_filter_exact_match_lower_bound(self):
        # Arrange
        price_range = ("150.00", "200.00")
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, [], [], priceRange=price_range, isPriceCheck=True)
        # Assert
        ids = {item["id"] for item in filtered}
        self.assertIn(2, ids) # ID 2 has price 150.00
        self.assertEqual(len(ids), 1) # Only ID 2 (150.00)

    def test_price_filter_exact_match_upper_bound(self):
        # Arrange
        price_range = ("100.00", "150.00")
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, [], [], priceRange=price_range, isPriceCheck=True)
        # Assert
        # Items in range: ID 2 (150.00)
        ids = {item["id"] for item in filtered}
        self.assertEqual(ids, {2})


    def test_price_filter_no_items_in_range(self):
        # Arrange
        price_range = ("0.01", "0.05")
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, [], [], priceRange=price_range, isPriceCheck=True)
        # Assert
        self.assertEqual(len(filtered), 0)

    def test_price_filter_all_items_in_range(self):
        # Arrange
        price_range = ("0.00", "3000.00") # Max price is 2500
        # Act
        filtered = self.filter_services.filteringContent(self.sample_contents, [], [], priceRange=price_range, isPriceCheck=True)
        # Assert
        self.assertEqual(len(filtered), len(self.sample_contents))

if __name__ == '__main__':
    unittest.main()
