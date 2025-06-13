import unittest
from Services.FiltersServices import FiltersServices

class TestFiltersServices(unittest.TestCase):

    def setUp(self):
        self.filters_services = FiltersServices()
        self.sample_contents = [
            {"title": "Amazing Product", "description": "This is a great product.", "price": 100},
            {"title": "Another Item", "description": "A different kind of item.", "price": 50},
            {"title": "Special Deal", "description": "Limited time offer!", "price": 75},
            {"title": "Generic Item", "description": "Just a regular item.", "price": 25},
            {"title": "Luxury Product", "description": "High-end luxury.", "price": 200}
        ]

    def test_filteringContent_empty_contents(self):
        result = self.filters_services.filteringContent(
            contents=[],
            titlePatern="",
            isDiscriptionCheck=False,
            discriptionPatern="",
            isPriceCheck=False,
            priceRange={"min": 0, "max": 0}
        )
        self.assertEqual(result, [])

    def test_filteringContent_title_match(self):
        result = self.filters_services.filteringContent(
            contents=self.sample_contents,
            titlePatern="Product",
            isDiscriptionCheck=False,
            discriptionPatern="",
            isPriceCheck=False,
            priceRange={"min": 0, "max": 0}
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "Amazing Product")
        self.assertEqual(result[1]["title"], "Luxury Product")

    def test_filteringContent_title_no_match(self):
        result = self.filters_services.filteringContent(
            contents=self.sample_contents,
            titlePatern="NonExistent",
            isDiscriptionCheck=False,
            discriptionPatern="",
            isPriceCheck=False,
            priceRange={"min": 0, "max": 0}
        )
        self.assertEqual(result, [])

    def test_filteringContent_description_match(self):
        result = self.filters_services.filteringContent(
            contents=self.sample_contents,
            titlePatern="",
            isDiscriptionCheck=True,
            discriptionPatern="great product",
            isPriceCheck=False,
            priceRange={"min": 0, "max": 0}
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["description"], "This is a great product.")

    def test_filteringContent_description_no_match(self):
        result = self.filters_services.filteringContent(
            contents=self.sample_contents,
            titlePatern="",
            isDiscriptionCheck=True,
            discriptionPatern="NonExistent",
            isPriceCheck=False,
            priceRange={"min": 0, "max": 0}
        )
        self.assertEqual(result, [])

    def test_filteringContent_price_match(self):
        result = self.filters_services.filteringContent(
            contents=self.sample_contents,
            titlePatern="",
            isDiscriptionCheck=False,
            discriptionPatern="",
            isPriceCheck=True,
            priceRange={"min": 50, "max": 100}
        )
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["price"], 100)
        self.assertEqual(result[1]["price"], 50)
        self.assertEqual(result[2]["price"], 75)


    def test_filteringContent_price_no_match(self):
        result = self.filters_services.filteringContent(
            contents=self.sample_contents,
            titlePatern="",
            isDiscriptionCheck=False,
            discriptionPatern="",
            isPriceCheck=True,
            priceRange={"min": 300, "max": 400}
        )
        self.assertEqual(result, [])

    def test_filteringContent_combination_match(self):
        result = self.filters_services.filteringContent(
            contents=self.sample_contents,
            titlePatern="Product",
            isDiscriptionCheck=True,
            discriptionPatern="luxury",
            isPriceCheck=True,
            priceRange={"min": 150, "max": 250}
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Luxury Product")

    def test_filteringContent_wildcard_title_match(self):
        result = self.filters_services.filteringContent(
            contents=self.sample_contents,
            titlePatern=".*Item", # Matches "Another Item" and "Generic Item"
            isDiscriptionCheck=False,
            discriptionPatern="",
            isPriceCheck=False,
            priceRange={"min": 0, "max": 0}
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "Another Item")
        self.assertEqual(result[1]["title"], "Generic Item")

    def test_filteringContent_wildcard_description_match(self):
        result = self.filters_services.filteringContent(
            contents=self.sample_contents,
            titlePatern="",
            isDiscriptionCheck=True,
            discriptionPatern="^This is", # Matches "This is a great product."
            isPriceCheck=False,
            priceRange={"min": 0, "max": 0}
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["description"], "This is a great product.")

if __name__ == '__main__':
    unittest.main()
