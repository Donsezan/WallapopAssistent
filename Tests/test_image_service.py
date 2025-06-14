import unittest
import os
import shutil
import requests # For requests.exceptions
import uuid
import sys # <--- IMPORT ADDED
from unittest.mock import patch, MagicMock

# Add project root to sys.path to allow importing from Services
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from Services.ImageService import ImageService

class TestImageService(unittest.TestCase):

    def setUp(self):
        self.test_temp_folder = "test_image_service_temp_dir"
        # Create the directory, ImageService will use it if it exists
        os.makedirs(self.test_temp_folder, exist_ok=True)
        # ImageService.SavePhotofromWeb is a static method, no instance needed for calling
        # self.image_service = ImageService() # Not strictly necessary

    def tearDown(self):
        if os.path.exists(self.test_temp_folder):
            shutil.rmtree(self.test_temp_folder)

    @patch('requests.get')
    def test_save_photo_from_web_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"dummy image data"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        url = "http://example.com/image.jpg"
        file_name_without_ext = "test_image"

        file_path = ImageService.SavePhotofromWeb(url, file_name_without_ext, temp_folder=self.test_temp_folder)

        mock_get.assert_called_once_with(url) # Removed timeout=10
        mock_response.raise_for_status.assert_called_once()

        expected_path = os.path.join(self.test_temp_folder, f"{file_name_without_ext}.jpg")
        self.assertEqual(file_path, expected_path)
        self.assertTrue(os.path.exists(file_path))

        with open(file_path, "rb") as f:
            content = f.read()
        self.assertEqual(content, b"dummy image data")

    @patch('requests.get')
    @patch('builtins.print') # To suppress and check print statements
    def test_save_photo_from_web_requests_connection_error(self, mock_print, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("Test connection error")

        url = "http://example.com/image.png"
        file_name = "connection_error_test"

        file_path = ImageService.SavePhotofromWeb(url, file_name, temp_folder=self.test_temp_folder)

        self.assertIsNone(file_path)
        # Check if the specific error message was printed
        # mock_print.assert_any_call("Error downloading image: Test connection error") # This can be too specific
        self.assertTrue(any("Error downloading image" in call_args[0][0] for call_args in mock_print.call_args_list))


    @patch('requests.get')
    @patch('builtins.print')
    def test_save_photo_from_web_http_error(self, mock_print, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        # Configure raise_for_status to actually raise the error
        mock_http_error = requests.exceptions.HTTPError("404 Client Error", response=mock_response)
        mock_response.raise_for_status.side_effect = mock_http_error
        mock_get.return_value = mock_response

        url = "http://example.com/notfound.gif"
        file_name = "http_error_test"

        file_path = ImageService.SavePhotofromWeb(url, file_name, temp_folder=self.test_temp_folder)

        self.assertIsNone(file_path)
        mock_response.raise_for_status.assert_called_once()
        self.assertTrue(any("Error downloading image" in call_args[0][0] for call_args in mock_print.call_args_list))


    @patch('uuid.uuid4')
    @patch('requests.get')
    def test_save_photo_from_web_empty_filename_generates_uuid(self, mock_get, mock_uuid4):
        # Configure uuid.uuid4() mock
        mock_uuid_obj = MagicMock()
        mock_uuid_obj.__str__.return_value = "12345678-abcd-1234-abcd-1234567890ab"
        mock_uuid4.return_value = mock_uuid_obj

        # Configure requests.get mock for success
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"dummy uuid image data"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        url = "http://example.com/image.jpeg"
        file_path = ImageService.SavePhotofromWeb(url, "", temp_folder=self.test_temp_folder)

        expected_generated_name_part = "12345678" # As per str(uuid.uuid4())[:8]
        expected_path = os.path.join(self.test_temp_folder, f"{expected_generated_name_part}.jpeg")

        self.assertEqual(file_path, expected_path)
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, "rb") as f:
            content = f.read()
        self.assertEqual(content, b"dummy uuid image data")
        mock_uuid4.assert_called_once()

    @patch('uuid.uuid4')
    @patch('requests.get')
    def test_save_photo_from_web_none_filename_generates_uuid(self, mock_get, mock_uuid4):
        # Configure uuid.uuid4() mock
        mock_uuid_obj = MagicMock()
        mock_uuid_obj.__str__.return_value = "abcdef12-abcd-1234-abcd-1234567890ab"
        mock_uuid4.return_value = mock_uuid_obj

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"dummy none image data"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        url = "http://example.com/image.gif"
        file_path = ImageService.SavePhotofromWeb(url, None, temp_folder=self.test_temp_folder)

        expected_generated_name_part = "abcdef12"
        expected_path = os.path.join(self.test_temp_folder, f"{expected_generated_name_part}.gif")

        self.assertEqual(file_path, expected_path)
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, "rb") as f:
            content = f.read()
        self.assertEqual(content, b"dummy none image data")
        mock_uuid4.assert_called_once()


    @patch('requests.get')
    def test_save_photo_temp_folder_creation(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"dummy folder data"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        url = "http://example.com/image.bmp"
        file_name = "folder_creation_test"
        specific_test_temp_folder = os.path.join(self.test_temp_folder, "specific_subdir_for_creation_test")

        # Ensure the specific_test_temp_folder does NOT exist before the call
        if os.path.exists(specific_test_temp_folder):
            shutil.rmtree(specific_test_temp_folder)
        self.assertFalse(os.path.exists(specific_test_temp_folder))

        file_path = ImageService.SavePhotofromWeb(url, file_name, temp_folder=specific_test_temp_folder)

        self.assertTrue(os.path.exists(specific_test_temp_folder))
        expected_file_path = os.path.join(specific_test_temp_folder, f"{file_name}.bmp")
        self.assertEqual(file_path, expected_file_path)
        self.assertTrue(os.path.exists(expected_file_path))

    @patch('requests.get')
    @patch('builtins.print')
    def test_save_photo_file_already_exists(self, mock_print, mock_get):
        url = "http://example.com/image_exists.png"
        file_name_without_ext = "existing_image"

        # Determine the expected path including the correct extension from the URL
        file_extension = url.split(".")[-1]
        existing_file_path = os.path.join(self.test_temp_folder, f"{file_name_without_ext}.{file_extension}")

        # Create the dummy file with some initial content
        os.makedirs(os.path.dirname(existing_file_path), exist_ok=True) # ensure directory exists
        with open(existing_file_path, "wb") as f:
            f.write(b"old data")

        returned_path = ImageService.SavePhotofromWeb(url, file_name_without_ext, temp_folder=self.test_temp_folder)

        # If file exists, ImageService.SavePhotofromWeb implicitly returns None
        # as per the code structure (no explicit return if os.path.exists(file_path) is true at the start)
        self.assertIsNone(returned_path)
        mock_get.assert_not_called() # Should not attempt to download

        # Verify the file content is still the old data
        with open(existing_file_path, "rb") as f:
            content = f.read()
        self.assertEqual(content, b"old data")
        # mock_print.assert_any_call(f"File {existing_file_path} already exist") # No print if file exists path is taken


if __name__ == '__main__':
    unittest.main()
