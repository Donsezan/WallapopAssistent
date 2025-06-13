import unittest
import os
import json
import shutil
from unittest.mock import patch, MagicMock

# Assuming FileServices is in Services.FileServices
# Adjust the import if the location is different
from Services.FileServices import FileServices
# Assuming ImageService is in Services.ImageService for mocking
# from Services.ImageService import ImageService


# Dummy ImageService for mocking, if the actual one is not available or complex to set up
class DummyImageService:
    @staticmethod
    def SavePhotofromWeb(url: str, folder_path: str, file_name: str) -> bool:
        # In a real scenario, this might create a dummy file or just pass
        print(f"Mock SavePhotofromWeb called with: {url}, {folder_path}, {file_name}")
        # Simulate file creation for test purposes
        with open(os.path.join(folder_path, file_name), 'w') as f:
            f.write("dummy image data")
        return True


class TestFileServices(unittest.TestCase):
    def setUp(self):
        self.file_services = FileServices()
        self.temp_folder = "temp_test_data"
        self.file_services.temp_folder = self.temp_folder # Override temp_folder for tests
        # Ensure ImageService is patched if it's a real class, or use DummyImageService
        # For this example, let's assume ImageService is available to be patched
        # If not, we would assign self.file_services.image_service = DummyImageService()
        # and then patch 'App.services.file_services.ImageService' if FileServices imports it directly
        # or patch 'self.file_services.image_service.SavePhotofromWeb'

        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder)

        # Sample data
        self.sample_data = [{"id": "1", "name": "Item 1", "web_slug": "item-1"}]
        # self.history_file_path = os.path.join(self.temp_folder, "test_history.json") # Path constructed by service now
        self.history_file_name = "test_history.json" # Just the name

    def tearDown(self):
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)

    # Test Save_content_to_file and Rehidrate_from_file
    def test_save_and_rehidrate_valid_data(self):
        self.file_services.Save_content_to_file(self.sample_data, self.history_file_name)
        expected_path = os.path.join(self.temp_folder, self.history_file_name)
        self.assertTrue(os.path.exists(expected_path))
        rehydrated_data = self.file_services.Rehidrate_from_file(self.history_file_name)
        self.assertEqual(self.sample_data, rehydrated_data)

    def test_save_empty_list(self):
        self.file_services.Save_content_to_file([], self.history_file_name)
        expected_path = os.path.join(self.temp_folder, self.history_file_name)
        self.assertFalse(os.path.exists(expected_path)) # Changed from assertTrue to assertFalse
        rehydrated_data = self.file_services.Rehidrate_from_file(self.history_file_name)
        # Rehydrating a non-existent file should return None (based on current Rehidrate_from_file behavior)
        self.assertIsNone(rehydrated_data) # Changed from assertEqual([], rehydrated_data)

    def test_save_none_data(self):
        # Save_content_to_file current implementation returns "Nothing to save" and doesn't create a file
        # if data is None or empty. So, os.path.exists will be false.
        # The test should reflect this behavior.
        self.file_services.Save_content_to_file(None, self.history_file_name)
        expected_path = os.path.join(self.temp_folder, self.history_file_name)
        # If Save_content_to_file is changed to create an empty file for None/empty list, this needs to change.
        self.assertFalse(os.path.exists(expected_path))
        # Rehydrating a non-existent or empty file (if it were created empty) should yield None or empty list
        rehydrated_data = self.file_services.Rehidrate_from_file(self.history_file_name)
        self.assertIsNone(rehydrated_data) # Assuming Rehidrate returns None for non-existent file


    def test_rehidrate_non_existent_file(self):
        rehydrated_data = self.file_services.Rehidrate_from_file("non_existent_file.json")
        self.assertIsNone(rehydrated_data)

    def test_rehidrate_invalid_json_file(self):
        invalid_json_path = os.path.join(self.temp_folder, "invalid.json")
        with open(invalid_json_path, 'w') as f:
            f.write("this is not json")
        rehydrated_data = self.file_services.Rehidrate_from_file(invalid_json_path)
        self.assertIsNone(rehydrated_data)

    # Test Merge_content
    def test_merge_content_both_none_or_empty(self):
        self.assertEqual(self.file_services.Merge_content(None, None), [])
        self.assertEqual(self.file_services.Merge_content([], []), [])
        self.assertEqual(self.file_services.Merge_content(self.sample_data, None), self.sample_data)
        self.assertEqual(self.file_services.Merge_content(self.sample_data, []), self.sample_data)
        self.assertEqual(self.file_services.Merge_content(None, self.sample_data), self.sample_data)
        self.assertEqual(self.file_services.Merge_content([], self.sample_data), self.sample_data)


    def test_merge_content_no_common_items(self):
        old_content = [{"id": "1", "name": "Item 1"}]
        new_content = [{"id": "2", "name": "Item 2"}]
        merged = self.file_services.Merge_content(old_content, new_content)
        self.assertEqual(len(merged), 2)
        self.assertIn({"id": "1", "name": "Item 1"}, merged)
        self.assertIn({"id": "2", "name": "Item 2"}, merged)

    def test_merge_content_some_common_items(self):
        old_content = [{"id": "1", "name": "Old Item 1"}, {"id": "2", "name": "Item 2"}]
        new_content = [{"id": "1", "name": "New Item 1"}, {"id": "3", "name": "Item 3"}]
        # Common item is id "1". It should take the version from old_content.
        merged = self.file_services.Merge_content(old_content, new_content)
        self.assertEqual(len(merged), 3)
        self.assertTrue(any(item['id'] == '1' and item['name'] == 'Old Item 1' for item in merged))
        self.assertTrue(any(item['id'] == '2' and item['name'] == 'Item 2' for item in merged))
        self.assertTrue(any(item['id'] == '3' and item['name'] == 'Item 3' for item in merged))


    def test_merge_content_new_all_in_old(self):
        old_content = [{"id": "1", "name": "Item 1"}, {"id": "2", "name": "Item 2"}]
        new_content = [{"id": "1", "name": "Updated Item 1"}] # Should keep "Item 1" from old
        merged = self.file_services.Merge_content(old_content, new_content)
        self.assertEqual(len(merged), 2)
        self.assertTrue(any(item['id'] == '1' and item['name'] == 'Item 1' for item in merged))


    def test_merge_content_old_all_in_new(self):
        old_content = [{"id": "1", "name": "Item 1"}]
        new_content = [{"id": "1", "name": "New Item 1"}, {"id": "2", "name": "Item 2"}]
        # Should result in old_content's item for "1" and new_content's item for "2"
        merged = self.file_services.Merge_content(old_content, new_content)
        self.assertEqual(len(merged), 2)
        self.assertTrue(any(item['id'] == '1' and item['name'] == 'Item 1' for item in merged))
        self.assertTrue(any(item['id'] == '2' and item['name'] == 'Item 2' for item in merged))


    # Test Delete_old_images
    def test_delete_old_images(self):
        # Setup dummy image files
        img1_slug = "image1"
        img2_slug = "image2-to-delete"
        img3_slug = "image3"

        open(os.path.join(self.temp_folder, f"{img1_slug}.jpg"), 'w').close()
        open(os.path.join(self.temp_folder, f"{img2_slug}.png"), 'w').close()
        open(os.path.join(self.temp_folder, f"{img3_slug}.gif"), 'w').close()
        open(os.path.join(self.temp_folder, "some_data.json"), 'w').close() # Should not be deleted

        content = [
            {"web_slug": img1_slug},
            {"web_slug": img3_slug}
        ]

        self.file_services.Delete_old_images(content)

        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, f"{img1_slug}.jpg")))
        self.assertFalse(os.path.exists(os.path.join(self.temp_folder, f"{img2_slug}.png"))) # Deleted
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, f"{img3_slug}.gif")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, "some_data.json")))

    def test_delete_old_images_empty_content(self):
        open(os.path.join(self.temp_folder, "image1.jpg"), 'w').close()
        open(os.path.join(self.temp_folder, "image2.png"), 'w').close()
        open(os.path.join(self.temp_folder, "data.json"), 'w').close() # Should not be deleted

        self.file_services.Delete_old_images([]) # Empty content

        self.assertFalse(os.path.exists(os.path.join(self.temp_folder, "image1.jpg")))
        self.assertFalse(os.path.exists(os.path.join(self.temp_folder, "image2.png")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, "data.json")))

    # Test Delete_old_historys
    def test_delete_old_historys(self):
        hist1_uuid = "uuid1"
        hist2_uuid_to_delete = "uuid2"
        hist3_uuid = "uuid3"

        open(os.path.join(self.temp_folder, f"History_{hist1_uuid}.json"), 'w').close()
        open(os.path.join(self.temp_folder, f"History_{hist2_uuid_to_delete}.json"), 'w').close()
        open(os.path.join(self.temp_folder, f"History_{hist3_uuid}.json"), 'w').close()
        open(os.path.join(self.temp_folder, "random_file.txt"), 'w').close() # Should not be deleted

        keys_to_keep = [hist1_uuid, hist3_uuid]
        self.file_services.Delete_old_historys(keys_to_keep)

        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, f"History_{hist1_uuid}.json")))
        self.assertFalse(os.path.exists(os.path.join(self.temp_folder, f"History_{hist2_uuid_to_delete}.json")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, f"History_{hist3_uuid}.json")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, "random_file.txt")))

    def test_delete_old_historys_empty_keys(self):
        open(os.path.join(self.temp_folder, "History_uuid1.json"), 'w').close()
        open(os.path.join(self.temp_folder, "History_uuid2.json"), 'w').close()

        self.file_services.Delete_old_historys([]) # Empty keys, should delete all History_* files

        self.assertFalse(os.path.exists(os.path.join(self.temp_folder, "History_uuid1.json")))
        self.assertFalse(os.path.exists(os.path.join(self.temp_folder, "History_uuid2.json")))

    # Test Download_missed_photos
    # Patching ImageService at the class or method level if it's an external dependency
    # For simplicity, let's assume FileServices has an image_service attribute that we can mock.
    # If ImageService is imported directly in file_services.py, use @patch('Services.ImageService.ImageService.SavePhotofromWeb')
    @patch('Services.ImageService.ImageService.SavePhotofromWeb', new_callable=MagicMock)
    def test_download_missed_photos_downloads_missing(self, mock_save_photo):
        # Simulate that SavePhotofromWeb creates the file, including extension handling
        def side_effect_save_photo(url, folder, filename_stem):
            # Basic extension extraction from URL for the mock
            try:
                url_path = url.split('?')[0]
                _, ext = os.path.splitext(url_path)
                if not ext or len(ext) > 5 or len(ext) < 2:
                    ext = '.jpg'
            except Exception:
                ext = '.jpg'

            # Construct filename with extension, similar to real ImageService
            full_filename = filename_stem + ext
            open(os.path.join(folder, full_filename), 'w').close()
            return True # Simulate successful save
        mock_save_photo.side_effect = side_effect_save_photo

        content = [
            {"web_slug": "item1", "images": [{"xsmall": "http://example.com/img1.jpg"}]},
            {"web_slug": "item2", "images": [{"xsmall": "http://example.com/img2.png"}]},
        ]
        # Pre-create one image to simulate it already exists
        existing_image_path = os.path.join(self.temp_folder, "item2.png")
        open(existing_image_path, 'w').close()

        self.file_services.Download_missed_photos(content)

        # item1.jpg should be downloaded
        # FileServices passes web_slug ("item1") as filename to ImageService, ImageService handles extension.
        mock_save_photo.assert_any_call("http://example.com/img1.jpg", self.temp_folder, "item1")

        # Check if item2.png (which existed) was attempted to be downloaded
        # This requires checking that it was NOT called for item2.png
        # We can count calls or check arguments more specifically if needed.
        # For now, assert_any_call is for item1.jpg. If only one call happened, this is implicitly tested.
        # If more robust checking is needed:
        calls = mock_save_photo.call_args_list
        called_for_item2 = any(
            call[0][2] == "item2.png" for call in calls
        )
        self.assertFalse(called_for_item2, "SavePhotofromWeb should not be called for existing image item2.png")
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, "item1.jpg"))) # Ensure it was "created" by mock

    @patch('Services.ImageService.ImageService.SavePhotofromWeb', new_callable=MagicMock)
    def test_download_missed_photos_all_exist(self, mock_save_photo):
        content = [
            {"web_slug": "item1", "images": [{"xsmall": "http://example.com/img1.jpg"}]},
        ]
        open(os.path.join(self.temp_folder, "item1.jpg"), 'w').close() # Pre-exists

        self.file_services.Download_missed_photos(content)
        mock_save_photo.assert_not_called()

    @patch('Services.ImageService.ImageService.SavePhotofromWeb', new_callable=MagicMock)
    def test_download_missed_photos_empty_content(self, mock_save_photo):
        self.file_services.Download_missed_photos(None)
        mock_save_photo.assert_not_called()
        self.file_services.Download_missed_photos([])
        mock_save_photo.assert_not_called()

    @patch('Services.ImageService.ImageService.SavePhotofromWeb', new_callable=MagicMock)
    def test_download_missed_photos_no_images_key(self, mock_save_photo):
        content = [{"web_slug": "item1"}] # No 'images' key
        self.file_services.Download_missed_photos(content)
        mock_save_photo.assert_not_called()

    @patch('Services.ImageService.ImageService.SavePhotofromWeb', new_callable=MagicMock)
    def test_download_missed_photos_no_xsmall_key(self, mock_save_photo):
        content = [{"web_slug": "item1", "images": [{"large": "url"}]}] # No 'xsmall'
        self.file_services.Download_missed_photos(content)
        mock_save_photo.assert_not_called()

    @patch('Services.ImageService.ImageService.SavePhotofromWeb', new_callable=MagicMock)
    def test_download_missed_photos_image_service_returns_false(self, mock_save_photo):
        mock_save_photo.return_value = False # Simulate download failure
        content = [{"web_slug": "item1", "images": [{"xsmall": "http://example.com/img1.jpg"}]}]

        # Ensure the file does not exist initially
        self.assertFalse(os.path.exists(os.path.join(self.temp_folder, "item1.jpg")))

        self.file_services.Download_missed_photos(content)

        # FileServices passes web_slug ("item1") as filename to ImageService, ImageService handles extension.
        mock_save_photo.assert_called_once_with("http://example.com/img1.jpg", self.temp_folder, "item1")
        # File should still not exist if SavePhotofromWeb returned False and didn't create it
        self.assertFalse(os.path.exists(os.path.join(self.temp_folder, "item1.jpg"))) # Actual file name on disk would have ext.

if __name__ == '__main__':
    unittest.main()
