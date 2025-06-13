import unittest
import os
import json
import shutil
import sys
from unittest.mock import patch, mock_open, MagicMock

# Add project root to sys.path to allow importing from Services
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from Services.FileServices import FileServices
from Services.ImageService import ImageService # For mocking

class TestFileServices(unittest.TestCase):

    def setUp(self):
        self.test_temp_folder = "test_temp_files_dir"
        # Create the directory if it doesn't exist, handle if it does
        os.makedirs(self.test_temp_folder, exist_ok=True)

        self.file_services = FileServices()
        self.file_services.temp_folder = self.test_temp_folder # Override temp_folder

        # Define path to Sample-History.json in the project root
        self.sample_history_path = os.path.join(project_root, "Sample-History.json")
        try:
            with open(self.sample_history_path, 'r') as f:
                self.sample_data = json.load(f)
        except FileNotFoundError:
            self.fail(f"Failed to load {self.sample_history_path}. Make sure the file exists in the project root.")
        except json.JSONDecodeError:
            self.fail(f"Failed to decode JSON from {self.sample_history_path}.")


        self.history_file_name = "test_history.json"
        self.image_service_mock = MagicMock(spec=ImageService)
        self.file_services.imageService = self.image_service_mock


    def tearDown(self):
        if os.path.exists(self.test_temp_folder):
            shutil.rmtree(self.test_temp_folder)

    def _get_test_file_path(self, filename):
        return os.path.join(self.test_temp_folder, filename)

    def test_save_content_to_file_success(self):
        result = self.file_services.Save_content_to_file(self.sample_data, self.history_file_name)
        expected_path = self._get_test_file_path(self.history_file_name)
        self.assertTrue(os.path.exists(expected_path))
        with open(expected_path, 'r') as f:
            content = json.load(f)
        self.assertEqual(content, self.sample_data)
        self.assertIsNone(result) # Assuming it returns None on success

    def test_save_content_to_file_empty_data(self):
        result = self.file_services.Save_content_to_file([], "empty.json")
        self.assertFalse(os.path.exists(self._get_test_file_path("empty.json")))
        self.assertEqual(result, "Nothing to save")

    def test_rehidrate_from_file_success(self):
        # First, save sample_data to history_file_name
        self.file_services.Save_content_to_file(self.sample_data, self.history_file_name)
        retrieved_data = self.file_services.Rehidrate_from_file(self.history_file_name)
        self.assertEqual(retrieved_data, self.sample_data)

    def test_rehidrate_from_file_not_found(self):
        retrieved_data = self.file_services.Rehidrate_from_file("non_existent_file.json")
        self.assertIsNone(retrieved_data)

    def test_rehidrate_from_file_invalid_json(self):
        invalid_json_path = self._get_test_file_path("invalid.json")
        with open(invalid_json_path, 'w') as f:
            f.write("This is not valid JSON")
        retrieved_data = self.file_services.Rehidrate_from_file("invalid.json")
        self.assertIsNone(retrieved_data)

    def test_merge_content_new_items(self):
        old_object = [self.sample_data[0]]
        new_object = [self.sample_data[1], self.sample_data[2]]
        merged = self.file_services.Merge_content(old_object, new_object)
        self.assertEqual(len(merged), 3)
        self.assertIn(self.sample_data[0], merged)
        self.assertIn(self.sample_data[1], merged)
        self.assertIn(self.sample_data[2], merged)

    def test_merge_content_no_duplicates(self):
        old_object = [self.sample_data[0], self.sample_data[1]]
        new_object = [self.sample_data[1], self.sample_data[2]] # sample_data[1] is a duplicate
        merged = self.file_services.Merge_content(old_object, new_object)
        self.assertEqual(len(merged), 3)
        merged_ids = [item['id'] for item in merged]
        self.assertIn(self.sample_data[0]['id'], merged_ids)
        self.assertIn(self.sample_data[1]['id'], merged_ids)
        self.assertIn(self.sample_data[2]['id'], merged_ids)
        self.assertEqual(merged_ids.count(self.sample_data[1]['id']), 1)


    def test_merge_content_empty_inputs(self):
        self.assertIsNone(self.file_services.Merge_content(None, None))
        self.assertEqual(self.file_services.Merge_content(self.sample_data, None), self.sample_data)
        self.assertEqual(self.file_services.Merge_content(None, self.sample_data), self.sample_data)
        self.assertEqual(self.file_services.Merge_content(self.sample_data, []), self.sample_data)
        self.assertEqual(self.file_services.Merge_content([], self.sample_data), self.sample_data)

    def test_delete_old_images(self):
        # Create dummy image files
        img1_path = self._get_test_file_path("img1.jpg")
        img_to_delete_path = self._get_test_file_path("img_to_delete.png")
        kept_image_slug = self.sample_data[0]['web_slug'] # "vintage-leather-jacket-123"
        kept_image_path = self._get_test_file_path(f"{kept_image_slug}.jpg")
        dummy_json_path = self._get_test_file_path("some_data.json")

        open(img1_path, 'w').close()
        open(img_to_delete_path, 'w').close()
        open(kept_image_path, 'w').close()
        open(dummy_json_path, 'w').write("{}")


        content_to_keep = [{"web_slug": kept_image_slug}, {"web_slug": "img1"}]
        self.file_services.Delete_old_images(content_to_keep)

        self.assertTrue(os.path.exists(kept_image_path))
        self.assertTrue(os.path.exists(img1_path))
        self.assertFalse(os.path.exists(img_to_delete_path))
        self.assertTrue(os.path.exists(dummy_json_path)) # JSON file should not be deleted

    def test_delete_old_historys(self):
        history_abc_path = self._get_test_file_path("History_abc.json")
        history_def_path = self._get_test_file_path("History_def.json")
        history_ghi_path = self._get_test_file_path("History_ghi.json")
        random_file_path = self._get_test_file_path("random_file.txt")

        open(history_abc_path, 'w').close()
        open(history_def_path, 'w').close()
        open(history_ghi_path, 'w').close()
        open(random_file_path, 'w').close()

        keys_to_keep = ["abc", "ghi"]
        self.file_services.Delete_old_historys(keys_to_keep)

        self.assertTrue(os.path.exists(history_abc_path))
        self.assertTrue(os.path.exists(history_ghi_path))
        self.assertFalse(os.path.exists(history_def_path))
        self.assertTrue(os.path.exists(random_file_path)) # Non-history file should not be deleted

    @patch('Services.FileServices.os.path.exists') # Patch os.path.exists used within FileServices itself
    def test_download_missed_photos(self, mock_os_exists):
        # Mock ImageService.SavePhotofromWeb which is now an instance variable
        self.file_services.imageService.SavePhotofromWeb = MagicMock(return_value="mocked_path.jpg")

        content_with_missing_photos = [self.sample_data[0], self.sample_data[1]]

        # Simulate images are missing
        mock_os_exists.return_value = False
        self.file_services.Download_missed_photos(content_with_missing_photos)

        self.assertEqual(self.file_services.imageService.SavePhotofromWeb.call_count, len(content_with_missing_photos))
        calls = []
        for item in content_with_missing_photos:
            expected_url = item['images'][0]['xsmall'].split('?', 1)[0]
            expected_filename = item['web_slug']
            # Check if any call matches the expected arguments
            self.assertTrue(
                any(
                    call_args[0][0] == expected_url and call_args[0][1] == expected_filename
                    for call_args in self.file_services.imageService.SavePhotofromWeb.call_args_list
                ),
                f"Expected call with ({expected_url}, {expected_filename}) not found"
            )


        # Reset mock for the next scenario
        self.file_services.imageService.SavePhotofromWeb.reset_mock()

        # Simulate images exist
        mock_os_exists.return_value = True
        self.file_services.Download_missed_photos(content_with_missing_photos)
        self.file_services.imageService.SavePhotofromWeb.assert_not_called()

if __name__ == '__main__':
    unittest.main()
