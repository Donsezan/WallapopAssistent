import unittest
import os
import json
from unittest.mock import patch, mock_open, MagicMock
from Services.FileServices import FileServices
from Services.ImageService import ImageService # Required for mocking

class TestFileServices(unittest.TestCase):

    def setUp(self):
        self.file_services = FileServices()
        self.temp_folder = self.file_services.temp_folder
        # Ensure temp folder exists for tests
        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder)

        # Clean up any files in temp folder before each test
        for item in os.listdir(self.temp_folder):
            item_path = os.path.join(self.temp_folder, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path): # Should not happen with current FileServices logic
                pass


    def tearDown(self):
        # Clean up temp folder after tests if needed, or leave for inspection
        for item in os.listdir(self.temp_folder):
            item_path = os.path.join(self.temp_folder, item)
            if os.path.isfile(item_path):
                try:
                    os.remove(item_path)
                except OSError: # Handle cases where file might be locked or already deleted by test
                    pass
        if os.path.exists(self.temp_folder) and not os.listdir(self.temp_folder):
             try:
                os.rmdir(self.temp_folder) # Remove temp_folder if it's empty
             except OSError: # Handle cases where rmdir might fail
                pass


    # Tests for Save_content_to_file
    def test_save_content_to_file_valid_data(self):
        # Arrange
        data = {"key": "value", "number": 123}
        file_name = "test_output.json"
        file_path = os.path.join(self.temp_folder, file_name)

        # Act
        self.file_services.Save_content_to_file(data, file_name)

        # Assert
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r') as f:
            saved_data = json.load(f)
        self.assertEqual(data, saved_data)

    def test_save_content_to_file_empty_data(self):
        # Arrange
        data = []
        file_name = "empty_data.json"

        # Act
        result = self.file_services.Save_content_to_file(data, file_name)

        # Assert
        self.assertEqual(result, "Nothing to save")
        file_path = os.path.join(self.temp_folder, file_name)
        self.assertFalse(os.path.exists(file_path))

    def test_save_content_to_file_none_data(self):
        # Arrange
        data = None
        file_name = "none_data.json"

        # Act
        result = self.file_services.Save_content_to_file(data, file_name)

        # Assert
        self.assertEqual(result, "Nothing to save")
        file_path = os.path.join(self.temp_folder, file_name)
        self.assertFalse(os.path.exists(file_path))

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.join') # Mock path join to control the path used in print
    def test_save_content_to_file_io_error(self, mock_os_path_join, mock_file_open):
        # Arrange
        mock_os_path_join.return_value = os.path.join(self.temp_folder, "error.json") # Expected path
        mock_file_open.side_effect = IOError("Test IOError")
        data = {"key": "value"}
        file_name = "error.json" # This name is passed to Save_content_to_file

        # Act & Assert
        with patch('builtins.print') as mock_print:
            self.file_services.Save_content_to_file(data, file_name)
            # Assert that the print call includes the path formed by os.path.join
            mock_print.assert_any_call(f"Error saving object to {os.path.join(self.temp_folder, file_name)}: Test IOError")


    # Tests for Rehidrate_from_file
    def test_rehidrate_from_file_valid_json(self):
        # Arrange
        data = {"key": "value", "number": 456}
        file_name = "valid_rehydrate.json"
        file_path = os.path.join(self.temp_folder, file_name)
        with open(file_path, 'w') as f:
            json.dump(data, f)

        # Act
        rehydrated_data = self.file_services.Rehidrate_from_file(file_name)

        # Assert
        self.assertEqual(data, rehydrated_data)

    def test_rehidrate_from_file_non_existing_file(self):
        # Arrange
        file_name = "non_existing.json"

        # Act & Assert
        with patch('builtins.print') as mock_print:
            result = self.file_services.Rehidrate_from_file(file_name)
            self.assertIsNone(result)
            mock_print.assert_any_call(f"Error: File '{file_name}' not found.")


    def test_rehidrate_from_file_empty_json_file(self):
        # Arrange
        file_name = "empty_file.json"
        file_path = os.path.join(self.temp_folder, file_name)
        with open(file_path, 'w') as f:
            pass

        # Act & Assert
        with patch('builtins.print') as mock_print:
            result = self.file_services.Rehidrate_from_file(file_name)
            self.assertIsNone(result)
            mock_print.assert_any_call(f"Error: Unable to decode JSON in file '{file_name}'. File may be empty or not valid JSON.")

    def test_rehidrate_from_file_invalid_json_file(self):
        # Arrange
        file_name = "invalid_file.json"
        file_path = os.path.join(self.temp_folder, file_name)
        with open(file_path, 'w') as f:
            f.write("this is not json")

        # Act & Assert
        with patch('builtins.print') as mock_print:
            result = self.file_services.Rehidrate_from_file(file_name)
            self.assertIsNone(result)
            mock_print.assert_any_call(f"Error: Unable to decode JSON in file '{file_name}'. File may be empty or not valid JSON.")


    # Tests for Merge_content
    def test_merge_content_no_duplicates(self):
        # Arrange
        old_obj = [{"id": "1", "data": "a"}, {"id": "2", "data": "b"}]
        new_obj = [{"id": "2", "data": "b_new"}, {"id": "3", "data": "c"}]
        expected = [{"id": "1", "data": "a"}, {"id": "2", "data": "b"}, {"id": "3", "data": "c"}]

        # Act
        with patch('builtins.print') as mock_print: # Suppress print within Merge_content
            merged = self.file_services.Merge_content(old_obj, new_obj)

        merged_sorted = sorted(merged, key=lambda x: x['id'])
        expected_sorted = sorted(expected, key=lambda x: x['id'])

        # Assert
        self.assertEqual(merged_sorted, expected_sorted)

    def test_merge_content_old_empty(self):
        # Arrange
        old_obj = []
        new_obj = [{"id": "1", "data": "a"}, {"id": "2", "data": "b"}]

        # Act
        with patch('builtins.print') as mock_print:
            merged = self.file_services.Merge_content(old_obj, new_obj)

        # Assert
        self.assertEqual(merged, new_obj)

    def test_merge_content_new_empty(self):
        # Arrange
        old_obj = [{"id": "1", "data": "a"}, {"id": "2", "data": "b"}]
        new_obj = []

        # Act
        with patch('builtins.print') as mock_print:
            merged = self.file_services.Merge_content(old_obj, new_obj)

        # Assert
        self.assertEqual(merged, old_obj)

    def test_merge_content_both_empty(self):
        # Arrange
        old_obj = []
        new_obj = []

        # Act
        with patch('builtins.print') as mock_print:
            merged = self.file_services.Merge_content(old_obj, new_obj)

        # Assert
        self.assertEqual(merged, [])

    def test_merge_content_old_none(self):
        # Arrange
        old_obj = None
        new_obj = [{"id": "1", "data": "a"}]

        # Act
        with patch('builtins.print') as mock_print:
            merged = self.file_services.Merge_content(old_obj, new_obj)

        # Assert
        self.assertEqual(merged, new_obj)

    def test_merge_content_new_none(self):
        # Arrange
        old_obj = [{"id": "1", "data": "a"}]
        new_obj = None

        # Act
        with patch('builtins.print') as mock_print:
            merged = self.file_services.Merge_content(old_obj, new_obj)

        # Assert
        self.assertEqual(merged, old_obj)

    def test_merge_content_both_none(self):
        # Arrange
        old_obj = None
        new_obj = None

        # Act
        with patch('builtins.print') as mock_print:
            merged = self.file_services.Merge_content(old_obj, new_obj)

        # Assert
        self.assertIsNone(merged)

    # Tests for Delete_old_images
    def test_delete_old_images_deletes_unlisted(self):
        # Arrange
        content = [{"web_slug": "image1"}, {"web_slug": "image3"}]
        open(os.path.join(self.temp_folder, "image1.jpg"), 'w').close()
        open(os.path.join(self.temp_folder, "image2.png"), 'w').close()
        open(os.path.join(self.temp_folder, "image3.gif"), 'w').close()
        open(os.path.join(self.temp_folder, "data.json"), 'w').close()

        # Act
        with patch('builtins.print') as mock_print:
            self.file_services.Delete_old_images(content)

        # Assert
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, "image1.jpg")))
        self.assertFalse(os.path.exists(os.path.join(self.temp_folder, "image2.png")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, "image3.gif")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, "data.json")))

    def test_delete_old_images_empty_content(self):
        # Arrange
        content = []
        open(os.path.join(self.temp_folder, "imageA.jpg"), 'w').close()
        open(os.path.join(self.temp_folder, "imageB.png"), 'w').close()
        open(os.path.join(self.temp_folder, "config.json"), 'w').close()

        # Act
        with patch('builtins.print') as mock_print:
            self.file_services.Delete_old_images(content)

        # Assert
        self.assertFalse(os.path.exists(os.path.join(self.temp_folder, "imageA.jpg")))
        self.assertFalse(os.path.exists(os.path.join(self.temp_folder, "imageB.png")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, "config.json")))

    def test_delete_old_images_none_content(self):
        # Arrange
        content = None
        open(os.path.join(self.temp_folder, "imageC.jpg"), 'w').close()
        open(os.path.join(self.temp_folder, "settings.json"), 'w').close()

        # Act
        with patch('builtins.print') as mock_print:
            self.file_services.Delete_old_images(content)

        # Assert
        self.assertFalse(os.path.exists(os.path.join(self.temp_folder, "imageC.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, "settings.json")))

    @patch('os.remove')
    @patch('builtins.print')
    def test_delete_old_images_os_error_on_delete(self, mock_print, mock_os_remove):
        # Arrange
        content = []
        image_to_fail_delete = "image_fail.jpg"
        image_path = os.path.join(self.temp_folder, image_to_fail_delete)
        open(image_path, 'w').close()

        mock_os_remove.side_effect = OSError("Test OS error")

        # Act
        self.file_services.Delete_old_images(content)

        # Assert
        mock_os_remove.assert_called_once_with(image_path)
        mock_print.assert_any_call(f"Error: Unable to delete file '{image_path}'.")
        mock_print.assert_any_call(f"Error details: Test OS error")


    # Tests for Delete_old_historys
    def test_delete_old_historys_deletes_unlisted(self):
        # Arrange
        keys = ["uuid1", "uuid3"]
        open(os.path.join(self.temp_folder, "History_uuid1.json"), 'w').close()
        open(os.path.join(self.temp_folder, "History_uuid2.json"), 'w').close()
        open(os.path.join(self.temp_folder, "History_uuid3.json"), 'w').close()
        open(os.path.join(self.temp_folder, "Otherfile.txt"), 'w').close()

        # Act
        with patch('builtins.print') as mock_print:
            self.file_services.Delete_old_historys(keys)

        # Assert
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, "History_uuid1.json")))
        self.assertFalse(os.path.exists(os.path.join(self.temp_folder, "History_uuid2.json")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, "History_uuid3.json")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, "Otherfile.txt")))

    def test_delete_old_historys_empty_keys(self):
        # Arrange
        keys = []
        open(os.path.join(self.temp_folder, "History_uuidA.json"), 'w').close()
        open(os.path.join(self.temp_folder, "History_uuidB.json"), 'w').close()
        open(os.path.join(self.temp_folder, "image.jpg"), 'w').close()

        # Act
        with patch('builtins.print') as mock_print:
            self.file_services.Delete_old_historys(keys)

        # Assert
        self.assertFalse(os.path.exists(os.path.join(self.temp_folder, "History_uuidA.json")))
        self.assertFalse(os.path.exists(os.path.join(self.temp_folder, "History_uuidB.json")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, "image.jpg")))

    # Tests for Download_missed_photos
    @patch.object(ImageService, 'SavePhotofromWeb')
    def test_download_missed_photos_downloads_missing(self, mock_save_photo):
        # Arrange
        contents = [
            {"web_slug": "photo1", "images": [{"urls": {"small": "http://example.com/photo1.jpg?params"}}]}, # Will be downloaded
            {"web_slug": "photo2", "images": [{"urls": {"small": "http://example.com/photo2.png?params"}}]}  # Should not be downloaded
        ]
        # Simulate photo2 exists by creating "photo2.jpg" because Download_missed_photos checks for .jpg
        photo2_checked_path = os.path.join(self.temp_folder, "photo2.jpg")
        open(photo2_checked_path, 'w').close()

        # Act
        self.file_services.Download_missed_photos(contents)

        # Assert
        # SavePhotofromWeb should only be called for photo1
        mock_save_photo.assert_called_once_with("http://example.com/photo1.jpg", "photo1")
        # Ensure the mock file we created to simulate existence is still there
        self.assertTrue(os.path.exists(photo2_checked_path))


    @patch.object(ImageService, 'SavePhotofromWeb')
    def test_download_missed_photos_all_present(self, mock_save_photo):
        # Arrange
        contents = [
            {"web_slug": "photoA", "images": [{"urls": {"small": "http://example.com/photoA.jpg"}}]},
            {"web_slug": "photoB", "images": [{"urls": {"small": "http://example.com/photoB.png"}}]}
        ]
        # Download_missed_photos checks for .jpg extension regardless of actual image type in URL
        open(os.path.join(self.temp_folder, "photoA.jpg"), 'w').close()
        open(os.path.join(self.temp_folder, "photoB.jpg"), 'w').close() # Simulate photoB.jpg exists

        # Act
        self.file_services.Download_missed_photos(contents)

        # Assert
        mock_save_photo.assert_not_called()


    @patch.object(ImageService, 'SavePhotofromWeb')
    def test_download_missed_photos_empty_content(self, mock_save_photo):
        # Arrange
        contents = []

        # Act
        self.file_services.Download_missed_photos(contents)

        # Assert
        mock_save_photo.assert_not_called()

    @patch.object(ImageService, 'SavePhotofromWeb')
    def test_download_missed_photos_none_content(self, mock_save_photo):
        # Arrange
        contents = None

        # Act
        self.file_services.Download_missed_photos(contents)

        # Assert
        mock_save_photo.assert_not_called()

if __name__ == '__main__':
    unittest.main()
